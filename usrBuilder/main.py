import subprocess

# List of script filenames in order
scripts = ["modules/JSON_to_USR.py", "modules/CXN_Module.py",
            "modules/Index_Mapping.py", "modules/Map_Concept_Cxn.py"]

for script in scripts:
    # print(f"Running {script}...")
    result = subprocess.run(["python3", script], capture_output=True, text=True)

    if result.stderr:
        print(f"Errors from {script}:\n{result.stderr}")

    if result.returncode != 0:
        print(f"{script} exited with an error. Stopping execution.")
        break
