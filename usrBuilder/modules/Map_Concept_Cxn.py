import re, sys, os
from wxconv import WXC
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from constants.Mapping import CXN_MAP, RELATION_MAP

wx = WXC(order='utf2wx')  # WX converter

def map_and_convert(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    updated_lines = []

    for line in lines:
        # Find all bracketed tags like [label_index]
        matches = re.findall(r'\[([^\]_]+)_(\d+)\]', line)

        for label, index in matches:
            original = f"[{label}_{index}]"
            if label in CXN_MAP:
                replacement = f"[{CXN_MAP[label]}_{index}]"
            else:
                wx_label = wx.convert(label.strip())
                replacement = f"[{wx_label}_{index}]"

            # Replace only the exact match
            line = line.replace(original, replacement)

        columns = line.strip().split('\t')
        if len(columns) >= 5:
            rel_col = columns[4]
            if ':' in rel_col:
                prefix, rel = rel_col.split(':', 1)
                rel = rel.strip()
                if rel in RELATION_MAP:
                    mapped_rel = RELATION_MAP[rel]
                    columns[4] = f"{prefix}:{mapped_rel}"
                    line = '\t'.join(columns) + '\n'

        updated_lines.append(line)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.writelines(updated_lines)

# Example usage
map_and_convert('IO/mapped_index_output.txt', 'IO/USR_output.txt')

