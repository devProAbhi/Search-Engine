import os
import linecache
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import string


def preprocess_text(text):
    # Remove punctuation and convert to lowercase
    text = text.translate(str.maketrans("", "", string.punctuation)).lower()
    # Tokenize the text
    words = word_tokenize(text)
    # Remove stop words
    stop_words = set(stopwords.words("english"))
    words = [word for word in words if word not in stop_words]
    # Perform stemming using Porter Stemmer
    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]
    # Reconstruct the preprocessed text from processed words
    processed_text = " ".join(words)
    return processed_text


def get_doc4mtxt(folder_path):
    documents = []
    names = []
    indexes = []
    print("processing.....")
    list = os.listdir(folder_path)
    list = [item for item in list if not item.startswith('.ipynb_checkpoints')]
    for filename in list:
        with open(os.path.join(folder_path, filename, filename+"a.txt"), "r", encoding="utf-8") as file:
            line = linecache.getline("links.txt", int(filename)).split(
                "m/problems/")[1].split("/")[0].strip()
            names.append(line)
            indexes.append(filename)
            document = file.read()
            document_full = " ".join([document, line])
            document_full = " ".join(document_full.split("\n"))
            pp_doc = preprocess_text(document_full)
            documents.append(pp_doc)
    print("Done.")
    return documents, names, indexes


    # Sample lists of strings
path = "qData"
list1, list2, list3 = get_doc4mtxt(path)

# Function to write a list to a text file


def write_list_to_file(list_data, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        for item in list_data:
            file.write(item + "\n")


# Name of the output text files
output_file1 = "documents.txt"
output_file2 = "names.txt"
output_file3 = "indexes.txt"

# Write each list to separate text files
write_list_to_file(list1, output_file1)
write_list_to_file(list2, output_file2)
write_list_to_file(list3, output_file3)

print(f"Text files created successfully.")
