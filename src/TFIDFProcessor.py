import math
import os
import re
from src.calculate_tf import calculate_tf
from src.calculate_idf import calculate_idf

class TFIDFProcessor:

    def __init__(self, directory):
        self.directory = directory
        self.tfidf_corpus = self.calculate_tfidf_matrix()

    @staticmethod
    def question_tokenisation(question):
        question = question.lower()
        question = re.sub(r"\w[’']", '', question)
        question = re.sub(r"-", ' ', question)
        question = re.sub(r"[^\w\s]", '', question)
        question = re.sub(r"\s+", ' ', question).strip()
        return question

    def calculate_idf_question(self, question):
        idf_dict = {}
        total_documents = len(os.listdir(self.directory))
        print(self.directory)
        word_document_count = {}

        for file in os.listdir(self.directory):
            with open(f"{self.directory}/{file}", 'r', encoding='utf-8') as file:
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

    def calculate_tfidf(self, question, calculate_idf):
        words_in_question = question.split()
        total_words = len(words_in_question)
        
        tfidf_question = {}
        for word in set(words_in_question):
            tf = words_in_question.count(word) / total_words
            idf = calculate_idf.get(word, 0)
            tfidf_question[word] = tf * idf

        return tfidf_question
    
    @staticmethod
    def scalar_product(A, B):
        return sum(A.get(word, 0) * B.get(word, 0) for word in set(A.keys()).intersection(B.keys()))

    @staticmethod
    def norm_vector(A):
        return math.sqrt(sum(value**2 for value in A.values()))

    @staticmethod
    def cosine_similarity(A, B):
        scalar_A_B = TFIDFProcessor.scalar_product(A, B)
        NormA = TFIDFProcessor.norm_vector(A)
        NormB = TFIDFProcessor.norm_vector(B)
        if NormA == 0 or NormB == 0:
            return 0
        return (scalar_A_B) / (NormA * NormB)

    def calculate_tfidf_matrix(self):
        idf_dict = calculate_idf(self.directory)
        tfidf_matrix = {}

        for file in os.listdir(self.directory):
            file_path = f"{self.directory}/{file}"
            with open(file_path, 'r', encoding='utf-8') as file:
                tf_dict = calculate_tf(file.read())
                tfidf_vector = {}
                for word, tf in tf_dict.items():
                    tfidf_vector[word] = tf * idf_dict.get(word, 0)
                tfidf_matrix[file_path] = tfidf_vector

        return tfidf_matrix

    def find_most_relevant_document(self, tfidf_question):
        max_similarity = -1
        most_relevant_document_name = None

        for doc_name, tfidf_vector in self.tfidf_corpus.items():
            similarity = TFIDFProcessor.cosine_similarity(tfidf_question, tfidf_vector)
            if similarity > max_similarity:
                max_similarity = similarity
                most_relevant_document_name = doc_name

        if most_relevant_document_name:
            return most_relevant_document_name.replace("cleaned", "speeches")
        else:
            return "No relevant document found"

    @staticmethod
    def find_highest_tfidf_word(tfidf_vector, document_path):
        sorted_tfidf = sorted(tfidf_vector.items(), key=lambda item: item[1], reverse=True)

        with open(document_path, 'r', encoding='utf-8') as file:
            document_content = file.read().split()

        for word, _ in sorted_tfidf:
            if word in document_content:
                return word

        return None

    @staticmethod
    def extract_sentence_with_word(document_path, word):
        with open(document_path, 'r', encoding='utf-8') as file:
            text = file.read()
            sentences = text.split(".")
            for sentence in sentences:
                if word in sentence.split():
                    return sentence.strip() + '.'
        return "Le mot n'a pas été trouvé dans le document."


processor = TFIDFProcessor("cleaned")
question = "Peux-tu me dire comment une nation peut-elle prendre soin du climat ?"
tokenized_question = processor.question_tokenisation(question)
idf_question = processor.calculate_idf_question(tokenized_question)
tfidf_question = processor.calculate_tfidf(tokenized_question, idf_question)
most_relevant_doc = processor.find_most_relevant_document(tfidf_question)
highest_tfidf_word = processor.find_highest_tfidf_word(tfidf_question, most_relevant_doc)
sentence_with_word = processor.extract_sentence_with_word(most_relevant_doc, highest_tfidf_word)

print("Question tokenisée:", tokenized_question)
print("IDF de la question:", idf_question)
print("TFIDF de la question:", tfidf_question)
print("Le document le plus pertinent est:", most_relevant_doc)
print("Mot ayant le TF-IDF le plus élevé:", highest_tfidf_word)
print("Reponse:", sentence_with_word)
