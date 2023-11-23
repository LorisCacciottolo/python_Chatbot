from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

with open('/speeches/Nomination_Chirac1.txt', 'r', encoding='utf-8') as file:
    text = file.read()
    documents = sent_tokenize(text, language='french')

tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

def get_most_similar_response(question, tfidf_matrix, vectorizer):
    question_tfidf = vectorizer.transform([question])
    cosine_similarities = cosine_similarity(question_tfidf, tfidf_matrix).flatten()
    most_similar_document_index = cosine_similarities.argsort()[-1]
    print(most_similar_document_index)
    return documents[most_similar_document_index]

example_question = "quesque le Général de Gaulle a t'il fondé"
most_similar_response = get_most_similar_response(example_question, tfidf_matrix, tfidf_vectorizer)

print(most_similar_response)
