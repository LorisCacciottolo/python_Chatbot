# python_Chatbot

[![GitHub Repo](https://img.shields.io/badge/Open-GitHub%20Repo-blue?logo=github)](https://github.com/LorisCacciottolo/python_Chatbot/tree/main)

## Table of Contents
- [Description](#description)
- [Installation](#installation)
- [Run Locally](#run-locally)
- [Testing Functionality](#testing-functionality)
- [Run Functions Separately](#run-functions-separately)
- [Features](#features)
- [Work Required](#work-required)
- [How to Contribute](#how-to-contribute)
- [License](#license)

## Description
The `python_Chatbot` project is designed to explore basic text processing concepts, focusing on methods used in developing chatbots and generative artificial intelligences. This project does not use neural networks but instead relies on analyzing word frequency in a corpus to generate intelligent responses.

## Installation
Clone the project with the following command:
```bash
git clone git@github.com:LorisCacciottolo/python_Chatbot.git
```

## Run Locally

Navigate to the project directory:

```bash
cd python_Chatbot
```

Install dependencies:

```bash
pip install -r requirements.txt
# or
pip3 install -r requirements.txt
```

Start the server (optional if you're only testing the features):

```bash
python main.py
# or
python3 main.py
```

## Testing Functionality

Test individual functions using a simple CLI:

```bash
python3 src/functionality.py
```

## Run Functions Separately

We've already explained how to run the web interface that simplifies the use of the program.
If you want to execute a different function you can use these commands

```bash
python3 src/name.py
python3 src/token.py
python3 src/calculate_idf.py
python3 src/calculate_tf.py
python3 src/calculate_tfidf_matrix.py
python3 src/TFIDFProcessor.py
```

- `name.py` = Lists the names of the presidents in the "speeches" folder.
- `token.py` = Cleans all texts in the "speeches" folder and writes them to the "cleaned" folder.
- `calculate_idf.py` = Calculates the IDF.
- `calculate_tf.py` = Calculates the TF.
- `calculate_tfidf_matrix.py`= Calculates the TF-IDF matrix.
- `TFIDFProcessor.py`= Generates the answer based on cleaned text.

## Features
- **Data Preprocessing**: Cleaning text by removing punctuation, converting to lowercase, and tokenizing.
- **TF-IDF Matrix Creation**: Calculating TF-IDF vectors for each unique word, creating a matrix where each row represents a word and each column a document.
- **Question Representation**: Preprocessing and calculating the TF-IDF vector for posed questions.
- **Similarity Calculation**: Using cosine similarity to determine the resemblance between questions and the corpus.
- **Selection and Provision of the Best Response**: Identifying the most similar words in the corpus and selecting the relevant response.

## Work Required
The project is divided into three main parts:
1. **Part I**: Development of basic functions to analyze the content of French presidential speeches.
2. **Part II**: Calculation of the similarity matrix and generation of automatic responses.
3. **Part III**: Generalization of the application to various themes.

### Part I: File Base
Analysis of French presidential speeches stored in the `speeches` directory. File names follow the format `Nomination_[president's name][number].txt`.

### Basic Functions
- Extracting presidents' names from the files.
- Associating a first name with each president.
- Displaying the list of presidents' names without duplicates.
- Converting texts to lowercase and storing in a new `cleaned` folder.
- Removing punctuation and special handling of certain characters.

## How to Contribute
Contributions are welcome. Please follow these steps to contribute to the project:
1. Fork the project.
2. Create a branch for each feature or correction.
3. Make a pull request to integrate your changes.

## License
Include details about the project's license, if applicable.

----

Feel free to copy and paste this template into your GitHub repository as the README for your "python_Chatbot" project. You can modify it as needed to better fit your project's specifics.