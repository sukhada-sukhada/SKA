import os
import re
import csv
from wxconv import WXC

# WX to Devanagari conversion using wxconv
def wx_to_devanagari(word):
    wxc = WXC()
    return wxc.convert(word)

# Load Devanagari → column2 mapping from CSV
def load_csv_words(csv_path):
    mapping = {}
    if not os.path.exists(csv_path):
        return mapping

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 4:
                dev_word = row[3].split('{')[0].strip()
                mapped_val = row[1].strip()  # 2nd column
                mapping[dev_word] = mapped_val
    return mapping

# Main function to process input file and lookup CSVs
def process_file(input_file, csv_folder):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    output_lines = []
    current_sent_id = None
    word_mappings = {}

    for line in lines:
        stripped = line.strip()

        # Handle <sent_id=...>
        if stripped.startswith("<sent_id="):
            match = re.search(r"<sent_id=(.*?)>", stripped)
            if match:
                current_sent_id = match.group(1)
                csv_path = os.path.join(csv_folder, f"{current_sent_id}.csv")
                word_mappings = load_csv_words(csv_path)
            output_lines.append(line)

        # Skip empty lines and metadata
        elif stripped == "" or stripped.startswith("#") or stripped.startswith("%"):
            output_lines.append(line)

        # Process token lines
        elif "\t" in line:
            columns = line.strip().split('\t')
            if columns:
                raw_word = columns[0]
                # Extract base WX word before first `_1`
                match = re.match(r"^(.*?)(?:_1.*)?$", raw_word)
                if match:
                    wx_word = match.group(1)
                    print(wx_word)
                    dev_word = wx_to_devanagari(wx_word)
                    print(dev_word)
                    mapped_val = word_mappings.get(dev_word, "_") 
                    columns.append(mapped_val)
                else:
                    columns.append("_")
                output_lines.append('\t'.join(columns))
        else:
            output_lines.append(line)

    # Print result (or write to file if needed)
    for line in output_lines:
        print(line)

# Example usage:
process_file('USR_output.txt', 'bAlakANda')
