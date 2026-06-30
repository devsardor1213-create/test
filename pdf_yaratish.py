import json
import re

def normalize_text(text):
    text = re.sub(r"['ʻ‘`’]", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    return text.lower()

# Botdagi bilan aynan bir xil kalit so'zlar (100% siz bergan ro'yxat)
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

try:
    with open("questions.json", "r", encoding="utf-8") as f:
        ALL_QUESTIONS = json.load(f)
except Exception:
    ALL_QUESTIONS = []
    print("questions.json topilmadi!")

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

# Aralashib ketmasligi uchun boshqa savollarni aralashtirmaymiz, faqat rasmdagilarini qoldiramiz.

html_content = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Maxsus 50 ta savol</title>
<style>
    body { font-family: Arial, sans-serif; padding: 20px; line-height: 1.6; max-width: 900px; margin: auto; }
    h2 { text-align: center; color: #333; border-bottom: 2px solid #ccc; padding-bottom: 10px; }
    .question-block { margin-bottom: 25px; page-break-inside: avoid; }
    .question { font-weight: bold; margin-bottom: 10px; font-size: 16px; }
    .options { margin-left: 20px; }
    .correct { color: #155724; background-color: #d4edda; border: 1px solid #c3e6cb; padding: 5px; border-radius: 4px; font-weight: bold; margin-bottom: 3px; }
    .incorrect { color: #721c24; background-color: #f8d7da; border: 1px solid #f5c6cb; padding: 5px; border-radius: 4px; margin-bottom: 3px; }
</style>
</head>
<body>
<h2>Maxsus 50 ta savol (Botdagi bilan aynan bir xil)</h2>
"""

for i, q in enumerate(special_questions, 1):
    html_content += f'<div class="question-block">'
    html_content += f'<div class="question">{i}. {q.get("question", "Savol matni yo\'q")}</div>'
    html_content += '<div class="options">'
    correct_idx = q.get("correct_index", 0)
    for j, opt in enumerate(q.get("options", [])):
        if j == correct_idx:
            html_content += f'<div class="correct">✔️ {opt}</div>'
        else:
            html_content += f'<div class="incorrect">❌ {opt}</div>'
    html_content += '</div></div>'

html_content += """
</body>
</html>
"""

with open("maxsus_50_savol.html", "w", encoding="utf-8") as f:
    f.write(html_content)

not_found = []
for kw in SPECIAL_KEYWORDS:
    found_this = False
    for q in special_questions:
        txt = normalize_text(q.get('question', '') + " " + " ".join(q.get('options', [])))
        if kw in txt:
            found_this = True
            break
    if not found_this:
        not_found.append(kw)

with open("not_found_keywords.txt", "w", encoding="utf-8") as f:
    f.write("\\n".join(not_found))

print(f"\\n--- NATIJA ---")
print(f"Topilgan va qo'shilgan maxsus savollar soni: {len(special_questions)} ta!")
print(f"Topilmagan savollar soni: {len(not_found)} ta. (Ular 'not_found_keywords.txt' ga yozildi)")
print("Muvaffaqiyatli! 'maxsus_50_savol.html' fayli yaratildi.")
print("Bu faylni ustiga ikki marta bosib brauzerda oching va Ctrl+P tugmasini bosib PDF qilib saqlab oling.\\n")
