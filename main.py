import requests
import telebot
from telebot import types
from dotenv import load_dotenv
import os


load_dotenv()
token_tg = os.environ["TOKEN_TG"]
bot = telebot.TeleBot(token_tg)


@bot.message_handler(commands=["start"])
def button_processing(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item_help = types.InlineKeyboardButton("Помощь🙏", callback_data="help")
    item_convert = types.InlineKeyboardButton(
        "Конвертировать валюту💸", callback_data="convert"
    )
    markup.add(item_help, item_convert)

    bot.send_message(message.chat.id, "Привет!", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def checking_buttons(call):
    chat_id = call.message.chat.id

    if call.data == "help":
        bot.send_message(
            chat_id,
            "Чтобы конвертировать валюту, отправьте сообщение в формате `100 RUB USD` То - Есть сначала пишите кол-во валюты, потом пишите какая эта валюта, и потом уже пишете в какую хотите.😁😁😁",
        )
    elif call.data == "convert":
        bot.send_message(
            chat_id,
            "Для конвертации валюты отправьте сообщение в формате 100 `RUB USD`.🥠",
        )
    else:
        bot.send_message(chat_id, "Произошла ошибка. Пожалуйста, попробуйте еще раз.😡")


@bot.message_handler(func=lambda message: True)
def convert_currency(message):
    try:
        chat_id = message.chat.id
        text = message.text.strip()
        amount, from_currency, to_currency = text.split()
        amount = float(amount)
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        response = requests.get(url)
        data = response.json()
        rate = data["rates"][to_currency]
        result = amount * rate
        bot.send_message(chat_id, f"{amount} {from_currency} = {result} {to_currency}")
    except Exception as e:
        bot.send_message(
            chat_id,
            "Произошла ошибка. Пожалуйста, убедитесь, что введены корректные данные для конвертации.",
        )


# def main():

if __name__ == "__main__":
    bot.polling()
