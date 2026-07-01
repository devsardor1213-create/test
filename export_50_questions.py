import json

def main():
    print("Savollar eksport qilinmoqda...")
    try:
        # JSON bazani o'qiymiz
        with open('special_questions.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        md_content = "# 50 ta Maxsus Savol va Ularning Javoblari\n\n"
        md_content += "Ushbu faylda barcha 50 ta savol, ularning variantlari va to'g'ri javoblari to'liq saqlangan.\n\n---\n\n"
        
        for i, q in enumerate(data, 1):
            md_content += f"### {i}-savol:\n**{q['question']}**\n\n"
            
            correct_idx = q['correct_index']
            
            # Variantlarni chiqaramiz
            for j, opt in enumerate(q['options']):
                letter = chr(65 + j) # A, B, C, D harflari
                if j == correct_idx:
                    md_content += f"- **{letter}) {opt}** ✅ *(To'g'ri javob)*\n"
                else:
                    md_content += f"- {letter}) {opt}\n"
                    
            md_content += "\n---\n\n"
            
        # Faylga saqlaymiz
        with open('50_savol_va_javoblar.md', 'w', encoding='utf-8') as f:
            f.write(md_content)
            
        print(f"Muvaffaqiyatli! Barcha {len(data)} ta savol '50_savol_va_javoblar.md' fayliga saqlandi.")
        
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")

if __name__ == '__main__':
    main()
