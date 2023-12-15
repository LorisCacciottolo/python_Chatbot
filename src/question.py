from calculate_tf import calculate_tf
import math
import os
import re


def question_tokenisation(question):
    question = question.lower()
    question = re.sub(r"\w[’']", '', question)
    question = re.sub(r"-", ' ', question)
    question = re.sub(r"[^\w\s]", '', question)
    question = re.sub(r"\s+", ' ', question).strip()
    return question


question = "Pourquoi Python ne marche pas!?"

question = question_tokenisation(question)

print(question)

tf_question = calculate_tf(question)
print(tf_question)


def calculate_idf(question, directory):
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

idf_question = calculate_idf(question, "cleaned")
print(idf_question)

def calculate_tfidf(question, calculate_tf, calculate_idf):
    tfidf_question = {}
    for word in question.split():
        tfidf = calculate_tf.get(word, 0) * calculate_idf.get(word, 0)
        if word not in tfidf_question:
            tfidf_question[word] = []
        tfidf_question[word].append(tfidf)
    return tfidf_question

tfidf_question = calculate_tfidf(question, tf_question, idf_question)
print(tfidf_question)