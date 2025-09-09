# def process_dvandva_insertion(filepath):
#     with open(filepath, 'r', encoding='utf-8') as f:
#         lines = f.readlines()

#     result_lines = []
#     i = 0
#     insert_count = 0

#     while i < len(lines):
#         line = lines[i]

#         # Copy comments, markup, or empty lines directly
#         if line.startswith(("#", "<", "%")) or line.strip() == "":
#             result_lines.append(line)
#             i += 1
#             continue

#         cols = line.strip().split('\t')

#         if len(cols) > 4 and "द्वन्द्वः" in cols[4]:
#             # Start of a द्वन्द्वः group
#             dvandva_group = []
#             op_index = 1

#             group_start_index = i
#             while i < len(lines):
#                 current_line = lines[i]
#                 current_cols = current_line.strip().split('\t')

#                 if len(current_cols) > 4 and "द्वन्द्वः" in current_cols[4]:
#                     while len(current_cols) < 9:
#                         current_cols.append('-')
#                     current_cols[8] = f"?:op{op_index}"  # Temporary placeholder
#                     dvandva_group.append(current_cols)
#                     op_index += 1
#                     i += 1
#                 else:
#                     break

#             # If there's a line after the group, calculate insert_id from it
#             insert_id = "?.?"
#             if i < len(lines):
#                 next_line = lines[i]
#                 next_cols = next_line.strip().split('\t')
#                 insert_after_id = next_cols[1] if len(next_cols) > 1 else "?.?"
#                 try:
#                     insert_id_val = float(insert_after_id)
#                     insert_id = f"{insert_id_val + 0.1:.2f}"
#                 except:
#                     insert_id = "?.?"

#             # Now update insert IDs in the group
#             for j, row in enumerate(dvandva_group):
                
                
#                 dvandva_type = dvandva_group[-1][4].split(':')[1] if ':' in dvandva_group[-1][4] else dvandva_group[-1][4]
#                 fifth_col = next_cols[4] if len(next_cols) > 4 else "-"

#                 row[8] = f"{insert_id}:op{j+1}"
#                 row[4] = '-'
#                 result_lines.append('\t'.join(row) + '\n')

#             # Tag the next line if exists
#             if i < len(lines):
#                 next_cols = lines[i].strip().split('\t')
#                 while len(next_cols) < 9:
#                     next_cols.append('-')
#                 next_cols[8] = f"{insert_id}:op{op_index}"
#                 next_cols[4] = '-'
#                 result_lines.append('\t'.join(next_cols) + '\n')

                
#                 insert_count += 1
#                 result_lines.append(f"[{dvandva_type}_{insert_count}]\t{insert_id}\t-\t-\t{fifth_col}\t-\t-\t-\t-\n")
#                 i += 1

#         else:
#             result_lines.append(line)
#             i += 1

#     with open("processed_output.txt", "w", encoding="utf-8") as f:
#         f.writelines(result_lines)

#     print("✔ Output written to 'processed_output.txt'.")

# # Run the function
# process_dvandva_insertion('input.txt')


def process_block(lines):
    """Process lines of a single <sent_id> block with dvandva insertion logic."""
    result_lines = []
    i = 0
    insert_count = 0

    while i < len(lines):
        line = lines[i]

        # Copy comments, markup, or empty lines directly
        if line.startswith(("#", "<", "%")) or line.strip() == "":
            result_lines.append(line)
            i += 1
            continue

        cols = line.strip().split('\t')

        if len(cols) > 4 and "द्वन्द्वः" in cols[4]:
            # Start of a द्वन्द्वः group
            dvandva_group = []
            op_index = 1

            group_start_index = i
            while i < len(lines):
                current_line = lines[i]
                current_cols = current_line.strip().split('\t')

                if len(current_cols) > 4 and "द्वन्द्वः" in current_cols[4]:
                    while len(current_cols) < 9:
                        current_cols.append('-')
                    current_cols[8] = f"?:op{op_index}"  # Temporary placeholder
                    dvandva_group.append(current_cols)
                    op_index += 1
                    i += 1
                else:
                    break

            # If there's a line after the group, calculate insert_id from it
            insert_id = "?.?"
            if i < len(lines):
                next_line = lines[i]
                next_cols = next_line.strip().split('\t')
                insert_after_id = next_cols[1] if len(next_cols) > 1 else "?.?"
                try:
                    insert_id_val = float(insert_after_id)
                    insert_id = f"{insert_id_val + 0.1:.2f}"
                except:
                    insert_id = "?.?"

            # Now update insert IDs in the group
            for j, row in enumerate(dvandva_group):
                dvandva_type = dvandva_group[-1][4].split(':')[1] if ':' in dvandva_group[-1][4] else dvandva_group[-1][4]
                fifth_col = next_cols[4] if len(next_cols) > 4 else "-"

                row[8] = f"{insert_id}:op{j+1}"
                row[4] = '-'
                result_lines.append('\t'.join(row) + '\n')

            # Tag the next line if exists
            if i < len(lines):
                next_cols = lines[i].strip().split('\t')
                while len(next_cols) < 9:
                    next_cols.append('-')
                next_cols[8] = f"{insert_id}:op{op_index}"
                next_cols[4] = '-'
                result_lines.append('\t'.join(next_cols) + '\n')

                insert_count += 1
                result_lines.append(f"[{dvandva_type}_{insert_count}]\t{insert_id}\t-\t-\t{fifth_col}\t-\t-\t-\t-\n")
                i += 1

        else:
            result_lines.append(line)
            i += 1

    return result_lines


def process_dvandva_insertion(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    output_lines = []
    block_lines = []
    inside_sent_id = False

    for line in lines:
        if line.startswith('<sent_id='):
            # Starting a new block
            if inside_sent_id and block_lines:
                # Process previous block
                processed = process_block(block_lines)
                output_lines.extend(processed)
                block_lines = []

            inside_sent_id = True
            block_lines.append(line)

        elif line.startswith('</sent_id>'):
            # End of current block
            block_lines.append(line)
            if inside_sent_id:
                processed = process_block(block_lines)
                output_lines.extend(processed)
                block_lines = []
            inside_sent_id = False

        else:
            if inside_sent_id:
                block_lines.append(line)
            else:
                # Outside sent_id blocks, copy as is
                output_lines.append(line)

    # If file ends inside a sent_id block
    if inside_sent_id and block_lines:
        processed = process_block(block_lines)
        output_lines.extend(processed)

    with open("IO/Dvandva_nc_output.txt", "w", encoding="utf-8") as f:
        f.writelines(output_lines)

    print("✔ Output written to 'processed_output.txt'.")


# Run the function
process_dvandva_insertion('IO/raw_output.txt')
