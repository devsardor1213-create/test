import json
import re

TARGET_QUESTIONS = [
    "Ifodalanishiga ko‘ra bir-biridan mazmunan farq qiladigan guruhlash belgisi",
    "Guruhlashtirishda dastlab quyidagilar aniqlanadi.",
    "Agar taklif noelastik bo‘lib, tovarga bo‘lgan talab kamaysa, sotuvchining daromadi:",
    "Bozor iqtisodiyoti normalari yig‘indisini nima tashkil etadi?",
    "Murakkab foyda ko‘rish normasi nima uchun zarur?",
    "Bozor iqtisodiyotining asosiy normasi qanday?",
    "Buyruqbozlik iqtisodiyotida foyda ko‘rish normasi qanday?",
    "Qonunga ishonch va bo‘ysunish normasi nima bilan bog‘liq?",
    "Bozor kelishuvining ekspansiyasi qanday oqibatlarga olib kelishi mumkin?",
    "Siyosat qanday jarayon hisoblanadi?",
    "Statistik ko‘rsatgich deb nimaga aytiladi?",
    "Nisbiy miqdorlar deb nimaga aytiladi?",
    "Tasodifiy tanlash deb nimaga aytiladi?",
    "Grafiklarning asosiy turi?",
    "Statistik xaritalar ko‘zlangan maqsad va vazifalarga qarab uch turga bo‘linadi. Ularning nomlarini toping.",
    "Korxona rivojlanish strategiyalari turlari?",
    "Menejment nima?",
    "Ularsiz sanoat iqtisodiyoti ham, fan-texnika majmui ham rivojlana olmaydi. Gap kimlar haqida ketmoqda?",
    "Yangi texnika samaradorligini hisoblash nimaga asoslanadi?",
    "Ishlab chiqarish xarajatlari bu nima?",
    "Zamonaviy texnologik almashinuv nima?",
    "Sanoat namunalari Xalqaro Klassifikatsiyasini ta’sis etish to‘g‘risidagi qonun qaysi?",
    "Iqtisodiy resurslar to‘liq ko‘rsatilgan qatorni belgilang.",
    "Ishlab chiqarish resursi hisoblanmaydigan qatorni belgilang.",
    "Iste’molchilarning arzon narxlarda aynan bir mahsulotdan ko‘proq xarid etishga moyilligi nima bilan izohlanadi?",
    "Maksimal foydani ko‘zlab harakat qilayotgan firma qo‘shimcha ishchilarni qachon yollaydi?",
    "Monopol hokimiyatda narx monopolist tomonidan qanday belgilanadi?",
    "Qaysi ibora insonlarning biror bir tovarni sotib olish uchun imkoniyat va xohishi borligini anglatadi?",
    "Nominal YAMM qanday usul bilan real YAMMga aylantiriladi?",
    "Budjet nima?",
    "Soliqlar tushunchasining mazmuni qaysi bandda to‘g‘ri ko‘rsatilgan?",
    "Shaxsiy iste’mol va jamg‘arma maqsadlarida foydalanish mumkin bo‘lgan daromad nima deyiladi?",
    "Ekstensiv iqtisodiy o‘sishga qanday erishiladi?",
    "Sof raqobatli tarmoqlarda baho nimaning ta’sirida shakllanadi?",
    "Stagnatsiya nima?",
    "Tovarlar, xizmatlar, mehnat va moliyaviy resurslarning milliy chegaradan tashqaridagi harakatiga xizmat qiluvchi muassasaviy tuzilmalar nima?",
    "Iqtisodiy g‘oyalarning vujudga kelishi, rivojlanishi, kurashi va almashinuvini qaysi fan o‘rganadi?",
    "Qadimgi Hindistondagi «Manu qonunlari»da nimalar aks etgan?",
    "Narx-navoning umumiy darajasi oshishi va pulning xarid qobiliyati pasayishi qaysi termin bilan izohlanadi?",
    "Ssuda olish maqsadida ko‘chmas mulkni garovga qo‘yish orqali qarz olish qaysi termin bilan izohlanadi?",
    "Firma ishini bozor sharoitiga moslashtirishga qaratilgan maxsus faoliyat turi qanday nomlanadi?",
    "Krepostnoylikning vujudga kelish sababi nima?",
    "Transfer to‘lovlar nima?",
    "Quyidagi ko‘rsatkichlardan qaysi biri xarajatlar yig‘indisi ko‘rinishida hisoblangan YaIM tarkibiga kirmaydi?",
    "Asosiy makroiqtisodiy ayniyat nimani anglatadi?",
    "Filips egri chizig‘i nimani ifodalaydi?",
    "AD egri chizig‘ining chap va o‘ng tomonga surilishi baholar darajasiga qachon ta’sir etmaydi?",
    "Yalpi taklifning klassik modelida nimalar o‘zgaruvchan hisoblanadi?",
    "Davlat xarajatlarining o‘sishi natijasida uzoq muddatda ishlab chiqarish va narxlar darajasi qanday o‘zgaradi?",
    "Umumiy makroiqtisodiy muvozanat nima?"
]

def normalize(text):
    text = text.lower().replace("‘", "'").replace("'", "").replace('"', '').strip()
    return re.sub(r'\s+', ' ', text)

def main():
    try:
        with open('savollar.txt', 'r', encoding='utf-8') as f:
            content = f.read()

        blocks = content.split('++++')
        parsed_q = []

        for block in blocks:
            if not block.strip(): continue
            parts = block.strip().split('====')
            if len(parts) > 1:
                question = parts[0].strip()
                correct_answer = None
                for opt in parts[1:]:
                    opt = opt.strip()
                    if opt.startswith('#'):
                        correct_answer = opt[1:].strip()
                        break
                
                parsed_q.append({
                    'question': question,
                    'correct_answer': correct_answer
                })

        results = []
        special_questions_with_answers = []
        
        for tq in TARGET_QUESTIONS:
            found = False
            for pq in parsed_q:
                if normalize(tq) in normalize(pq['question']) or normalize(pq['question']) in normalize(tq):
                    results.append({
                        'target': tq,
                        'question_in_txt': pq['question'],
                        'correct_answer': pq['correct_answer']
                    })
                    
                    # We also want to save a json file with options and answers if possible
                    # but for now, we just want to show the correct answers
                    
                    found = True
                    break
            if not found:
                results.append({
                    'target': tq,
                    'question_in_txt': "NOT FOUND",
                    'correct_answer': "NOT FOUND"
                })

        # output to markdown artifact
        md_content = "# 50 ta maxsus savol va ularning to'g'ri javoblari (savollar.txt asosida)\n\n"
        for i, r in enumerate(results, 1):
            md_content += f"**{i}. Savol:** {r['target']}\n"
            if r['question_in_txt'] != "NOT FOUND":
                md_content += f"> **To'g'ri javob:** {r['correct_answer']}\n\n"
            else:
                md_content += f"> **Diqqat: Ushbu savol savollar.txt dan topilmadi!**\n\n"

        with open('tekshiruv.md', 'w', encoding='utf-8') as f:
            f.write(md_content)
            
        print("Muvaffaqiyatli 'tekshiruv.md' fayli yaratildi.")

    except Exception as e:
        print(f"Xatolik: {e}")

if __name__ == '__main__':
    main()
