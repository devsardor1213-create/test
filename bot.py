import asyncio
import json
import random
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import PollType

logging.basicConfig(level=logging.INFO)

# --- DIQQAT: BOT TOKENINI SHU YERGA YOZING ---
TOKEN = "8001673740:AAF1tGGwN4Hm1D7h4nWdVOO7bUrvPBNxA7s"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Savollarni yuklash
try:
    with open("questions.json", "r", encoding="utf-8") as f:
        ALL_QUESTIONS = json.load(f)
except FileNotFoundError:
    ALL_QUESTIONS = []
    print("Xatolik: questions.json fayli topilmadi!")

# Savollarni 100 tadan bo'limlarga ajratish
SECTIONS = []
chunk_size = 100
for i in range(0, len(ALL_QUESTIONS), chunk_size):
    SECTIONS.append(ALL_QUESTIONS[i:i + chunk_size])

# Bo'limlarning nomlari (O'zingiz xohlagan nomlarni shu yerga yozib chiqing)
SECTION_NAMES = [
    "1-bo'lim (1-100 savollar)",
    "2-bo'lim (101-200 savollar)",
    "3-bo'lim (201-300 savollar)",
    "4-bo'lim (301-400 savollar)",
    "5-bo'lim (401-500 savollar)",
    "6-bo'lim (501-600 savollar)",
    "7-bo'lim (601-dan oxirigacha)"
]
SECTIONS = []
chunk_size = 100
for i in range(0, len(ALL_QUESTIONS), chunk_size):
    SECTIONS.append(ALL_QUESTIONS[i:i + chunk_size])

active_games = {} # Guruhlardagi o'yin holatini saqlash uchun

def get_start_keyboard(bot_username):
    bot_link = f"https://t.me/{bot_username}?startgroup=true"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Guruhga qo'shish ➕", url=bot_link)]
    ])
    return keyboard

def get_sections_keyboard():
    buttons = []
    for i in range(len(SECTIONS)):
        # Agar bizda nomlar ro'yxatida nom bo'lsa, o'shani oladi
        if i < len(SECTION_NAMES):
            btn_text = SECTION_NAMES[i]
        else:
            btn_text = f"{i+1}-bo'lim"
            
        # "to'liq sig'sin" deganingiz uchun har bir qatorga bittadan tugma qo'ydim
        buttons.append([InlineKeyboardButton(text=btn_text, callback_data=f"sec_{i}")])
        
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_ready_keyboard(players_count=0):
    text = f"Men tayyorman ✋ ({players_count})" if players_count > 0 else "Men tayyorman ✋"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text, callback_data="ready")],
        [InlineKeyboardButton(text="Boshlash 🚀", callback_data="start_game")],
        [InlineKeyboardButton(text="Bo'limni o'zgartirish 🗂", callback_data="change_section")]
    ])

@dp.message(Command("stop"))
async def stop_cmd(message: types.Message):
    chat_id = message.chat.id
    if chat_id in active_games and active_games[chat_id].get("is_running"):
        active_games[chat_id]["is_running"] = False
        task = active_games[chat_id].get("task")
        if task:
            task.cancel()
        active_games.pop(chat_id, None)
        await message.answer("O'yin to'xtatildi! Test o'tkazish uchun bo'limni tanlang:", reply_markup=get_sections_keyboard())
    else:
        await message.answer("Hozir hech qanday o'yin ketmayapti. Test o'tkazish uchun bo'limni tanlang:", reply_markup=get_sections_keyboard())

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Salom! Test o'tkazish uchun bo'limni tanlang:", reply_markup=get_sections_keyboard())

@dp.callback_query(F.data.startswith("sec_"))
async def section_callback(callback: types.CallbackQuery):
    section_idx = int(callback.data.split("_")[1])
    chat_id = callback.message.chat.id
    
    if chat_id in active_games and active_games[chat_id].get("is_running"):
        await callback.answer("O'yin allaqachon boshlangan! To'xtatish uchun /stop buyrug'ini bering.", show_alert=True)
        return
    
    questions_in_section = SECTIONS[section_idx]
    
    active_games[chat_id] = {
        "section_idx": section_idx,
        "players": set(),
        "questions": random.sample(questions_in_section, len(questions_in_section)), # Shu bo'limdagi hamma savol
        "scores": {},
        "is_running": False
    }
    
    try:
        await callback.message.edit_text(
            f"{section_idx + 1}-bo'lim bo'yicha test o'ynashga kim tayyor?",
            reply_markup=get_ready_keyboard(0)
        )
    except:
        await callback.message.delete()
        await callback.message.answer(
            f"{section_idx + 1}-bo'lim bo'yicha test o'ynashga kim tayyor?",
            reply_markup=get_ready_keyboard(0)
        )

@dp.callback_query(F.data == "change_section")
async def change_section_cb(callback: types.CallbackQuery):
    chat_id = callback.message.chat.id
    if chat_id in active_games:
        if active_games[chat_id]["is_running"]:
            await callback.answer("O'yin allaqachon boshlangan!", show_alert=True)
            return
        active_games.pop(chat_id, None)
        
    try:
        await callback.message.edit_text("Test o'tkazish uchun bo'limni tanlang:", reply_markup=get_sections_keyboard())
    except:
        await callback.message.delete()
        await callback.message.answer("Test o'tkazish uchun bo'limni tanlang:", reply_markup=get_sections_keyboard())

@dp.callback_query(F.data == "ready")
async def ready_callback(callback: types.CallbackQuery):
    chat_id = callback.message.chat.id
    if chat_id in active_games and not active_games[chat_id]["is_running"]:
        user_id = callback.from_user.id
        full_name = callback.from_user.full_name
        
        active_games[chat_id]["players"].add(user_id)
        if user_id not in active_games[chat_id]["scores"]:
            active_games[chat_id]["scores"][user_id] = {"name": full_name, "score": 0}
            
        await callback.answer("Siz ro'yxatdan o'tdingiz! O'yin boshlanishini kuting.", show_alert=False)
        
        players_count = len(active_games[chat_id]["players"])
        try:
            await callback.message.edit_reply_markup(reply_markup=get_ready_keyboard(players_count))
        except:
            pass 
    else:
        await callback.answer("O'yin topilmadi. Qayta bo'lim tanlang.", show_alert=True)

@dp.callback_query(F.data == "start_game")
async def start_game_cb(callback: types.CallbackQuery):
    chat_id = callback.message.chat.id
    if chat_id not in active_games or active_games[chat_id]["is_running"]:
        await callback.answer("O'yin allaqachon boshlangan!", show_alert=True)
        return
        
    if not active_games[chat_id]["players"]:
        await callback.answer("Hali hech kim tayyor emas!", show_alert=True)
        return

    active_games[chat_id]["is_running"] = True
    await callback.message.delete()
    
    asyncio.create_task(run_quiz(chat_id))
    await callback.answer("O'yin boshlandi!")

async def run_quiz(chat_id):
    game = active_games.get(chat_id)
    if not game:
        return
    game["task"] = asyncio.current_task()
    
    try:
        await bot.send_message(chat_id, "O'yin boshlandi! 🎉\nHar bir savolga javob berish uchun 25 soniya vaqt beriladi.")
        await asyncio.sleep(2)
        
        for i, q in enumerate(game["questions"], 1):
            # Javoblarni aralashtirish
            options_list = list(enumerate(q["options"]))
            random.shuffle(options_list)
            
            shuffled_options = [opt_text for idx, opt_text in options_list]
            correct_idx = next(idx for idx, (orig_idx, _) in enumerate(options_list) if orig_idx == q["correct_index"])
            
            question_text = f"{i}-savol: {q['question']}"
            if len(question_text) > 300:
                question_text = question_text[:297] + "..."
                
            poll_msg = await bot.send_poll(
                chat_id=chat_id,
                question=question_text,
                options=shuffled_options,
                type=PollType.QUIZ,
                correct_option_id=correct_idx,
                is_anonymous=False, 
                explanation="Telegramda to'g'ri javob topsangiz ekranda chiroyli emojilar o'zi chiqadi! 🎊",
                open_period=25 
            )
            
            game["current_poll_id"] = poll_msg.poll.id
            game["current_correct_id"] = correct_idx
            
            await asyncio.sleep(27)
            
        await finish_game(chat_id)
    except asyncio.CancelledError:
        pass

@dp.poll_answer()
async def handle_poll_answer(poll_answer: types.PollAnswer):
    for chat_id, game in active_games.items():
        if game.get("current_poll_id") == poll_answer.poll_id:
            user_id = poll_answer.user.id
            selected = poll_answer.option_ids[0]
            
            if user_id not in game["scores"]:
                game["scores"][user_id] = {"name": poll_answer.user.full_name, "score": 0}
                
            if selected == game["current_correct_id"]:
                game["scores"][user_id]["score"] += 1

async def finish_game(chat_id):
    game = active_games.pop(chat_id, None)
    if not game:
        return
        
    scores = game["scores"]
    if not scores:
        text = "O'yin tugadi. Hech kim to'g'ri javob topolmadi 😢"
    else:
        sorted_scores = sorted(scores.values(), key=lambda x: x["score"], reverse=True)
        text = "🏆 O'yin yakunlandi! Natijalar:\n\n"
        for i, s in enumerate(sorted_scores, 1):
            text += f"{i}. {s['name']} - {s['score']} ta to'g'ri\n"
            
    # Bo'limni indeksini saqlab olingan
    sec_idx = game["section_idx"]
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ayni bo'limni qayta o'ynash 🔄", callback_data=f"sec_{sec_idx}")],
        [InlineKeyboardButton(text="Boshqa bo'lim tanlash 🗂", callback_data="change_section")]
    ])
    
    await bot.send_message(chat_id, text, reply_markup=kb)

async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
