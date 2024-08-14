import json
from constants.mappedRel import RELATION_MAP  

def process_json_data(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    result = {}
    for filename, entries in data.items():
        dep_rel = []
        dependency_relations = []
        hyphen_count = 1

        for entry in entries:
            # Map the dependency_relation using RELATION_MAP
            mapped_relation = RELATION_MAP.get(entry['dependency_relation'], entry['dependency_relation'])

            if entry['wx_root'] != '-' and (not entry['is_indeclinable'] or entry['wx_root'] in ['yaxA', 'waxA']):
                # Combine dependency_head and the mapped_relation into a tuple
                dep_rel.append((entry['dependency_head'], mapped_relation))

                if entry['word'].endswith('-'):
                    # Combine hyphen_count and the mapped_relation into a tuple and append to dependency_relations
                    dependency_relations.append((str(hyphen_count), mapped_relation))
                    hyphen_count += 1

        # Append all dependency_relation values at the end of dep_rel
        dep_rel.extend(dependency_relations)

        # Index the concepts, using a string representation of the tuple as the value
        indexed_concepts = {f"{i+1}": f"{wx_root[0]}:{wx_root[1]}" for i, wx_root in enumerate(dep_rel)}
        
        result[filename] = indexed_concepts

    # Save the processed data to a new JSON file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)

    print(f"Processed data saved to ---> {output_file_path}")

# Example usage
input_file_path = 'jsonIO/combined_data.json'
output_file_path = 'jsonIO/depRel.json'
process_json_data(input_file_path, output_file_path)
