import json, math, re, sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from constants.Named_Entity import NE_LIST, AVYA_LIST
from constants.Mapping import CONCEPT_MAP, MAIN_MAP, TAM_LIST
from constants.Discourse import DISCOURSE_PARTICLES_DEP
from constants.Number import NUMBER_MAP

# Load JSON from file
with open('IO/combined_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Write output to a file
with open('IO/raw_output.txt', 'w', encoding='utf-8') as out_file:
    for file_name, entries in data.items():
        out_file.write(f"<sent_id={file_name.strip('.csv')}>\n")

        # Build the sentence line with hyphenation logic
        sentence_parts = []
        for entry in entries:
            word = entry.get("word", "")
            if not word:
                continue
            if sentence_parts and sentence_parts[-1].endswith("-"):
                sentence_parts[-1] += word
            else:
                sentence_parts.append(word)
        sentence_line = ' '.join(sentence_parts)
        out_file.write(f"#{sentence_line}\n")

        # Collect discourse particle info: {head_id: particle_root}
        particle_map = {}
        for entry in entries:
            dep_rel = entry.get("dependency_relation")
            dep_head = entry.get("dependency_head")
           
            if dep_head is None or (isinstance(dep_head, float) and math.isnan(dep_head)):
                dep_head = 0
            if dep_rel is None or (isinstance(dep_rel, float) and math.isnan(dep_rel)):
                dep_rel = "main"
            
            if dep_rel in DISCOURSE_PARTICLES_DEP or (
                dep_rel in ['समुच्चय_द्योतकः', 'सुप्_समुच्चय_द्योतकः', 'घटक_द्योतकः'] and entry.get("root") == 'अपि') or (
                dep_rel == 'सम्बन्धः' and entry.get("is_indeclinable")
                ):
                particle_map[str(dep_head)] = entry.get("wx_root")


        
        sent_type = 'affirmative'
        has_abhihita_karm = has_abhihita_karta = has_kim = has_pratishedha = False
        # Process and write each word line
        for entry in entries:
            wx_root = entry.get("wx_root")
            anvaya_no = entry.get("anvaya_no")
            dep_rel = entry.get("dependency_relation")
            dep_head = entry.get("dependency_head")

            # Handle NaN or None for dep_rel and dep_head
            if dep_head is None or (isinstance(dep_head, float) and math.isnan(dep_head)):
                dep_head = 0
            if dep_rel is None or (isinstance(dep_rel, float) and math.isnan(dep_rel)):
                dep_rel = "main"

            if dep_rel == 'अभिहित_कर्ता':
                has_abhihita_karta = True
            if dep_rel == 'अभिहित_कर्म':
                has_abhihita_karm = True
            if dep_rel == 'प्रतिषेधः':
                has_pratishedha = True
            if wx_root == 'kim':
                has_kim = True
        
            if has_abhihita_karta and has_pratishedha:
                sent_type = 'negative'
            if has_abhihita_karta and has_kim:
                sent_type = 'interrogative'
            if has_abhihita_karta and 'लोट्' in entry.get("morph_in_context"):
                sent_type = 'imperative'
            if has_abhihita_karm:
                sent_type = 'pass_affirmative'
            if has_abhihita_karm and has_pratishedha:
                sent_type = 'pass_negative'
            if has_abhihita_karm and has_kim:
                sent_type = 'pass_interrogative'
            if has_abhihita_karm and 'लोट्' in entry.get("morph_in_context"):
                sent_type = 'pass_imperative'
            

            if (wx_root and wx_root != "-") and dep_rel not in AVYA_LIST:
                # Morphological features
                morph_flag = ""
                if entry.get('is_mawupa', False):
                    morph_flag = "mawupa"
                elif entry.get('is_causative', False):
                    morph_flag = "causative"
                elif "तरप्" in re.findall(r'\{(.*?)\}', entry.get("morph_in_context", "")):
                    morph_flag = 'compermore'
                elif "तमप्" in re.findall(r'\{(.*?)\}', entry.get("morph_in_context", "")):
                    morph_flag = 'comperless'
                else:
                    number = entry.get("number", "")
                    if number in ["NA", "sg"]:
                        morph_flag = "-"
                    else:
                        morph_flag = number if number else "-"

                sem_cat = '-'
                if wx_root in NE_LIST:
                    gender = entry.get("gender", "")
                    if gender:
                        sem_cat = f'per/{gender}'

                dep_rel_mapped = MAIN_MAP.get(dep_rel, dep_rel)
                if dep_rel_mapped == 'main':
                    dep_head = '0'

                morph_context = entry.get('morph_in_context', "")
                cleaned_wx_root = re.sub(r'\d+$', '', wx_root)

                # Determine speaker info
                if cleaned_wx_root in ["ewax", "ixam"]:
                    spk_info = "proximal"
                elif cleaned_wx_root in ["wax", "axas"]:
                    spk_info = "distal"
                else:
                    spk_info = "-"

                # Add particle root to spk_info if current word is particle_head
                particle_root = particle_map.get(str(anvaya_no))
                if particle_root:
                    spk_info = particle_root + '_1' if spk_info == '-' else f'{spk_info}/{particle_root}_1'

                final_wx_root = CONCEPT_MAP.get(cleaned_wx_root, cleaned_wx_root)
                if 'संख्येयम्' in morph_context:
                    final_wx_root = NUMBER_MAP.get(final_wx_root, final_wx_root)
                else:
                    if final_wx_root not in ('$wyax', '$yax'):
                        final_wx_root = re.sub(r'\(.*?\)', '', final_wx_root).strip('-')
                        for key in TAM_LIST:
                            if all(term in morph_context for term in key):
                                final_wx_root += f"_1-{TAM_LIST[key]}"
                                break
                        final_wx_root += "_1"

                if 'समुच्चितः' == str(dep_rel) or 'घटकः' == str(dep_rel) or 'अन्वाचितः' == str(dep_rel):
                    dep_info = '-'
                    cxn_info = f'{dep_head}:{dep_rel}'
                else:
                    dep_info = f'{dep_head}:{dep_rel_mapped}'
                    cxn_info = '-'

                out_file.write(
                    f"{final_wx_root}\t{anvaya_no}\t{sem_cat}\t{morph_flag}\t{dep_info}\t-\t{spk_info}\t-\t{cxn_info}\n"
                )

        out_file.write(f"%{sent_type}\n")
        out_file.write(f"</sent_id>\n\n")

