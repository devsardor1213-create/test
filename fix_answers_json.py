import json
import re

# User provided corrections
updates = {
    # 29
    "Nоminаl YAMM qаndаy usul bilаn rеаl YAMMgа аylаntirilаdi?": "Nominal YAMM ni narx indeksi (deflyator) ga bo‘lish orqali.",
    # 31
    "Sоliqlаr tushunchаsining mаzmuni qаysi bаnddа to‘g‘ri ko‘rsаtilgаn?": "majburiy ravishda budjetga undiriladigan to‘lovlar.",
    # 33
    "Ekstensiv iqtisоdiy o‘sishgа qаndаy erishilаdi?": "ishlab chiqarish omillari miqdorini ko‘paytirish hisobiga.",
    # 40 (already correct but we'll ensure exact match)
    "Ssuda, qarz olish maqsadida ko‘chmas mulkni garovga qo‘yish orqali qarz olish qaysi termin bilan izohlanadi?": "ipoteka.",
    # 43
    "Tranfеrt to‘lovlar, bu:": "aholiga yoki tashkilotlarga evazsiz beriladigan to‘lovlar (pensiya, stipendiya, nafaqa va h.k.).",
    # 44
    "Quyidagi ko‘rsatkichlardan qaysi biri xarajatlar yig‘indisi ko‘rinishida hisoblangan YaIM tarkibiga kirmaydi?": "transfer to‘lovlar (davlat xarajatlari esa YaIM tarkibiga kiradi).",
    # 46
    "Filips egri chizig‘i:": "ishsizlik va inflyatsiya o‘rtasidagi teskari bog‘liqlik.",
    # 47
    "AD egri chizig‘ining chap va o‘ng tomonga suriladi baholar darajasiga ta'sir etmaydi, agar:": "iqtisodiyot to‘liq bandlikdan uzoqda bo‘lsa (gorizontal Keynes kesimida).",
    # 48
    "Yalpi taklifning klassik modеlida:": "ish haqi va baholar o‘zgaruvchan, real YaIM esa to‘liq bandlik darajasida doimiy.",
    # 49
    "Davlat xarajatlarining o‘sishi natijasida uzoq muddatda ishlab chiqarish va narxlar darajasi qanday o‘zgaradi?": "narxlar oshadi, real ishlab chiqarish hajmi esa uzoq muddatda deyarli o‘zgarmaydi.",
    # 50
    "Umumiy makroiqtisodiy muvozanat-bu:": "barcha asosiy bozorlar (tovar, mehnat, pul va boshqalar) bir vaqtning o‘zida muvozanatda bo‘lishi."
}

def normalize(text):
    return re.sub(r'\s+', ' ', text.lower().replace("‘", "'").replace("'", "").replace('"', '').strip())

def main():
    try:
        with open('special_questions.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        updated_count = 0
        for q in data:
            q_text = q['question']
            q_norm = normalize(q_text)
            
            for key, new_correct in updates.items():
                if normalize(key) == q_norm or normalize(key) in q_norm:
                    correct_idx = q['correct_index']
                    q['options'][correct_idx] = new_correct
                    updated_count += 1
                    break
                    
            # Handle question 28 manually to ensure "talab"
            if "tovarni sotib olish" in q_norm and "imkoniyat" in q_norm:
                q['options'][q['correct_index']] = "talab"
                updated_count += 1
                
        with open('special_questions.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"Muvaffaqiyatli! {updated_count} ta savolning javoblari siz aytgandek to'g'rilandi.")
        
    except Exception as e:
        print(f"Xatolik: {e}")

if __name__ == '__main__':
    main()
