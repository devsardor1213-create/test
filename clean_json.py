import json

clean_questions = [
    "Ifodalanishiga ko‘ra bir-biridan mazmunan farq qiladigan guruhlash belgisi nima deyiladi?",
    "Guruhlashtirishda dastlab nimalar aniqlanadi?",
    "Agar taklif noelastik bo‘lib, tovarga bo‘lgan talab kamaysa, sotuvchining daromadi qanday o‘zgaradi?",
    "Bozor iqtisodiyoti normalari yig‘indisini nima tashkil etadi?",
    "Murakkab foyda ko‘rish normasi nima uchun zarur?",
    "Bozor iqtisodiyotining asosiy normasi qanday?",
    "Buyruqbozlik iqtisodiyotida foyda ko‘rish normasi qanday?",
    "Qonunga ishonch va bo‘ysunish normasi nima bilan bog‘liq?",
    "Bozor kelishuvining ekspansiyasi qanday oqibatlarga olib kelishi mumkin?",
    "Siyosat qanday jarayon hisoblanadi?",
    "Statistik ko‘rsatkich deb nimaga aytiladi?",
    "Nisbiy miqdorlar deb nimaga aytiladi?",
    "Tasodifiy tanlash deb nimaga aytiladi?",
    "Grafiklarning asosiy turi nima?",
    "Statistik xaritalar ko‘zlangan maqsad va vazifalarga qarab necha turga bo‘linadi?",
    "Korxona rivojlanish strategiyalari turlari qaysilar?",
    "Menejment nima?",
    "\"Ularsiz sanoat iqtisodiyoti ham, fan-texnika majmui ham rivojlana olmaydi.\" Gap kimlar haqida ketmoqda?",
    "Yangi texnika samaradorligini hisoblash nimaga asoslanadi?",
    "Ishlab chiqarish xarajatlari nima?",
    "Zamonaviy texnologik almashinuv nima?",
    "Sanoat namunalari xalqaro klassifikatsiyasini ta’sis etish to‘g‘risidagi qonun qaysi?",
    "Iqtisodiy resurslar to‘liq ko‘rsatilgan qatorni belgilang.",
    "Ishlab chiqarish resursi hisoblanmaydigan qatorni belgilang.",
    "Iste’molchilarning arzon narxlarda aynan bir mahsulotdan ko‘proq xarid etishga moyilligi nima bilan izohlanadi?",
    "Maksimal foydani ko‘zlayotgan firma qachon qo‘shimcha ishchilarni yollaydi?",
    "Monopol hokimiyatda narx kim tomonidan belgilanadi?",
    "Qaysi ibora insonlarning biror bir tovarni sotib olish uchun imkoniyat va xohish borligini anglatadi?",
    "Nominal YAMM qanday usul bilan real YAMMga aylantiriladi?",
    "Budjet nima?",
    "Soliqlar tushunchasining mazmuni qaysi bandda to‘g‘ri ko‘rsatilgan?",
    "Shaxsiy iste’mol va jamg‘arma maqsadlarida foydalanish mumkin bo‘lgan daromad nima deyiladi?",
    "Ekstensiv iqtisodiy o‘sishga qanday erishiladi?",
    "Sof raqobatli tarmoqlarda baho nimaning ta’sirida shakllanadi?",
    "Stagnatsiya nima?",
    "Tovarlar, xizmatlar, mehnat va moliyaviy resurslarning milliy chegaradan tashqaridagi harakatiga xizmat qiluvchi muassasaviy tuzilmalar nima?",
    "Iqtisodiy g‘oyalarning vujudga kelishi, rivojlanishi, kurashi va almashinuvini qaysi fan o‘rganadi?",
    "Qadimgi Hindistondagi \"Manu qonunlari\"da nimalar aks etgan?",
    "Narx-navoning umumiy darajasi oshishi va pulning qadrsizlanishi qaysi termin bilan izohlanadi?",
    "Ssuda olish maqsadida ko‘chmas mulkni garovga qo‘yish orqali qarz olish qaysi termin bilan izohlanadi?",
    "Firma ishini bozor sharoitiga moslashtirishga qaratilgan maxsus faoliyat turi nima?",
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

cyrillic_to_latin = {
    'а': 'a', 'о': 'o', 'е': 'e', 'с': 'c', 'р': 'r', 'х': 'x', 'у': 'y', 'в': 'v', 'м': 'm', 
    'н': 'n', 'к': 'k', 'и': 'i', 'т': 't', 'ь': "'", 'ъ': "'", 'э': 'e', 'л': 'l'
}

def clean_text(text):
    for c, l in cyrillic_to_latin.items():
        text = text.replace(c, l)
    
    # Umumiy xatolar va g'alati belgilar
    text = text.replace('In son', 'Inson')
    text = text.replace('Yirik,o\'rta', 'Yirik, o\'rta')
    text = text.replace('koeffisientda,fоizda', 'koeffitsiyentda, foizda')
    text = text.replace('premоllida,prоdesimellida', 'promilleda, prodesimillada')
    return text.strip()

def main():
    try:
        with open('special_questions.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for i, q in enumerate(data):
            if i < len(clean_questions):
                # O'zingiz bergan grammatik to'g'ri savolni qo'yamiz
                q['question'] = clean_questions[i]
                
            for j in range(len(q['options'])):
                # Variantlarni kirill aralashmasidan va boshqa harf xatolaridan tozalaymiz
                q['options'][j] = clean_text(q['options'][j])
                
        with open('special_questions.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print("Muvaffaqiyatli! special_questions.json to'liq tozalandi, xatolar tuzatildi.")
        
    except Exception as e:
        print(f"Xatolik: {e}")

if __name__ == '__main__':
    main()
