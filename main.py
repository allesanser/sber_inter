import telebot
from telebot.async_telebot import AsyncTeleBot
import asyncio
import re
import pickle
from pymystem3 import Mystem


bot = AsyncTeleBot('#### тут id бота')
m = Mystem()
filename = 'forest_model.sav'
model = pickle.load(open(filename, 'rb'))


def clean_text(text):
        text = text.lower()
        text = re.sub('\s+', ' ', text)
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub('пожалуйста', '', text)
        text = re.sub('какая', '', text)
        text = re.sub('какой', '', text)
        text = re.sub('подскажи', '', text)
        text = re.sub('расскажи', '', text)
        text = re.sub('скажи', '', text)
        text = re.sub('квартиру', '', text)
        text = re.sub('квартира', '', text)
        text = re.sub('жилье', '', text)
        text = re.sub('жильё', '', text)
        text = re.sub(' на ', ' ', text)
        text = re.sub(' за ', ' ', text)
        text = re.sub('первичный', ' ', text)
        text = re.sub('первичного', ' ', text)
        text = re.sub('ипотеку', ' ', text)
        text = re.sub('ипотека', ' ', text)
        text = re.sub('б у', 'вторичка', text)

        text = text.strip(' ')

        return text


def diction_form(text):
        text = ''.join(m.lemmatize(text)).rstrip('\n')
        return text

slovar = {
    0:"Ставка будет от 10.5 % ",
    1:"Взнос будет от 0 %",
    2:"Ставка на вторичное жилье будет от 10.5 %",
    3:"Взнос за вторичное жильё будет от 0 %",
    4:"ставка и взнос будут от 10.5 % и 0 % соответсвенно",
    5:"ставска и взнос бу будут от 10.5 % и 0 % соответсвенно",
    6:"ставка и взнос будут от 5.3 % от 15 % ",
    7:"ставка и взнос будут от 6.3 % от 15 % седьмое",
    8:"ставка и взнос будут от 4.7 % от 15 % иit",
    9:"ставка и взнос будут от 5.3 % от 15 % два документа",
    10:"ставка и взнос будут от 1.5 % от 15 % дальний восток",
    11:"ставка и взнос по молодежной ипотеке будут от 10.5 % от 0.1 %",
    12:"ставка и взнос на военной ипотеке будут от 9.9 % от 15 %"
    }


@bot.message_handler(func=lambda message: True)
async def echo_message(message):
        global model
        message_text = clean_text(message.text)
        message_text = diction_form(message_text)

        prediction = model.predict([message_text])
        print("Сделали предсказание")

        await bot.send_message(message.chat.id, str(slovar[prediction[0]]))


if __name__ == "__main__":   
        print("Bot is running...")
   
        asyncio.run(bot.polling())