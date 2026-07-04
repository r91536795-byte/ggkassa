import os
import telebot
from telebot import types

TOKEN = os.environ.get("TOKEN")

# 👇 твой Telegram ID уже вставлен
ADMIN_ID = 8349263362

if not TOKEN:
    raise Exception("TOKEN не задан в Render")

bot = telebot.TeleBot(TOKEN)

OPERATOR_ONLINE = True

@bot.message_handler(commands=["start"])
def start(message):
    status = "🟢 Оператор в сети" if OPERATOR_ONLINE else "🔴 Оператор оффлайн"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📩 Написать в поддержку")

    bot.send_message(
        message.chat.id,
        f"👋 Привет!\n\n{status}\n\nНажми кнопку ниже 👇",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text == "📩 Написать в поддержку")
def support(message):
    status = "🟢 Оператор в сети" if OPERATOR_ONLINE else "🔴 Оператор оффлайн"

    bot.send_message(
        message.chat.id,
        f"{status}\n\n✍ Напишите ваш вопрос или отправьте фото"
    )

@bot.message_handler(content_types=["text"])
def text_handler(message):

    if message.from_user.id == ADMIN_ID and message.reply_to_message:
        try:
            if "ID:" in message.reply_to_message.text:
                user_id = int(
                    message.reply_to_message.text.split("ID: ")[1].split("\n")[0]
                )

                bot.send_message(user_id, f"💬 Ответ поддержки:\n\n{message.text}")
                bot.send_message(ADMIN_ID, "✅ Ответ отправлен")
        except:
            bot.send_message(ADMIN_ID, "❌ Ошибка ответа")
        return

    bot.send_message(
        ADMIN_ID,
        f"📩 Сообщение\n\n👤 ID: {message.from_user.id}\n\n💬 {message.text}"
    )

    bot.reply_to(message, "✅ Отправлено")

@bot.message_handler(content_types=["photo"])
def photo_handler(message):

    bot.send_photo(
        ADMIN_ID,
        message.photo[-1].file_id,
        caption=f"📩 Фото\n\n👤 ID: {message.from_user.id}"
    )

    bot.reply_to(message, "✅ Отправлено")

print("Bot started...")
bot.infinity_polling(skip_pending=True)
