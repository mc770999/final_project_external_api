import os

def get_counter(file_path=r"C:\Users\menac\OneDrive\Desktop\final_project_files\extenal\final_project_external_api\app\asset\counter.txt"):
    # Check if the file exists
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                return int(file.read().strip())
            except ValueError:
                return 0
    return 0

def increment_counter(file_path=r"C:\Users\menac\OneDrive\Desktop\final_project_files\extenal\final_project_external_api\app\asset\counter.txt"):
    counter = get_counter(file_path) + 1
    with open(file_path, "w") as file:
        file.write(str(counter))
    return counter

