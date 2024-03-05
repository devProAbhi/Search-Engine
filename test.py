import os

def get_files(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read().splitlines()
    return content

# Function to read text from file and convert to a list
def read_file_to_list(folder_path):
    # List all the text files in the folder
    all_lists=[]
    text_files = [file for file in os.listdir(folder_path) if file.endswith(".txt")]
    for file_name in text_files:
        file_path = os.path.join(folder_path, file_name)
        file_list = get_files(file_path)
        all_lists.append(file_list)
        print(file_name)
    return all_lists

# Folder path containing the text files
folder_path = "Lists Fol"

abhishek=read_file_to_list(folder_path)
