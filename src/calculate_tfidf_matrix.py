import os
from calculate_tf import calculate_tf
from calculate_idf import calculate_idf

def calculate_tfidf_matrix(directory):
    idf_dict = calculate_idf(directory)
    tfidf_matrix = {}
    all_words = set()

    for file in os.listdir(directory):
        with open(f"{directory}/{file}", 'r', encoding='utf-8') as file:
            all_words.update(file.read().split())

    for file in os.listdir(directory):
        with open(f"{directory}/{file}", 'r', encoding='utf-8') as file:
            tf_dict = calculate_tf(file.read())
            for word in all_words:
                tfidf = tf_dict.get(word, 0) * idf_dict.get(word, 0)
                if word not in tfidf_matrix:
                    tfidf_matrix[word] = []
                tfidf_matrix[word].append(tfidf)

    return tfidf_matrix

if __name__ == '__main__':
    print(calculate_tfidf_matrix("cleaned"))