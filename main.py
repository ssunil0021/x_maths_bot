import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from database import Database
from keyboards import main_menu
from datetime import datetime

# Token aur Admin ID setup
TOKEN = "YOUR_BOT_TOKEN_HERE"
ADMIN_ID = 123456789  # Apni ID yahan daalein
bot = Bot(token=TOKEN)
dp = Dispatcher()
db = Database()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Welcome to 'You Know Mathematics'! 🎓\nMon, Wed, Fri ko naye questions milenge.", 
                         reply_markup=main_menu())

@dp.message(F.text == "Today’s Question")
async def show_today_question(message: types.Message):
    today = datetime.now().date()
    now_time = datetime.now().time()
    
    content = await db.get_content_by_date(today)
    
    if content:
        # Question PDF bhejien
        await message.answer_document(content['question_file_id'], 
                                     caption=f"📝 Concept: {content['concept_title']}")
        
        # Check karein agar shaam ke 7 baj chuke hain toh solution bhi dein
        if now_time.hour >= 19 and content['solution_file_id']:
            await message.answer_document(content['solution_file_id'], caption="✅ Solution for today's question.")
        elif now_time.hour < 19:
            await message.answer("⏳ Solution aaj shaam 7:00 bje add hoga.")
    else:
        await message.answer("Aaj koi naya question nahi hai. Agla question Mon/Wed/Fri ko aayega!")

async def main():
    await db.connect()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())