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
TOKEN = "8448653743:AAElXteMA0bl5-ItsRP6Bdu1xl6NzRlEET4"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Savollarni yuklash
try:
    with open("questions.json", "r", encoding="utf-8") as f:
        ALL_QUESTIONS = json.load(f)
except Exception as e:
    ALL_QUESTIONS = []
    print(f"Xatolik: questions.json o'qilmadi! Sababi: {e}")

# --- MAXSUS 50 TALIK BO'LIMNI AJRATISH ---
import re
def normalize_text(text):
    text = re.sub(r"['ʻ‘`’]", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    return text.lower()

# Foydalanuvchi so'ragan maxsus savollarni topish uchun kalit so'zlar
SPECIAL_KEYWORDS = [
    "ifodalanishiga kora bir biridan mazmunan",
    "guruhlashtirishda dastlab quyidagilar aniqlanadi",
    "agar taklif noelastik bolib tovarga bolgan",
    "bozor iqtisodiyoti normalari yigindisini",
    "murakkab foyda korish normasi nima uchun",
    "bozor iqtisodiyotining asosiy normasi qanday",
    "buyruqbozlik iqtisodiyotida foyda korish",
    "qonunga ishonch va boysunish normasi",
    "bozor kelishuvining ekspansiyasi qanday",
    "siyosat qanday jarayon hisoblanadi",
    "statistik korsatgich deb nimaga aytiladi",
    "statistik korsatkich deb nimaga aytiladi",
    "nisbiy miqdorlar deb nimaga aytiladi",
    "tasodifiy tanlash deb nimaga aytiladi",
    "grafiklarning asosiy turi",
    "statistik xaritalar kozlangan maqsad",
    "korxona rivojlanish strategiyalari",
    "boshqarish sanati va mahorati",
    "ularsiz sanoat iqtisodiyot ham fan texnika",
    "yangi texnika samaradorligini hisoblash",
    "ishlab chiqarish xarajatlari bu",
    "zamonaviy texnologik almashinuv",
    "sanoat namualarining xalqaro klassifikatsiyasi",
    "iqtisodiy resurslar toliq korsatilgan",
    "ishlab chiqarish resursi hisoblanmaydigan",
    "istemolchilarning arzon narxlarda",
    "maksimal foydani kozlab harakat qilayotgan",
    "monopol hokimiyatda narx monopolist",
    "insonlarning biror bir tovarni sotib",
    "nominal yamm qanday usul bilan real",
    "budjet bu",
    "soliqlar tushunchasining mazmuni",
    "shaxsiy istemol va jamgarma maqsadlarida",
    "ekstensiv iqtisodiy osishga qanday erishiladi",
    "sof raqobatli tarmoqlarda baho nimaning",
    "stagnatsiya bu",
    "milliy chegaradan tashqaridagi harakatiga",
    "iqtisodiy goyalarni vujudga kelishi",
    "qadimgi hindistondagi manu qonunlarida",
    "narx navo umumiy darajasining oshishi",
    "kochmas mulkni garovga qoyish",
    "firma ishini bozor sharoitiga",
    "krepostnoylikning vujudga kelish",
    "tranfert tolovlar bu",
    "transfert tolovlar bu",
    "quyidagi korsatkichlardan qaysi biri xarajatlar",
    "asosiy makroiqtisodiy ayniyat anglatadi",
    "filips egri chizigi",
    "ad egri chizigining chap va ong",
    "yalpi taklifning klassik modelida",
    "davlat xarajatlarining osishi natijasida",
    "umumiy makroiqtisodiy muvozanat bu"
]

special_questions = []
other_questions = []

for q in ALL_QUESTIONS:
    text_to_search = normalize_text(q.get('question', '') + " " + " ".join(q.get('options', [])))
    found = False
    for kw in SPECIAL_KEYWORDS:
        if kw in text_to_search:
            found = True
            break
    if found and q not in special_questions:
        special_questions.append(q)
    else:
        if q not in special_questions:
            other_questions.append(q)

# Boshqa savollarni 50 taga to'ldirish uchun sun'iy aralashtirish olib tashlandi,
# faqat rasmdagi savollar chiqishi kafolatlandi.

print(f"\\n[INFO] Maxsus bo'lim uchun topilgan savollar soni: {len(special_questions)} ta\\n")

SECTION_NAMES = [
    f"⭐ Maxsus bo'lim ({len(special_questions)} ta savol)"
]

SECTIONS = [special_questions]

# Qolganlarini odatiy bo'limlarga bo'lamiz
chunk_size = 100
for i in range(0, len(other_questions), chunk_size):
    chunk = other_questions[i:i + chunk_size]
    SECTIONS.append(chunk)
    
# Bo'lim nomlarini to'ldirish
for i in range(1, len(SECTIONS)):
    start_idx = (i-1)*100 + 1
    end_idx = start_idx + len(SECTIONS[i]) - 1
    SECTION_NAMES.append(f"{i}-bo'lim ({start_idx}-{end_idx}-savollar)")

active_games = {} # Guruhlardagi o'yin holatini saqlash uchun

def get_start_keyboard(bot_username):
    bot_link = f"https://t.me/{bot_username}?startgroup=true"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Shaxsiy o'ynash 👤", callback_data="play_private")],
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
    if message.chat.type == "private":
        bot_info = await bot.get_me()
        await message.answer("Salom! Testni qayerda o'ynamoqchisiz?", reply_markup=get_start_keyboard(bot_info.username))
    else:
        await message.answer("Salom! Test o'tkazish uchun bo'limni tanlang:", reply_markup=get_sections_keyboard())

@dp.callback_query(F.data == "play_private")
async def play_private_cb(callback: types.CallbackQuery):
    if callback.message:
        await callback.message.edit_text("Test o'tkazish uchun bo'limni tanlang:", reply_markup=get_sections_keyboard())

@dp.callback_query(F.data.startswith("sec_"))
async def section_callback(callback: types.CallbackQuery):
    section_idx = int(callback.data.split("_")[1])
    
    if not callback.message:
        return
        
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
    except Exception:
        await callback.message.delete()
        await callback.message.answer(
            f"{section_idx + 1}-bo'lim bo'yicha test o'ynashga kim tayyor?",
            reply_markup=get_ready_keyboard(0)
        )

@dp.callback_query(F.data == "change_section")
async def change_section_cb(callback: types.CallbackQuery):
    if not callback.message:
        return
        
    chat_id = callback.message.chat.id
    if chat_id in active_games:
        if active_games[chat_id]["is_running"]:
            await callback.answer("O'yin allaqachon boshlangan!", show_alert=True)
            return
        active_games.pop(chat_id, None)
        
    try:
        await callback.message.edit_text("Test o'tkazish uchun bo'limni tanlang:", reply_markup=get_sections_keyboard())
    except Exception:
        await callback.message.delete()
        await callback.message.answer("Test o'tkazish uchun bo'limni tanlang:", reply_markup=get_sections_keyboard())

@dp.callback_query(F.data == "ready")
async def ready_callback(callback: types.CallbackQuery):
    if not callback.message:
        return
        
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
        except Exception:
            pass 
    else:
        await callback.answer("O'yin topilmadi. Qayta bo'lim tanlang.", show_alert=True)

@dp.callback_query(F.data == "start_game")
async def start_game_cb(callback: types.CallbackQuery):
    if not callback.message:
        return
        
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
            try:
                # Javoblarni aralashtirish
                options_list = list(enumerate(q["options"]))
                random.shuffle(options_list)
                
                shuffled_options = []
                for idx, opt_text in options_list:
                    opt_str = str(opt_text)
                    if len(opt_str) > 100:
                        opt_str = opt_str[:97] + "..."
                    shuffled_options.append(opt_str)
                
                # Variantlar takrorlanmasligini ta'minlash (Telegram talabi)
                seen = set()
                for j in range(len(shuffled_options)):
                    while shuffled_options[j] in seen:
                        # Agar takrorlansa, oxiriga bo'sh joy yoki belgi qo'shamiz
                        if len(shuffled_options[j]) < 100:
                            shuffled_options[j] += "\u200b" # zero-width space
                        else:
                            shuffled_options[j] = shuffled_options[j][:98] + str(random.randint(10, 99))
                    seen.add(shuffled_options[j])
                
                # Variantlar soni 2 tadan kam bo'lmasligi va 10 tadan oshmasligi kerak (Telegram talabi)
                while len(shuffled_options) < 2:
                    shuffled_options.append(f"Qo'shimcha javob {len(shuffled_options)}")
                if len(shuffled_options) > 10:
                    shuffled_options = shuffled_options[:10]

                correct_idx = next((idx for idx, (orig_idx, _) in enumerate(options_list) if orig_idx == q.get("correct_index", 0)), 0)
                
                default_q = "Savol matni yo'q"
                question_text = f"{i}-savol: {q.get('question', default_q)}"
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
            except asyncio.CancelledError:
                raise
            except Exception as e:
                logging.error(f"Savol yuborishda xatolik ({i}-savol): {e}")
                if "retry after" in str(e).lower():
                    # Agar rate limitga tushsa, 10 soniya kutib yana davom etamiz
                    await asyncio.sleep(10)
                else:
                    await bot.send_message(chat_id, f"⚠️ {i}-savolni yuborishda xatolik yuz berdi va o'tkazib yuborildi.")
                    await asyncio.sleep(2)
            
        await finish_game(chat_id)
    except asyncio.CancelledError:
        pass
    except Exception as e:
        logging.error(f"Quiz loop error: {e}")
        await finish_game(chat_id)

@dp.poll_answer()
async def handle_poll_answer(poll_answer: types.PollAnswer):
    if not poll_answer.option_ids:
        return # Foydalanuvchi javobni bekor qildi

    for chat_id, game in list(active_games.items()):
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
            line = f"{i}. {s['name']} - {s['score']} ta to'g'ri\n"
            if len(text) + len(line) > 4000:
                text += "\n... (qolganlar ko'rsatilmaydi)\n"
                break
            text += line
            
    # Bo'limni indeksini saqlab olingan
    sec_idx = game["section_idx"]
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ayni bo'limni qayta o'ynash 🔄", callback_data=f"sec_{sec_idx}")],
        [InlineKeyboardButton(text="Boshqa bo'lim tanlash 🗂", callback_data="change_section")]
    ])
    
    await bot.send_message(chat_id, text, reply_markup=kb)

async def main():
    print("Bot ishga tushdi...")
    while True:
        try:
            await dp.start_polling(bot)
        except Exception as e:
            logging.error(f"Bot ulanishda xatolik: {e}. 5 soniyadan so'ng qayta ulanadi...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
