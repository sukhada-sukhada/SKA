# import re

# def extract_and_check_duplicates(filename, output_filename):
#     in_block = False
#     updated_lines = []
#     insert_next = None  # Tuple: (dep_label, next_dep_ref, new_float_index)
#     float_index_counters = {}  # base -> next decimal to use

#     # First pass: determine existing float indices
#     with open(filename, 'r', encoding='utf-8') as file:
#         lines = file.readlines()

#     existing_indices = {}

#     float_index_pattern = re.compile(r'^.*?\t(\d+)\.(\d+)\t')

#     for line in lines:
#         match = float_index_pattern.match(line)
#         if match:
#             base = int(match.group(1))
#             decimal = int(match.group(2))
#             if base not in existing_indices or decimal > existing_indices[base]:
#                 existing_indices[base] = decimal

#     # Prepare counters from existing highest decimals
#     for base, max_decimal in existing_indices.items():
#         float_index_counters[base] = max_decimal + 1  # Start from next decimal

#     # Second pass: main logic
#     i = 0
#     while i < len(lines):
#         line = lines[i]
#         stripped_line = line.strip()

#         # Block start
#         if stripped_line.startswith('#'):
#             in_block = True
#             updated_lines.append(line)
#             i += 1
#             continue

#         # Block end
#         elif stripped_line.startswith('%'):
#             in_block = False
#             if insert_next:
#                 dep_label, next_dep_ref, new_float_index = insert_next
#                 inserted_line = f"{dep_label}\t{new_float_index}\t{next_dep_ref} <inserted>\t-\t-\n"
#                 updated_lines.append(inserted_line)
#                 insert_next = None
#             updated_lines.append(line)
#             i += 1
#             continue

#         # Add current line
#         updated_lines.append(line)

#         # Insert if scheduled
#         if insert_next:
#             dep_label, next_dep_ref, new_float_index = insert_next
#             inserted_line = f"[{dep_label}_1]\t{new_float_index}\t-\t-\t{next_dep_ref} <inserted>\t-\t-\n"
            
#             # Add "mod" to the previous-to-previous line
#             if len(updated_lines) >= 2:
#                 prev_line = updated_lines[-1].split('\t')
#                 prev_to_prev_line = updated_lines[-2].split('\t')
#                 updated_lines[-2] = '\t'.join(prev_to_prev_line[:4]) + f"\t-\t-\t-\t-\t{new_float_index}:mod\n"
#                 updated_lines[-1] = '\t'.join(prev_line[:4]) + f"\t-\t-\t-\t-\t{new_float_index}:head\n"
#             # updated_lines.append("head\n")
#             updated_lines.append(inserted_line)
#             insert_next = None

#         # Check for insertion opportunity
#         if in_block and stripped_line:
#             parts = stripped_line.split('\t')
#             if len(parts) >= 5:
#                 index_col = parts[1]
#                 dep_info = parts[4]
#                 if '.' in index_col and ':' in dep_info and '.' in dep_info.split(':')[0]:
#                     base_current = index_col.split('.')[0]
#                     base_dep = dep_info.split(':')[0].split('.')[0]
#                     if base_current == base_dep:
#                         dep_label = dep_info.split(':')[1]
#                         if i + 1 < len(lines):
#                             next_line = lines[i + 1].strip()
#                             next_parts = next_line.split('\t')
#                             if len(next_parts) >= 5:
#                                 next_dep_ref = next_parts[4]
#                                 try:
#                                     base_int = int(base_current)
#                                     if base_int not in float_index_counters:
#                                         float_index_counters[base_int] = 4  # fallback if not found in first pass
#                                     suffix = float_index_counters[base_int]
#                                     new_float_index = f"{base_int}.{suffix}"
#                                     float_index_counters[base_int] += 1
#                                     insert_next = (dep_label, next_dep_ref, new_float_index)
#                                 except ValueError:
#                                     pass
#         i += 1

#     # Write final result
#     with open(output_filename, 'w', encoding='utf-8') as out_file:
#         out_file.writelines(updated_lines)

# extract_and_check_duplicates('output1.txt', 'output1_modified.txt')


import re

def extract_and_check_duplicates(filename, output_filename):
    with open(filename, 'r', encoding='utf-8') as file:
        all_lines = file.readlines()

    updated_lines = []
    i = 0
    while i < len(all_lines):
        line = all_lines[i]

        # Start of a sentence block
        if line.startswith("<sent_id="):
            block_lines = [line]
            i += 1
            while i < len(all_lines) and not all_lines[i].startswith("</sent_id>"):
                block_lines.append(all_lines[i])
                i += 1
            if i < len(all_lines):
                block_lines.append(all_lines[i])  # Include </sent_id>
                i += 1

            # Process the block and add to output
            updated_block = process_sentence_block(block_lines)
            updated_lines.extend(updated_block)
        else:
            updated_lines.append(line)
            i += 1

    # Write to output
    with open(output_filename, 'w', encoding='utf-8') as out_file:
        out_file.writelines(updated_lines)


def process_sentence_block(lines):
    in_block = False
    updated_lines = []
    insert_next = None
    float_index_counters = {}
    dep_label_counters = {}

    float_index_pattern = re.compile(r'^.*?\t(\d+)\.(\d+)\t')
    existing_indices = {}

    # First pass: determine highest float index suffix per base
    for line in lines:
        match = float_index_pattern.match(line)
        if match:
            base = int(match.group(1))
            decimal = int(match.group(2))
            if base not in existing_indices or decimal > existing_indices[base]:
                existing_indices[base] = decimal

    for base, max_decimal in existing_indices.items():
        float_index_counters[base] = max_decimal + 1

    # Second pass
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped_line = line.strip()

        # Start sentence metadata or comment
        if stripped_line.startswith("#") or stripped_line.startswith("<sent_id="):
            in_block = True
            updated_lines.append(line)
            i += 1
            continue

        elif stripped_line.startswith("%"):
            in_block = False
            if insert_next:
                dep_label, next_dep_ref, new_float_index = insert_next
                count = dep_label_counters.get(dep_label, 0) + 1
                dep_label_counters[dep_label] = count
                dep_label_indexed = f"{dep_label}_{count}"
                inserted_line = f"[{dep_label_indexed}]\t{new_float_index}\t-\t-\t{next_dep_ref}\t-\t-\t-\t-\n"
                updated_lines.append(inserted_line)
                insert_next = None
            updated_lines.append(line)
            i += 1
            continue

        elif stripped_line.startswith("</sent_id>"):
            updated_lines.append(line)
            i += 1
            continue

        # Add normal line
        updated_lines.append(line)

        # Insert if scheduled
        if insert_next:
            dep_label, next_dep_ref, new_float_index = insert_next
            count = dep_label_counters.get(dep_label, 0) + 1
            dep_label_counters[dep_label] = count
            dep_label_indexed = f"{dep_label}_{count}"
            inserted_line = f"[{dep_label_indexed}]\t{new_float_index}\t-\t-\t{next_dep_ref}\t-\t-\t-\t-\n"

            if len(updated_lines) >= 2:
                prev_line = updated_lines[-1].split('\t')
                prev_to_prev_line = updated_lines[-2].split('\t')
                updated_lines[-2] = '\t'.join(prev_to_prev_line[:4]) + f"\t-\t-\t-\t-\t{new_float_index}:mod\n"
                updated_lines[-1] = '\t'.join(prev_line[:4]) + f"\t-\t-\t-\t-\t{new_float_index}:head\n"

            updated_lines.append(inserted_line)
            insert_next = None

        # Check insertion opportunity
        if in_block and stripped_line and '\t' in stripped_line:
            parts = stripped_line.split('\t')
            if len(parts) >= 5:
                index_col = parts[1]
                dep_info = parts[4]
                if '.' in index_col and ':' in dep_info and '.' in dep_info.split(':')[0]:
                    base_current = index_col.split('.')[0]
                    base_dep = dep_info.split(':')[0].split('.')[0]
                    if base_current == base_dep:
                        dep_label = dep_info.split(':')[1]
                        if i + 1 < len(lines):
                            next_line = lines[i + 1].strip()
                            next_parts = next_line.split('\t')
                            if len(next_parts) >= 5:
                                next_dep_ref = next_parts[4]
                                try:
                                    base_int = int(base_current)
                                    if base_int not in float_index_counters:
                                        float_index_counters[base_int] = 4
                                    suffix = float_index_counters[base_int]
                                    new_float_index = f"{base_int}.{suffix}"
                                    float_index_counters[base_int] += 1
                                    insert_next = (dep_label, next_dep_ref, new_float_index)
                                except ValueError:
                                    pass
        i += 1

    return updated_lines


# Example usage
extract_and_check_duplicates('IO/raw_output.txt', 'IO/output_with_cxn.txt')
