def process_file_with_insertion(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    output_lines = []

    # Split into sentence blocks
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
        samuccita_map = {}       # {head_id: [dependent_line_indices]}
        relation_type_map = {}   # {head_id: 'conj' or 'disjunct'}
        conj_index_map = {}      # {head_id: conj_or_disjunct_id}
        used_indices = set()
        conj_counter = 1
        new_block = block.copy()

        # First pass: collect समुच्चितः / अन्यतरः relations and used indices
        for idx, line in enumerate(block):
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or stripped.startswith("<") or stripped.startswith("%"):
                continue
            parts = stripped.split('\t')
            if len(parts) >= 2:
                used_indices.add(parts[1])
            if len(parts) >= 9 and ':' in parts[8]:
                dep, rel = parts[8].split(':', 1)
                rel = rel.strip()
                if rel in ('समुच्चितः', 'समुच्चित', 'अन्यतरः'):
                    dep = dep.strip()
                    samuccita_map.setdefault(dep, []).append(idx)
                    relation_type_map[dep] = 'conj' if rel in ('समुच्चितः', 'समुच्चित') else 'disjunct'

        # Second pass: insert conj/disjunct lines
        for head_id in list(samuccita_map.keys()):
            if head_id in conj_index_map:
                continue

            # Collect all related indices: head + dependents
            related_indices = []
            for idx, line in enumerate(new_block):
                parts = line.strip().split('\t')
                if len(parts) >= 2 and (parts[1] == head_id or idx in samuccita_map[head_id]):
                    related_indices.append(idx)

            insert_after_idx = max(related_indices)

            # Generate unique conj/disjunct ID
            # if '.' in head_id:
            #     prefix, suffix = head_id.split('.')
            #     suffix = int(suffix)
            # else:
            #     prefix, suffix = head_id, 0

            if '.' in head_id:
                prefix, suffix = head_id.rsplit('.', 1)  # split only once, from the right
                try:
                    suffix = int(suffix)
                except ValueError:
                    suffix = 0  # fallback if suffix isn’t a number
            else:
                prefix, suffix = head_id, 0


            while True:
                suffix += 1
                new_conj_id = f"{prefix}.{suffix}"
                if new_conj_id not in used_indices:
                    used_indices.add(new_conj_id)
                    break

            # Determine whether to insert conj or disjunct
            label_type = relation_type_map.get(head_id, 'conj')
            conj_label = f"[{label_type}_{conj_counter}]"
            conj_counter += 1

            # Get deprel from head_id row
            conj_deprel = '-'
            for line in new_block:
                parts = line.strip().split('\t')
                if len(parts) >= 5 and parts[1] == head_id:
                    conj_deprel = parts[4]
                    break

            conj_line = f'{conj_label}\t{new_conj_id}\t-\t-\t{conj_deprel}\t-\t-\t-\t-'
            new_block.insert(insert_after_idx + 1, conj_line)
            conj_index_map[head_id] = new_conj_id

        # Third pass: assign opN relations
        op_counter_map = {}

        for head_id, dep_indices in samuccita_map.items():
            conj_id = conj_index_map.get(head_id, head_id)
            label_type = relation_type_map.get(head_id, 'conj')

            if head_id not in op_counter_map:
                op_counter_map[head_id] = 1

            related_indices = set(dep_indices)

            for idx, line in enumerate(new_block):
                parts = line.strip().split('\t')
                if len(parts) >= 2 and parts[1] == head_id:
                    related_indices.add(idx)

            for idx in sorted(related_indices):
                parts = new_block[idx].strip().split('\t')
                if len(parts) >= 9:
                    op_n = f"op{op_counter_map[head_id]}"
                    op_counter_map[head_id] += 1
                    parts[8] = f"{conj_id}:{op_n}"
                    parts[4] = '-'  # Remove old deprel
                    new_block[idx] = '\t'.join(parts)

        # Append final updated block to output
        output_lines.extend(line.rstrip('\n') for line in new_block)

    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in output_lines:
            f.write(line + '\n')


# Call the function with filenames
process_file_with_insertion('IO/complete_nc_output.txt', 'IO/final_cxn_output.txt')
