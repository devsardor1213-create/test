import json
import re
import random

def normalize_text(text):
    # Remove leading numbers and punctuation like "1. ", "24. \t"
    text = re.sub(r'^\d+[\.\)\t\s]+', '', text)
    # Normalize apostrophes
    text = text.replace("‘", "'").replace("’", "'").replace("'", "'").replace('`', "'")
    return text.strip().lower()

def main():
    try:
        with open("questions.json", "r", encoding="utf-8") as f:
            all_questions = json.load(f)
            
        with open("special_questions.json", "r", encoding="utf-8") as f:
            special_questions = json.load(f)
            
        # Create a lookup dictionary for all questions
        lookup = {}
        for q in all_questions:
            q_text = normalize_text(q.get("question", ""))
            lookup[q_text] = q
            
        fixed_count = 0
        not_found = []
        
        for sq in special_questions:
            sq_text = normalize_text(sq.get("question", ""))
            
            match = lookup.get(sq_text)
            if not match:
                # Try finding by partial match
                for key, q in lookup.items():
                    if sq_text in key or key in sq_text:
                        match = q
                        break
                        
            if match:
                real_options = match.get("options", [])
                real_correct_idx = match.get("correct_index", 0)
                
                if not real_options:
                    continue
                    
                correct_answer_text = real_options[real_correct_idx]
                
                # Shuffle the options
                shuffled = real_options[:]
                random.shuffle(shuffled)
                new_correct_idx = shuffled.index(correct_answer_text)
                
                sq["options"] = shuffled
                sq["correct_index"] = new_correct_idx
                fixed_count += 1
            else:
                not_found.append(sq.get("question"))
                
        with open("special_questions.json", "w", encoding="utf-8") as f:
            json.dump(special_questions, f, ensure_ascii=False, indent=2)
            
        print(f"Muvaffaqiyatli to'g'rilandi: {fixed_count} ta savol.")
        if not_found:
            print("Quyidagi savollar questions.json dan topilmadi:")
            for nf in not_found:
                print(f" - {nf}")
                
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")

if __name__ == '__main__':
    main()
