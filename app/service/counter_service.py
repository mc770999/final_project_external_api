import os

def get_counter(file_path=r"C:\Users\770mc\PycharmProjects\final_project_data_engnir2\external_api\data\counter.txt"):
    # Check if the file exists
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                return int(file.read().strip())
            except ValueError:
                return 0
    return 0

def increment_counter(file_path=r"C:\Users\770mc\PycharmProjects\final_project_data_engnir2\external_api\data\counter.txt"):
    counter = get_counter(file_path) + 1
    with open(file_path, "w") as file:
        file.write(str(counter))
    return counter

