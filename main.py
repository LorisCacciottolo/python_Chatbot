from flask import Flask, render_template, request, jsonify
from src.TFIDFProcessor import TFIDFProcessor

app = Flask(__name__)
processor = TFIDFProcessor("cleaned")

@app.route('/')
def chatbot_ui():
    return render_template('index.html')

@app.route('/process_question', methods=['POST'])
def process_question():
    data = request.json
    question = data['question']
    tokenized_question = processor.question_tokenisation(question)
    idf_question = processor.calculate_idf_question(tokenized_question)
    tfidf_question = processor.calculate_tfidf(tokenized_question, idf_question)
    most_relevant_doc = processor.find_most_relevant_document(tfidf_question)
    highest_tfidf_word = processor.find_highest_tfidf_word(tfidf_question, most_relevant_doc)
    sentence_with_word = processor.extract_sentence_with_word(most_relevant_doc, highest_tfidf_word)
    
    response = {
        "most_relevant_doc": most_relevant_doc,
        "highest_tfidf_word": highest_tfidf_word,
        "sentence_with_word": sentence_with_word
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)


