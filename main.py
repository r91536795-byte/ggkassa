import os
import telebot
from telebot import types

TOKEN = os.environ.get("TOKEN")
ADMIN_ID = int(os.environ.get("8349263362"))

bot = telebot.TeleBot(TOKEN)

# хранение последнего пользователя для ответа
last_user = {}

# 🚀 START
@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("📩 Написать в поддержку")
    markup.add(btn)

    bot.send_message(
        message.chat.id,
        "👋 Добро пожаловать в поддержку!\n\nНажмите кнопку ниже 👇",
        reply_markup=markup
    )

# 📩 КНОПКА ПОДДЕРЖКИ
@bot.message_handler(func=lambda m: m.text == "📩 Написать в поддержку")
def support(message):
    bot.send_message(message.chat.id, "✍ Напишите ваш вопрос или отправьте фото")

# 📩 ТЕКСТ ОТ ПОЛЬЗОВАТЕЛЯ
@bot.message_handler(content_types=["text"])
def text_handler(message):

    # если это ответ админа
    if message.from_user.id == ADMIN_ID and message.reply_to_message:
        user_id = int(message.reply_to_message.text.split("ID: ")[1].split("\n")[0])

        bot.send_message(user_id, f"💬 Ответ поддержки:\n\n{message.text}")
        bot.send_message(ADMIN_ID, "✅ Ответ отправлен")
        return

    # отправка админу
    msg = bot.send_message(
        ADMIN_ID,
        f"📩 Сообщение\n\nID: {message.from_user.id}\n\n{message.text}\n\n👉 Ответь просто reply на это сообщение"
    )

    last_user[msg.message_id] = message.from_user.id

    bot.reply_to(message, "✅ Отправлено в поддержку")

# 🖼 ФОТО
@bot.message_handler(content_types=["photo"])
def photo_handler(message):

    msg = bot.send_photo(
        ADMIN_ID,
        message.photo[-1].file_id,
        caption=f"📩 Фото\n\nID: {message.from_user.id}\n\n👉 Ответь reply на это сообщение"
    )

    last_user[msg.message_id] = message.from_user.id

    bot.reply_to(message, "✅ Фото отправлено")

bot.infinity_polling()
