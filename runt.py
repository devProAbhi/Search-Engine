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
            document_full = document+line
            processed_text = preprocess_text(document_full)
            documents.append(processed_text)
    print("Done.")
    return documents, names, indexes