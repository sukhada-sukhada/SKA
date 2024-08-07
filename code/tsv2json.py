# # import pandas as pd
# # import json
# # from constants.dropColumns import columns_to_drop

# # def convert_tsv_to_json(tsv_file_path, json_file_path):
# #     try:
# #         # Load the TSV file
# #         data = pd.read_csv(tsv_file_path, delimiter='\t', encoding='utf-8')

# #         # Drop rows where all elements are NaN
# #         data.dropna(how='all', inplace=True)

# #         # Process the 'kaaraka_sambandha' column
# #         for index, row in data.iterrows():
# #             if pd.notna(row['morph_in_context']):
# #                 root = row['morph_in_context'].split('{')[0].strip()
# #                 data.at[index, 'root'] = root
                
# #                 if 'पुं' in row['morph_in_context']:
# #                     data.at[index, 'gender'] = 'male'
# #                 elif 'स्त्री' in row['morph_in_context']:
# #                     data.at[index, 'gender'] = 'female'
# #                 elif 'नपुं' in row['morph_in_context']:
# #                     data.at[index, 'gender'] = 'NA'
# #                 else:
# #                     data.at[index, 'gender'] = 'NA'

# #                 if 'बहु' in row['morph_in_context']:
# #                     data.at[index, 'number'] = 'pl'
# #                 elif 'द्वि' in row['morph_in_context']:
# #                     data.at[index, 'number'] = 'dl'
# #                 elif 'एक' in row['morph_in_context']:
# #                     data.at[index, 'number'] = 'sg'
# #                 else:
# #                     data.at[index, 'number'] = 'NA'

# #                 if 'सर्वनाम' in row['morph_in_context']:
# #                     data.at[index, 'is_pronoun'] = True
# #                 else:
# #                     data.at[index, 'is_pronoun'] = False

# #                 if 'अव्य' in row['morph_in_context']:
# #                     data.at[index, 'is_indeclinable'] = True
# #                 else:
# #                     data.at[index, 'is_indeclinable'] = False

                
# #             else:
# #                 data.at[index, 'root'] = 'NA'
# #                 data.at[index, 'gender'] = 'NA'
# #                 data.at[index, 'number'] = 'NA'
# #                 data.at[index, 'person'] = 'NA'

# #             if pd.notna(row['kaaraka_sambandha']):
# #                 if ',' in row['kaaraka_sambandha']:
# #                     dep_rel = row['kaaraka_sambandha'].split(',', 1)[0]
# #                     dep_head = row['kaaraka_sambandha'].split(',', 1)[1]
# #                     data.at[index, 'dependency_relation'] = dep_rel.strip()
# #                     data.at[index, 'dependency_head'] = dep_head.strip()
# #                     if ';' in dep_head:
# #                         data.at[index, 'verb_type'] = dep_head.split(';')[1]
# #                         data.at[index, 'dependency_head'] = dep_head.split(';')[0]
# #                     else:
# #                         data.at[index, 'verb_type'] = 'NA'


        
# #         data.drop(columns=columns_to_drop, inplace=True, errors='ignore')

# #         # Convert the DataFrame to a list of dictionaries
# #         data_dict = data.to_dict(orient='records')

# #         # Save the data as a JSON file
# #         with open(json_file_path, 'w', encoding='utf-8') as json_file:
# #             json.dump(data_dict, json_file, ensure_ascii=False, indent=4)
            
# #         print(f"TSV file has been successfully converted to JSON file at {json_file_path}")
# #     except Exception as e:
# #         print(f"An error occurred: {e}")

# # # Define file paths
# # tsv_file_path = 'data/016_2.tsv'
# # json_file_path = 'modified.json'

# # # Convert TSV to JSON
# # convert_tsv_to_json(tsv_file_path, json_file_path)

# import os
# import pandas as pd
# import json
# from constants.dropColumns import columns_to_drop

# def convert_tsv_folder_to_json(folder_path, json_file_path):
#     try:
#         combined_data = {}

#         # Loop through each file in the folder
#         for filename in os.listdir(folder_path):
#             if filename.endswith(".tsv"):
#                 tsv_file_path = os.path.join(folder_path, filename)
                
                
#                 data = pd.read_csv(tsv_file_path, delimiter='\t', encoding='utf-8')
#                 data.dropna(how='all', inplace=True)

#                 for index, row in data.iterrows():
#                     if pd.notna(row['morph_in_context']):
#                         root = row['morph_in_context'].split('{')[0].strip()
#                         data.at[index, 'root'] = root
                        
#                         if 'पुं' in row['morph_in_context']:
#                             data.at[index, 'gender'] = 'male'
#                         elif 'स्त्री' in row['morph_in_context']:
#                             data.at[index, 'gender'] = 'female'
#                         elif 'नपुं' in row['morph_in_context']:
#                             data.at[index, 'gender'] = 'NA'
#                         else:
#                             data.at[index, 'gender'] = 'NA'

#                         if 'बहु' in row['morph_in_context']:
#                             data.at[index, 'number'] = 'pl'
#                         elif 'द्वि' in row['morph_in_context']:
#                             data.at[index, 'number'] = 'dl'
#                         elif 'एक' in row['morph_in_context']:
#                             data.at[index, 'number'] = 'sg'
#                         else:
#                             data.at[index, 'number'] = 'NA'

#                         if 'सर्वनाम' in row['morph_in_context']:
#                             data.at[index, 'is_pronoun'] = True
#                         else:
#                             data.at[index, 'is_pronoun'] = False

#                         if 'अव्य' in row['morph_in_context']:
#                             data.at[index, 'is_indeclinable'] = True
#                         else:
#                             data.at[index, 'is_indeclinable'] = False

#                     else:
#                         data.at[index, 'root'] = 'NA'
#                         data.at[index, 'gender'] = 'NA'
#                         data.at[index, 'number'] = 'NA'
#                         data.at[index, 'person'] = 'NA'

#                     if pd.notna(row['kaaraka_sambandha']):
#                         if ',' in row['kaaraka_sambandha']:
#                             dep_rel = row['kaaraka_sambandha'].split(',', 1)[0]
#                             dep_head = row['kaaraka_sambandha'].split(',', 1)[1]
#                             data.at[index, 'dependency_relation'] = dep_rel.strip()
#                             data.at[index, 'dependency_head'] = dep_head.strip()
#                             if ';' in dep_head:
#                                 data.at[index, 'verb_type'] = dep_head.split(';')[1]
#                                 data.at[index, 'dependency_head'] = dep_head.split(';')[0]
#                             else:
#                                 data.at[index, 'verb_type'] = 'NA'

#                 data.drop(columns=columns_to_drop, inplace=True, errors='ignore')

#                 # Convert the DataFrame to a list of dictionaries
#                 data_dict = data.to_dict(orient='records')

#                 # Store data with filename as the key
#                 combined_data[filename] = data_dict

#         # Save the combined data as a JSON file
#         with open(json_file_path, 'w', encoding='utf-8') as json_file:
#             json.dump(combined_data, json_file, ensure_ascii=False, indent=4)

#         print(f"TSV files have been successfully converted to JSON file at {json_file_path}")
#     except Exception as e:
#         print(f"An error occurred: {e}")


# folder_path = 'ramayana/'
# json_file_path = 'combined_data.json'

# convert_tsv_folder_to_json(folder_path, json_file_path)

import os
import pandas as pd
import json
from constants.dropColumns import columns_to_drop

def convert_tsv_folder_to_json(folder_path, json_file_path):
    try:
        combined_data = {}

        # List all TSV files in the folder
        filenames = [filename for filename in os.listdir(folder_path) if filename.endswith(".tsv")]
        
        # Sort filenames in ascending order
        filenames.sort()

        # Loop through each file in the sorted list
        for filename in filenames:
            tsv_file_path = os.path.join(folder_path, filename)
                
            data = pd.read_csv(tsv_file_path, delimiter='\t', encoding='utf-8')
            data.dropna(how='all', inplace=True)

            for index, row in data.iterrows():
                if pd.notna(row['morph_in_context']):
                    root = row['morph_in_context'].split('{')[0].strip()
                    data.at[index, 'root'] = root
                    
                    if 'पुं' in row['morph_in_context']:
                        data.at[index, 'gender'] = 'male'
                    elif 'स्त्री' in row['morph_in_context']:
                        data.at[index, 'gender'] = 'female'
                    elif 'नपुं' in row['morph_in_context']:
                        data.at[index, 'gender'] = 'NA'
                    else:
                        data.at[index, 'gender'] = 'NA'

                    if 'बहु' in row['morph_in_context']:
                        data.at[index, 'number'] = 'pl'
                    elif 'द्वि' in row['morph_in_context']:
                        data.at[index, 'number'] = 'dl'
                    elif 'एक' in row['morph_in_context']:
                        data.at[index, 'number'] = 'sg'
                    else:
                        data.at[index, 'number'] = 'NA'

                    if 'सर्वनाम' in row['morph_in_context']:
                        data.at[index, 'is_pronoun'] = True
                    else:
                        data.at[index, 'is_pronoun'] = False

                    if 'अव्य' in row['morph_in_context']:
                        data.at[index, 'is_indeclinable'] = True
                    else:
                        data.at[index, 'is_indeclinable'] = False

                else:
                    data.at[index, 'root'] = 'NA'
                    data.at[index, 'gender'] = 'NA'
                    data.at[index, 'number'] = 'NA'
                    data.at[index, 'person'] = 'NA'

                if pd.notna(row['kaaraka_sambandha']):
                    if ',' in row['kaaraka_sambandha']:
                        dep_rel = row['kaaraka_sambandha'].split(',', 1)[0]
                        dep_head = row['kaaraka_sambandha'].split(',', 1)[1]
                        data.at[index, 'dependency_relation'] = dep_rel.strip()
                        data.at[index, 'dependency_head'] = dep_head.strip()
                        if ';' in dep_head:
                            data.at[index, 'verb_type'] = dep_head.split(';')[1]
                            data.at[index, 'dependency_head'] = dep_head.split(';')[0]
                        else:
                            data.at[index, 'verb_type'] = 'NA'

            data.drop(columns=columns_to_drop, inplace=True, errors='ignore')

            # Convert the DataFrame to a list of dictionaries
            data_dict = data.to_dict(orient='records')

            # Store data with filename as the key
            combined_data[filename] = data_dict

        # Save the combined data as a JSON file
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(combined_data, json_file, ensure_ascii=False, indent=4)

        print(f"TSV files have been successfully converted to JSON file at {json_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

folder_path = 'ramayana/'
json_file_path = 'combined_data.json'

convert_tsv_folder_to_json(folder_path, json_file_path)
