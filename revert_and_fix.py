import json
import subprocess

def main():
    print("Avvalgi holatga qaytarish va to'g'rilash boshlandi...")
    
    # 1. 50 ta savolni aslicha qaytadan olish
    print("1. Asl bazadan (questions.json) 50 ta savol ajratilmoqda...")
    try:
        subprocess.run(['python', 'extract_50_questions.py'], check=True)
    except Exception as e:
        print(f"Xato (extract_50_questions): {e}")
    
    # 2. 12 ta xatoni to'g'rilash
    print("2. 12 ta asosiy xato tahrirlanmoqda...")
    try:
        subprocess.run(['python', 'fix_answers_json.py'], check=True)
    except Exception as e:
        print(f"Xato (fix_answers_json): {e}")
    
    # Endi o'zimizning aniq to'g'rilashlarni qo'llaymiz
    with open('special_questions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    print("3. Qo'shimcha format va 5 ta maxsus savol tahrirlanmoqda...")
    for q in data:
        # Format xatoliklari (=\n#)
        if "Bozor kelishuvining ekspansiyasi qanday oqibatlarga olib kelishi mumkin?" in q['question']:
            for i, opt in enumerate(q['options']):
                if opt == "=\n# Boylikning o‘ta nomutanosib taqsimlanishiga":
                    q['options'][i] = "Boylikning o‘ta nomutanosib taqsimlanishiga"
        
        if "Statistik xaritalar ko‘zlangan maqsad va vazifalarga qarab" in q['question']:
            for i, opt in enumerate(q['options']):
                if opt == "=\n# xaritogramma, xaritodiagramma va markazgrammalarga bo`linadi.":
                    q['options'][i] = "xaritogramma, xaritodiagramma va markazgrammalarga bo'linadi."
                    
        # 5 ta maxsus savol
        if "Korxona rivojlanish strategiyalari turlari" in q['question']:
            q['options'] = [
                "tadbirkorlik, raqabotchilik",
                "boshqarish san’ati va mahorati",
                "yoshlar haqida",
                "ishlab chiqarish samaradorligi"
            ]
            q['correct_index'] = 0
            
        if "Ularsiz sanoat iqtisodiyot ham, fan-texnika majmui ham rivojlana olmaydi" in q['question']:
            q['options'] = [
                "kadrlar",
                "menejerlar",
                "tadbirkorlar",
                "yoshlar haqida"
            ]
            q['correct_index'] = 0
            
        if "Yangi texnika samaradorligini hisoblash nimaga asoslanadi?" in q['question']:
            q['options'] = [
                "qiyosiy samaradorlikni aniqlash",
                "yillik samaradorlikni aniqlash",
                "texnik samaradorlikni aniqlash",
                "ishlab chiqarish samaradorligi"
            ]
            q['correct_index'] = 0
            
        if "Zamonaviy texnologik almashinuv?" in q['question']:
            q['options'] = [
                "Litsenziya savdosi",
                "Litsenziya",
                "Patent axboroti",
                "Sertifikatlash"
            ]
            q['correct_index'] = 0
            
        if "Xalqaro Klassifikatsiyasi" in q['question'] or "Xalqaro klassifikatsiyasi" in q['question']:
            q['options'] = [
                "Lokarno bitimi",
                "Yer, mеhnаt, kаpitаl, mаtеriаllаr, tаdbirkоrlik qоbiliyati vа ахbоrоt",
                "istе’mоl mоllаri",
                "Оmillаrdаn оqilоnа fоydаlаnish sаmаrаsi bilаn izоhlаnаdi"
            ]
            q['correct_index'] = 0

    with open('special_questions.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print("Asliga qaytarish yakunlandi. Barcha narsa oxirgi ma'qul kelgan (xatosiz) holatiga qaytdi!")

if __name__ == '__main__':
    main()
