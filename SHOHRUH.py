import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from groq import Groq

logging.basicConfig(level=logging.INFO)





TOKEN = os.getenv("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")
GROQ_API_KEY = os.getenv("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")



bot = Bot(token=TOKEN)
dp = Dispatcher()
client = Groq(api_key=GROQ_API_KEY)
import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F, types
from groq import Groq

logging.basicConfig(level=logging.INFO)

# Telegram BotFather'dan olingan TOKEN va Groq API kaliti:
TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

bot = Bot(token=TOKEN)
dp = Dispatcher()
client = Groq(api_key=GROQ_API_KEY)
# Toshkentlik, ravon va tushunarli muloqot uchun yo'riqnoma (System Prompt)
BOT_UZGF_PROMPT = """
Sening isming bot_uzgf. Sen Toshkentlik xushmuomala, madaniyatli va samimiy yigitsan.
Qoidalar:
1. Har doim foydalanuvchiga "Siz" deb hurmat bilan, odaobiylik bilan murojaat qil.
2. Toshkent shevasiga xos samimiy va tushunarli uslubda (lekin nojo'ya ko'cha slangisiz) ravon va imlo xatolarisiz gapir.
3. Savollarga juda aniq, londa va tushunarli javob qaytar. Keraksiz va uzun gaplarni ishlatma.
4. Javoblaringda o'zbekona samimiy iboralardan o'rinli foydalan (masalan: "Xo'p bo meydimi", "Tushundim", "Mayli, siz aytganday bo'lsin", "Albatta").
"""

@dp.message(F.text == "/start")
async def start_cmd(message: types.Message):
    await message.answer("Assalomu alaykum! Men bot_uzgf bo'laman. Yaxshimisiz? Qanday yordam bera olaman?")

@dp.message(F.text)
async def handle_text_message(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": BOT_UZGF_PROMPT},
                {"role": "user", "content": message.text}
            ],
            model="qwen/qwen3.8-27b",
            max_tokens=150,
        )
        reply_text = chat_completion.choices[0].message.content
        await message.reply(reply_text)
    except Exception as e:
        print(f"XATOLIK: {e}")
        await message.reply(f"⚠️ Xatolik kodi:\n`{e}`", parse_mode="Markdown")

async def main():
    print(">>> BOT_UZGF ISHGA TUSHDI! <<<")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())