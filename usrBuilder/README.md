# Sanskrit USR Generation from Parsed Morphological Output

This tool generates Sanskrit USR (Universal Semantic Representation) from parsed Sanskrit morphological output.

## Prerequisites

- Python 3.x must be installed
- Parsed Sanskrit files must be available in a single folder

---

## Step 1: Convert Parsed Files to JSON

Convert individual parsed Sanskrit files into a consolidated JSON file.

### Usage

```
python3 Convert_to_JSON.py <folder_name>
```
- <folder_name> should be the path to the folder containing all individual parsed Sanskrit files.

## Step 1: Generate the Sanskrit USR

Once the JSON is created, generate the Sanskrit USR.

### Usage

```
python3 main.py
```
- The output USR will be saved in the IO/ directory as USR_output.txt

## Output

- Location: IO/generated_USR.txt
- Format: Text file containing the generated Sanskrit USR.

## Notes

- Ensure that input files are in the correct format expected by the parser.

- For examples or formatting guidelines, refer to the documentation or sample input files on the SKT eReaders GitHub repository.