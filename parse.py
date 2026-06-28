import json
import re

def parse_questions():
    try:
        with open('savollar.txt', 'r', encoding='utf-8') as f:
            content = f.read()
            
        blocks = re.split(r'\+{4,}', content)
        
        questions = []
        
        for block in blocks:
            block = block.strip()
            if not block:
                continue
                
            parts = [p.strip() for p in block.split('====')]
            
            if len(parts) < 3:
                continue
                
            # Telegram quiz limits:
            # Question max 300 chars
            question = parts[0][:300]
            
            options = []
            correct_index = 0 # Default to first if not found
            
            for i in range(1, len(parts)):
                opt = parts[i]
                if not opt:
                    continue
                    
                if opt.startswith('#'):
                    correct_index = len(options)
                    opt = opt[1:].strip()
                
                # Option max 100 chars
                options.append(opt[:100])
                
            if 2 <= len(options) <= 10:
                questions.append({
                    "question": question,
                    "options": options,
                    "correct_index": correct_index
                })
                
        with open('questions.json', 'w', encoding='utf-8') as f:
            json.dump(questions, f, ensure_ascii=False, indent=2)
            
        print(f"Jami {len(questions)} ta savol muvaffaqiyatli saqlandi!")
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")

if __name__ == '__main__':
    parse_questions()
