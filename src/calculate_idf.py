import math
import os

def calculate_idf(directory):
    idf_dict = {}
    total_documents = len(os.listdir(directory))
    word_document_count = {}

    for file in os.listdir(directory):
        with open(f"{directory}/{file}", 'r', encoding='utf-8') as file:
            content = set(file.read().split())
            for word in content:
                word_document_count[word] = word_document_count.get(word, 0) + 1

    for word, count in word_document_count.items():
        idf_dict[word] = math.log10(total_documents / count)

    return idf_dict

if __name__ == '__main__':
    print(calculate_idf("cleaned"))