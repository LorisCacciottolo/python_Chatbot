from calculate_tf import calculate_tf
import math
import os

question = "Pourquoi python ne marche pas ?"

tf_question = calculate_tf(question)
print(tf_question)

def calculate_common_words(question, directory):
    idf_dict = {}
    total_documents = len(os.listdir(directory))
    word_document_count = {}

    for file in os.listdir(directory):
        with open(f"{directory}/{file}", 'r', encoding='utf-8') as file:
            content = set(file.read().split())
            content_question = set(question.split())
            for word in content:
                if word in content_question:
                    word_document_count[word] = word_document_count.get(word, 0) + 1

    for word, count in word_document_count.items():
        idf_dict[word] = math.log10(total_documents / count)

    for i in question.split():
        if i not in idf_dict:
            idf_dict[i] = 0

    return idf_dict


print(calculate_common_words(question, "../cleaned"))