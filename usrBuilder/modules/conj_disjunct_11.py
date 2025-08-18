# def process_file_with_insertion(filename):
#     with open(filename, 'r', encoding='utf-8') as f:
#         lines = f.readlines()

#     output_lines = []

#     # Split the input into sentence blocks
#     sentence_blocks = []
#     current_block = []

#     for line in lines:
#         if line.strip().startswith("<sent_id="):
#             if current_block:
#                 sentence_blocks.append(current_block)
#             current_block = [line]
#         else:
#             current_block.append(line)
#     if current_block:
#         sentence_blocks.append(current_block)

#     for block in sentence_blocks:
#         samuccita_map = {}    # {head_index: [line_idx1, line_idx2, ...]}
#         used_indices = set()
#         new_block = []
#         conj_index = 1

#         # First pass: gather समुच्चितः links and all used indices
#         for idx, line in enumerate(block):
#             stripped = line.strip()
#             if not stripped or stripped.startswith("#") or stripped.startswith("<") or stripped.startswith("%"):
#                 continue
#             parts = stripped.split('\t')
#             if len(parts) >= 2:
#                 used_indices.add(parts[1])
#             if len(parts) >= 9 and ':' in parts[8]:
#                 dep, rel = parts[8].split(':', 1)
#                 if rel.strip() == "समुच्चितः":
#                     samuccita_map.setdefault(dep.strip(), []).append(idx)

#         # Assign op1, op2,... for समुच्चितः relations
#         op_labels = {}   # {line_index: label}
#         op_count_map = {}  # {head_index: current_count}
#         for dep, idx_list in samuccita_map.items():
#             for i, line_idx in enumerate(idx_list):
#                 label = f"op{i + 1}"
#                 op_labels[line_idx] = label
#             op_count_map[dep] = len(idx_list)

#         # Second pass: assign op(N+1)... if any line's col 2 == head_index
#         for idx, line in enumerate(block):
#             stripped = line.strip()
#             if not stripped or stripped.startswith("#") or stripped.startswith("<") or stripped.startswith("%"):
#                 continue
#             parts = stripped.split('\t')
#             if len(parts) < 2:
#                 continue
#             current_id = parts[1]

#             if current_id in op_count_map:
#                 next_op = op_count_map[current_id] + 1
#                 label = f"op{next_op}"
#                 op_labels[idx] = label
#                 op_count_map[current_id] = next_op  # update count

#         # Third pass: apply replacements and insert conj lines
#         for idx, line in enumerate(block):
#             stripped = line.strip()
#             new_block.append(line.rstrip('\n'))

#             if not stripped or stripped.startswith("#") or stripped.startswith("<") or stripped.startswith("%"):
#                 continue

#             parts = stripped.split('\t')
#             if len(parts) < 2:
#                 continue

#             if idx in op_labels and len(parts) >= 9:
#                 if ':' in parts[8]:
#                     dep, _ = parts[8].split(':', 1)
#                     parts[8] = f"{dep}:{op_labels[idx]}"
#                 else:
#                     parts[8] = f"{parts[8]}:{op_labels[idx]}"
#                 new_block[-1] = '\t'.join(parts)

#             # Insert conj line if needed
#             if parts[1] in samuccita_map:
#                 base = parts[1]
#                 if '.' in base:
#                     prefix, suffix = base.split('.')
#                     suffix = int(suffix)
#                 else:
#                     prefix, suffix = base, 0

#                 while True:
#                     suffix += 1
#                     new_index = f"{prefix}.{suffix}"
#                     if new_index not in used_indices:
#                         used_indices.add(new_index)
#                         break

#                 conj_label = f"[conj_{conj_index}]"
#                 conj_index += 1
#                 new_line = f'{conj_label}\t{new_index}\t-\t-\t{parts[4]}\t-\t-\t-\t-'
#                 new_block.append(new_line)

#         output_lines.extend(new_block)

#     # Final output
#     for line in output_lines:
#         print(line)



def process_file_with_insertion(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    output_lines = []

    # Split the input into sentence blocks
    sentence_blocks = []
    current_block = []

    for line in lines:
        if line.strip().startswith("<sent_id="):
            if current_block:
                sentence_blocks.append(current_block)
            current_block = [line]
        else:
            current_block.append(line)
    if current_block:
        sentence_blocks.append(current_block)

    for block in sentence_blocks:
        samuccita_map = {}       # {head_index: [line_idx1, line_idx2, ...]}
        conj_index_map = {}      # {head_index: conj_id (e.g. 5.2)}
        used_indices = set()
        new_block = []
        conj_counter = 1

        # First pass: collect समुच्चितः links and all used indices
        for idx, line in enumerate(block):
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or stripped.startswith("<") or stripped.startswith("%"):
                continue
            parts = stripped.split('\t')
            if len(parts) >= 2:
                used_indices.add(parts[1])
            if len(parts) >= 9 and ':' in parts[8]:
                dep, rel = parts[8].split(':', 1)
                if rel.strip() == "समुच्चितः":
                    samuccita_map.setdefault(dep.strip(), []).append(idx)

        # Second pass: insert conj lines and update conj_index_map
        for idx, line in enumerate(block):
            stripped = line.strip()
            new_block.append(line.rstrip('\n'))

            if not stripped or stripped.startswith("#") or stripped.startswith("<") or stripped.startswith("%"):
                continue

            parts = stripped.split('\t')
            if len(parts) < 2:
                continue

            current_id = parts[1]
            if current_id in samuccita_map and current_id not in conj_index_map:
                # Create unique conj index
                if '.' in current_id:
                    prefix, suffix = current_id.split('.')
                    suffix = int(suffix)
                else:
                    prefix, suffix = current_id, 0

                while True:
                    suffix += 1
                    new_conj_id = f"{prefix}.{suffix}"
                    if new_conj_id not in used_indices:
                        used_indices.add(new_conj_id)
                        break

                conj_label = f"[conj_{conj_counter}]"
                conj_counter += 1
                conj_line = f'{conj_label}\t{new_conj_id}\t-\t-\t{parts[4]}\t-\t-\t-\t-'
                new_block.append(conj_line)
                conj_index_map[current_id] = new_conj_id

        # # Third pass: apply opN labels pointing to conj index
        # op_labels = {}  # {line_idx: new_relation}
        # for head_id, idx_list in samuccita_map.items():
        #     conj_id = conj_index_map.get(head_id, head_id)
        #     for i, line_idx in enumerate(idx_list):
        #         op_n = f"op{i + 1}"
        #         # Fetch original line
        #         line = block[line_idx]
        #         parts = line.strip().split('\t')
        #         if len(parts) >= 9:
        #             dep, _ = parts[8].split(':', 1)
        #             parts[8] = f"{conj_id}:{op_n}"
        #             new_block[line_idx] = '\t'.join(parts)

        # Third pass: apply opN labels pointing to conj index
        op_counter_map = {}  # For tracking op index per head
        for head_id, idx_list in samuccita_map.items():
            conj_id = conj_index_map.get(head_id, head_id)
            if head_id not in op_counter_map:
                op_counter_map[head_id] = 1

            # Gather all relevant line indices:
            related_indices = set(idx_list)

            for idx, line in enumerate(block):
                parts = line.strip().split('\t')
                if len(parts) >= 2 and parts[1] == head_id:
                    related_indices.add(idx)

            # Sort and relabel with opN
            for line_idx in sorted(related_indices):
                op_n = f"op{op_counter_map[head_id]}"
                op_counter_map[head_id] += 1

                line = block[line_idx]
                parts = line.strip().split('\t')
                if len(parts) >= 9:
                    parts[8] = f"{conj_id}:{op_n}"
                    parts[4] = '-'
                    new_block[line_idx] = '\t'.join(parts)

        output_lines.extend(new_block)

    # Final output
    for line in output_lines:
        print(line)

process_file_with_insertion('test.txt')


