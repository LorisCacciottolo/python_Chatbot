import math
import os
import re
from src.calculate_tf import calculate_tf
from src.calculate_idf import calculate_idf


class TFIDFProcessor:
    # @staticmethod
    # The @staticmethod decorator indicates that this method is a static method of the class.
    # This means the method can be called on the class itself, without needing an instance of the class.


    def __init__(self, directory):
        self.directory = directory
        self.tfidf_corpus = self.calculate_tfidf_matrix()

    @staticmethod
    def question_tokenisation(question):
        question = question.lower()
        # Removes all apostrophes and characters following them within words.
        question = re.sub(r"\w[’']", '', question)
        # Replaces hyphens with spaces to avoid concatenation of words.
        question = re.sub(r"-", ' ', question)
        # Removes all characters except word characters (letters and numbers) and whitespace.
        question = re.sub(r"[^\w\s]", '', question)
        # Replaces multiple whitespace characters with a single space and trims leading/trailing spaces.
        question = re.sub(r"\s+", ' ', question).strip()
        return question

    def calculate_idf_question(self, question):
        idf_dict = {}
        total_documents = len(os.listdir(self.directory))
        print(self.directory)
        word_document_count = {}

        # Iterates through each file in the directory.
        for file in os.listdir(self.directory):
            with open(f"{self.directory}/{file}", 'r', encoding='utf-8') as file:
                # Creates sets of unique words from both the file and the question.
                content = set(file.read().split())
                content_question = set(question.split())
                # Counts the number of documents in which each word in the question appears (Tf).
                for word in content:
                    if word in content_question:
                        word_document_count[word] = word_document_count.get(word, 0) + 1

        # Calculates IDF for each word in the question.
        for word, count in word_document_count.items():
            idf_dict[word] = math.log10(total_documents / count)

        # Ensures all words in the question have an IDF value, assigning 0 if not present in the IDF dictionary.
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
        # Calculates IDF values
        idf_dict = calculate_idf(self.directory)
        tfidf_matrix = {}

        # Iterates over files in the directory.
        for file in os.listdir(self.directory):
            file_path = f"{self.directory}/{file}"
            # Reads each file and calculates its TF values.
            with open(file_path, 'r', encoding='utf-8') as file:
                tf_dict = calculate_tf(file.read())
                tfidf_vector = {}
                # Calculates TF-IDF value for each word in the file.
                for word, tf in tf_dict.items():
                    tfidf_vector[word] = tf * idf_dict.get(word, 0)
                # Adds the file's TF-IDF vector to the matrix.
                tfidf_matrix[file_path] = tfidf_vector

        return tfidf_matrix

    def find_most_relevant_document(self, tfidf_question):
        max_similarity = -1
        most_relevant_document_name = None

        # Iterates over each document's TF-IDF vector in the corpus.
        for doc_name, tfidf_vector in self.tfidf_corpus.items():
            # Calculates cosine similarity between the question's TF-IDF and the document's TF-IDF.
            similarity = TFIDFProcessor.cosine_similarity(tfidf_question, tfidf_vector)
            # Updates the most relevant document if a higher similarity score is found.
            if similarity > max_similarity:
                max_similarity = similarity
                most_relevant_document_name = doc_name

        if most_relevant_document_name:
            return most_relevant_document_name.replace("cleaned", "speeches")
        else:
            return "No relevant document found"

    @staticmethod
    def find_highest_tfidf_word(tfidf_vector, document_path):
        # Sorts the TF-IDF vector in descending order by TF-IDF value.
        sorted_tfidf = sorted(tfidf_vector.items(), key=lambda item: item[1], reverse=True)

        with open(document_path.replace("speeches","cleaned"), 'r', encoding='utf-8') as file:
            document_content = file.read().split()

        # Iterates over the sorted TF-IDF vector to find the highest scoring word present in the document.
        for word, _ in sorted_tfidf:
            if word in document_content:
                return word

        return None

    @staticmethod
    def extract_sentence_with_word(document_path, word):
        # Opens the document
        with open(document_path, 'r', encoding='utf-8') as file:
            text = file.read()
            # Splits the text into sentences
            sentences = text.split(".")
            for sentence in sentences:
                if word in sentence.lower():
                    return sentence.strip() + '.'
        return "Le mot n'a pas été trouvé dans le document."


# Call all function for test and debug
processor = TFIDFProcessor("cleaned")
question = "Peux-tu me dire comment une nation peut-elle prendre soin du climat ?" # Exemple question
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

