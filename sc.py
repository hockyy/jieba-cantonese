import json
import re
import ast

def has_cjk(text):
    return bool(re.search(r'[\u4e00-\u9fff]', text))

def map_pos_to_jieba(pos):
    pos_mapping = {
        '名詞': 'n',
        '動詞': 'v',
        '形容詞': 'a',
        '副詞': 'd',
        '語素': 'x',
        '語句': 'l',
        '詞綴': 'k',
        '介詞': 'p',
        '區別詞': 'b',
        '數詞': 'm',
        '連詞': 'c',
        '擬聲詞': 'o',
        '代詞': 'r',
        '助詞': 'u',
        '量詞': 'q',
        '感嘆詞': 'e',  # Added mapping for exclamation
        '其他': 'x',    # Map 'other' to 'x' (for miscellaneous)
        '---': 'x'      # Map '---' to 'x' as well
    }
    return pos_mapping.get(pos, None)

import ast

def load_pos_data(filename):
    pos_data = {}
    line_count = 0
    error_count = 0

import re
import ast

def load_pos_data(filename):
    pos_data = {}
    line_count = 0
    error_count = 0
    bracket_pattern = re.compile(r'\[(.*?)\]')

    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line_count += 1
            parts = line.strip().split(',', 1)
            if len(parts) >= 2:
                words = [w.strip() for w in parts[0].split('/')]
                pos_string = parts[1].strip()
                match = bracket_pattern.search(pos_string)
                if match:
                    pos_string = match.group(1)  # Extract content within brackets
                    try:
                        pos_list = ast.literal_eval(f"[{pos_string}]")
                        if isinstance(pos_list, list) and len(pos_list) > 0:
                            pos = pos_list[0]  # Take only the first POS tag
                            for word in words:
                                pos_data[word] = pos
                        else:
                            raise ValueError("POS data is not a valid list")
                    except (ValueError, SyntaxError) as e:
                        error_count += 1
                        if error_count <= 5:
                            print(words)
                            print(pos_string)
                            print(f"Error parsing POS in line {line_count}: {line.strip()}")
                else:
                    error_count += 1
                    if error_count <= 5:
                        print(f"Error: No brackets found in line {line_count}: {line.strip()}")
            else:
                error_count += 1
                if error_count <= 5:
                    print(f"Error splitting line {line_count}: {line.strip()}")
            
            if line_count <= 5 or line_count % 10000 == 0:
                print(f"Line {line_count}: {line.strip()}")
                
    print(f"Total lines in POS file: {line_count}")
    print(f"Total words in pos_data: {len(pos_data)}")
    print(f"Total errors: {error_count}")
    return pos_data

def create_jieba_dict(word_freq, pos_data):
    jieba_dict = []
    words_with_pos = 0
    words_without_pos = 0
    unmapped_pos = {}
    
    for word, freq in word_freq.items():
        if has_cjk(word):
            pos = pos_data.get(word)
            if pos:
                jieba_pos = map_pos_to_jieba(pos)
                if jieba_pos:
                    jieba_dict.append(f"{word} {freq} {jieba_pos}")
                    words_with_pos += 1
                else:
                    if pos not in unmapped_pos:
                        unmapped_pos[pos] = []
                    unmapped_pos[pos].append(word)
                    jieba_dict.append(f"{word} {freq}")
                    words_without_pos += 1
            else:
                jieba_dict.append(f"{word} {freq}")
                words_without_pos += 1

    print(f"Total words processed: {len(word_freq)}")
    print(f"Words with POS: {words_with_pos}")
    print(f"Words without POS: {words_without_pos}")
    
    print("\nUnmapped POS tags:")
    for pos, words in unmapped_pos.items():
        print(f"POS '{pos}': {len(words)} words (e.g., '{words[0]}')")

    # Print some sample entries from pos_data and word_freq
    print("\nSample entries from pos_data:")
    sample_entries = list(pos_data.items())[:5]
    for word, pos in sample_entries:
        print(f"{word}: {pos}")

    print("\nSample entries from word_freq:")
    sample_entries = list(word_freq.items())[:5]
    for word, freq in sample_entries:
        print(f"{word}: {freq}")

    return jieba_dict

def main():
    # Load JSON data
    with open('existingwordcount.json', 'r', encoding='utf-8') as f:
        word_freq = json.load(f)

    # Load POS data
    pos_data = load_pos_data('wordpos-1721333150.csv')

    # Create Jieba dictionary entries
    jieba_dict = create_jieba_dict(word_freq, pos_data)

    # Write Jieba dictionary to file
    with open('yue.jieba.txt', 'w', encoding='utf-8') as f:
        for entry in jieba_dict:
            f.write(entry + '\n')

    print("Jieba dictionary created successfully.")

if __name__ == "__main__":
    main()