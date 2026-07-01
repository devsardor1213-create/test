import json
import re
import string

def normalize(text):
    if not text: return ""
    text = text.lower().replace("‘", "'").replace("'", "").replace('"', '').replace('`', "'").replace('\n', ' ').strip()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return re.sub(r'\s+', ' ', text)

def main():
    print("Tekshiruv boshlandi. Iltimos kuting...")
    try:
        # 1. savollar.txt faylidan barcha savol va to'g'ri javoblarni yig'ib olamiz
        with open('savollar.txt', 'r', encoding='utf-8') as f:
            content = f.read()

        blocks = content.split('++++')
        txt_data = []

        for block in blocks:
            if not block.strip(): continue
            parts = block.strip().split('====')
            if len(parts) > 1:
                q_text = parts[0].strip()
                correct_opt = None
                for opt in parts[1:]:
                    if '#' in opt:
                        idx = opt.find('#')
                        correct_opt = opt[idx+1:].strip()
                        break
                
                if correct_opt:
                    txt_data.append({
                        'question': q_text,
                        'correct_answer': correct_opt
                    })

        # 2. JSON bazani o'qiymiz
        with open('special_questions.json', 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        errors = []
        
        # 3. Har bir savolni solishtiramiz
        for i, q in enumerate(json_data):
            q_norm = normalize(q['question'])
            
            matched_txt = None
            # Savolni matnli bazadan topamiz
            for tq in txt_data:
                tq_norm = normalize(tq['question'])
                if q_norm == tq_norm or q_norm in tq_norm or tq_norm in q_norm:
                    matched_txt = tq
                    break
            
            # Agar aniq topilmasa, dastlabki 30 ta harfi orqali topamiz
            if not matched_txt:
                for tq in txt_data:
                    tq_norm = normalize(tq['question'])
                    if len(q_norm) > 20 and q_norm[:20] == tq_norm[:20]:
                        matched_txt = tq
                        break

            if not matched_txt:
                continue
                
            txt_correct = matched_txt['correct_answer']
            if not txt_correct:
                continue
                
            current_correct_idx = q['correct_index']
            current_correct_text = q['options'][current_correct_idx]
            
            clean_txt_correct = txt_correct.strip()
            
            # Solishtirish
            if normalize(current_correct_text) != normalize(clean_txt_correct):
                found_in_options = False
                # Variantlar ichidan aniqrog'ini qidiramiz
                for opt_i, opt_text in enumerate(q['options']):
                    if normalize(opt_text) == normalize(clean_txt_correct):
                        q['correct_index'] = opt_i
                        q['options'][opt_i] = clean_txt_correct
                        found_in_options = True
                        break
                
                # Agar topilmasa, mavjud indeksdagi noto'g'ri javobni butunlay almashtiramiz
                if not found_in_options:
                    q['options'][current_correct_idx] = clean_txt_correct

                errors.append({
                    'q_num': i + 1,
                    'question': q['question'],
                    'current_ans': current_correct_text,
                    'correct_ans': clean_txt_correct,
                    'reason': "JSON dagi variant matni savollar.txt dagi (asl manba) to'g'ri variant matniga mos kelmadi yoki boshqa indeks belgilangan."
                })
            else:
                # Har ehtimolga qarshi, orqacha belgilarni tozalash (masalan =\n#)
                q['options'][current_correct_idx] = clean_txt_correct
                
        # 4. JSONni qayta saqlaymiz
        with open('special_questions.json', 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)

        # 5. Hisobotni markdown formatida yozamiz
        md = "# JSON Baza Tekshiruvi: Xatolar Hisoboti\n\n"
        if errors:
            for err in errors:
                md += f"### {err['q_num']}-savol\n"
                md += f"**Savol:** {err['question']}\n"
                md += f"- **Hozirgi javob:** {err['current_ans']}\n"
                md += f"- **To'g'ri javob:** {err['correct_ans']}\n"
                md += f"- **Nima uchun xato:** {err['reason']}\n\n"
                
            md += "\n> **✅ Barcha xatolar `special_questions.json` da avtomatik tuzatildi va `savollar.txt` bilan 100% bir xil qilindi!**\n"
        else:
            md += "Hech qanday xato topilmadi, tayyor baza `savollar.txt` bilan mukammal mos keladi!\n"
            
        with open('xatolar_hisoboti.md', 'w', encoding='utf-8') as f:
            f.write(md)
            
        print(f"Tekshiruv tugadi! Jami {len(errors)} ta savol savollar.txt ga asosan to'g'rilandi.")
        print("Batafsil xulosani 'xatolar_hisoboti.md' faylida ko'rishingiz mumkin.")

    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")

if __name__ == '__main__':
    main()
