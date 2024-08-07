import json

def process_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    result = {}
    for key, value_list in data.items():
        words = []
        for item in value_list:
            word = item['word']
            if words and words[-1].endswith('-'):
                words[-1] = words[-1] + word
            else:
                words.append(word)
        result[key] = ' '.join(words)
    
    return result

file_path = 'combined_data.json'
result = process_json_file(file_path)

final_result = {}
for key, words in result.items():
    final_result[key] = {
        'original_sent': words,
    }

print(json.dumps(final_result, ensure_ascii=False, indent=4))
