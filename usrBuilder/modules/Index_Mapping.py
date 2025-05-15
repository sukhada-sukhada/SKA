import re

def map_indices_by_sentences(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    result = []
    index_map = {}
    counter = 1

    float_index_pattern = re.compile(r"\b(\d+\.\d+)(:\S+)?\b")

    def process_sentence(sentence_lines):
        nonlocal counter
        index_map.clear()
        counter = 1
        updated_lines = []

        # Step 1: Collect all float indices
        all_indices = set()
        for line in sentence_lines:
            for match in float_index_pattern.finditer(line):
                float_id = match.group(1)
                all_indices.add(float_id)

        # Step 2: Map each unique float ID to int
        for float_id in sorted(all_indices, key=lambda x: tuple(map(int, x.split(".")))):
            index_map[float_id] = str(counter)
            counter += 1

        # Step 3: Replace all float IDs in all columns
        for line in sentence_lines:
            if line.strip() == "" or line.startswith("#") or line.startswith("<sent_id=") or line.strip() == "affirmative":
                updated_lines.append(line)
                continue

            # Replace float IDs with mapped int IDs, preserving optional labels
            def replace_match(m):
                float_id = m.group(1)
                label = m.group(2) if m.group(2) else ""
                return index_map.get(float_id, float_id) + label

            new_line = float_index_pattern.sub(replace_match, line)
            updated_lines.append(new_line)

        return updated_lines

    # Process sentences separated by <sent_id=...>
    temp_sent_lines = []
    for line in lines:
        if line.startswith("<sent_id="):
            if temp_sent_lines:
                result.extend(process_sentence(temp_sent_lines))
                temp_sent_lines = []
            result.append(line)
        else:
            temp_sent_lines.append(line)

    if temp_sent_lines:
        result.extend(process_sentence(temp_sent_lines))

    return result

# Example usage
file_path = "IO/cxn_output.txt"
mapped_output = map_indices_by_sentences(file_path)

with open("IO/mapped_index_output.txt", "w", encoding='utf-8') as f:
    f.writelines(mapped_output)
