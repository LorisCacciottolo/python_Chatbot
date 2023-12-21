import math
import os

def calculate_idf(directory):
    idf_dict = {}
    total_documents = len(os.listdir(directory))
    word_document_count = {}

    # Iterate through the files in cleaned directory
    for file in os.listdir(directory):
        # Open the file for reading with UTF-8 encoding
        with open(f"{directory}/{file}", 'r', encoding='utf-8') as file:
            content = set(file.read().split())
            for word in content:
                word_document_count[word] = word_document_count.get(word, 0) + 1

    # Calculate the idf of every word with the formula
    for word, count in word_document_count.items():
        idf_dict[word] = math.log10(total_documents / (count + 1))

    return idf_dict

if __name__ == '__main__':
    print(calculate_idf("cleaned"))

