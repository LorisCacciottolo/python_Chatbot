from calculate_tf import calculate_tf
from calculate_idf import calculate_idf
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


question = "europe"

question = question_tokenisation(question)

print(question)



def calculate_idf_question(question, directory):
    word_document_count = {}
    idf_corpus = calculate_idf(directory)
    print(idf_corpus)

    content_question = set(question.split())
    for word in content_question:
        if word in content_question:
            if word not in idf_corpus:
                word_document_count[word] = 0
            else:
                word_document_count[word] = idf_corpus[word]


    return word_document_count


idf_question = calculate_idf_question(question, "cleaned")
print("aaaa",idf_question)

def calculate_tfidf(question, calculate_idf):
    words_in_question = question.split()
    
    tfidf_question = {}
    for word in set(words_in_question):
        tf = words_in_question.count(word)
        idf = calculate_idf.get(word, 0)
        tfidf_question[word] = tf * idf

    return tfidf_question


tfidf_question = calculate_tfidf(question, idf_question)



def scalar_Product(A, B):
    return sum(A.get(word, 0) * B.get(word, 0) for word in set(A.keys()).intersection(B.keys()))


def norm_vector(A):
    return math.sqrt(sum(value**2 for value in A.values()))


def cosine_similarity(A,B):
    scalar_A_B = scalar_Product(A,B)
    NormA = norm_vector(A)
    NormB = norm_vector(B)
    if NormA == 0 or NormB == 0:
        return 0
    return (scalar_A_B)/(NormA * NormB)





def calculate_tfidf_matrix(directory):
    idf_dict = calculate_idf(directory)
    tfidf_matrix = {}

    for file in os.listdir(directory):
        file_path = f"{directory}/{file}"
        with open(file_path, 'r', encoding='utf-8') as file:
            tf_dict = calculate_tf(file.read())
            tfidf_vector = {}
            for word, tf in tf_dict.items():
                tfidf_vector[word] = tf * idf_dict.get(word, 0)
            tfidf_matrix[file_path] = tfidf_vector

    return tfidf_matrix


def find_most_relevant_document(tfidf_corpus, tfidf_question):
    max_similarity = -1
    most_relevant_document_name = None

    for doc_name, tfidf_vector in tfidf_corpus.items():
        similarity = cosine_similarity(tfidf_question, tfidf_vector)
        if similarity > max_similarity:
            max_similarity = similarity
            most_relevant_document_name = doc_name

    if most_relevant_document_name:
        return most_relevant_document_name.replace("cleaned", "speeches")
    else:
        return "No relevant document found"



tfidf_corpus = calculate_tfidf_matrix("cleaned")

print(tfidf_question)
most_relevant_doc = find_most_relevant_document(tfidf_corpus, tfidf_question)
print("Le document le plus pertinent est :", most_relevant_doc)



def find_highest_tfidf_word(tfidf_vector, document_path):
    sorted_tfidf = sorted(tfidf_vector.items(), key=lambda item: item[1], reverse=True)

    with open(document_path.replace("speeches","cleaned"), 'r', encoding='utf-8') as file:
        document_content = file.read().split()

    for word, _ in sorted_tfidf:
        if word in document_content:
            return word

    return None


def extract_sentence_with_word(document_path, word):
    with open(document_path, 'r', encoding='utf-8') as file:
        text = file.read()
        sentences = text.split(".")
        for sentence in sentences:
            if word in sentence.lower():
                return sentence.strip() + '.'
    return "Le mot n'a pas été trouvé dans le document."




highest_tfidf_word = find_highest_tfidf_word(tfidf_question, most_relevant_doc)
print("Mot ayant le TF-IDF le plus élevé :", highest_tfidf_word)


sentence_with_word = extract_sentence_with_word(most_relevant_doc, highest_tfidf_word)


print("Reponse :", sentence_with_word)
