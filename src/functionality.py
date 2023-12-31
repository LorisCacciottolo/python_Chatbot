import os
import re
from calculate_tfidf_matrix import calculate_tfidf_matrix
from calculate_tf import calculate_tf

# Display the list of the non important words in the corpus of documents. A word is said non important if his TD-IDF = 0 in every file.
def non_important_words(tfidf_matrix):
    # create a variable that will contain the non important words.
    get_non_important_words = []
    # loop all the items of our tf-idf matrix.
    for word, scores in tfidf_matrix.items():
        if all(score == 0 for score in scores):  # "all" returns "true" if the score = 0.
            get_non_important_words.append(word)
    return get_non_important_words

# Display the word(s) having the highest TF-IDF score.
def words_score_max(tfidf_matrix) :
    max_score = 0
    # Initialize a list of words.
    max_words = []

    # Iterate through the (word, scores) pairs in the tfidf_matrix dictionary
    for word, scores in tfidf_matrix.items():
        # Loop the score list
        for score in scores:
            # Check if the current score is greater than the maximum score
            if score > max_score:
                # If so, update the maximum score and reset the list of maximum words
                max_score = score
                max_words = [word]
            # If the score is equal to the maximum score found so far
            elif score == max_score:
                max_words.append(word)

    return max_words


def repeat_word(directory, president_name):
    # Initialize an empty dictionary to store the term frequency for each word
    tf_chirac = {}

    # Iterate through the files in cleaned directory
    for file in os.listdir(directory):
        # Check if the president's name is not in the filename, if true, skip to the next iteration
        if president_name not in str(file):
            continue

        # Open the file for reading with UTF-8 encoding
        with open(f"{directory}/{file}", 'r', encoding='utf-8') as file:
            # Read the file
            tf_dict = calculate_tf(file.read())

            # Iterate through the items (word, tf) in the tf_dict
            for word, tf in tf_dict.items():
                # If the word is not in tf_chirac, set the tf of chirac to 0
                if word not in tf_chirac:
                    tf_chirac[word] = 0
                # Increment the term frequency of the word in tf_chirac
                tf_chirac[word] = tf_chirac[word] + tf

    # Find the word with the maximum term frequency in tf_chirac
    maxTuple = max(tf_chirac.items(), key=lambda i: int(i[1]))

    return maxTuple



# Indicate the name(s) of the president(s) who spoke about the « Nation » and the one who has repeated this word the most times
def presidents_speaking_nation(directory):
    freq_nation = {}
    max_freq = 0
    president_max = ""

    # Iterate through the files in cleaned directory
    for file in os.listdir(directory):
        # Open the file for reading with UTF-8 encoding
        with open(f"{directory}/{file}", 'r', encoding='utf-8') as file_content:
            content = file_content.read()
            count = content.count("nation")
            if count > 0:
                # Extracts the president's name from the file name using regex, assuming the format 'Nomination_[President's Name][Year].txt'
                # ([a-zA-Z\s]+) matches and captures a sequence of alphabetic characters (both uppercase and lowercase) and spaces.
                # (\d*) matches and captures zero or more digits. It's used here to extract the year from the file name.
                president = re.match(r"Nomination_([a-zA-Z\s]+)(\d*)\.txt", file).group(1)
                freq_nation[president] = freq_nation.get(president, 0) + count
                if freq_nation[president] > max_freq:
                    max_freq = freq_nation[president]
                    president_max = president

    return freq_nation, president_max


# Indicate the first president talking about the climate and/or the ecology.
def first_president_ecology(directory):
    # Iterate through the files in cleaned directory
    for file in sorted(os.listdir(directory)):
        # Open the file for reading with UTF-8 encoding
        with open(f"{directory}/{file}", 'r', encoding='utf-8') as file_content:
            # Check if "climat" or "écologie" is in file
            if "climat" in file_content.read() or "écologie" in file_content.read():
                return re.match(r"Nomination_([a-zA-Z\s]+)(\d*)\.txt", file).group(1)
    return None


# Apart from the so-called « non important » words, which is/are the word(s) that every president has mentioned.
def words_mentioned_by_everyone(directory, tfidf_matrix):
    non_important = non_important_words(tfidf_matrix)
    all_text = ""
    # Iterate through the files in cleaned directory
    for file in os.listdir(directory):
        # Open the file for reading with UTF-8 encoding
        with open(f"{directory}/{file}", 'r', encoding='utf-8') as file:
            all_text += file.read() + " "
    tf_all = {}
    # Iterate through the files in cleaned directory
    for file in os.listdir(directory):
        # Open the file for reading with UTF-8 encoding
        with open(f"{directory}/{file}", 'r', encoding='utf-8') as file:
            # Calculate the tf of the current file
            tf_dict = calculate_tf(file.read())
            for word, tf in tf_dict.items():
                if word not in all_text: continue
                if word not in tf_all:
                    tf_all[word] = 0
                tf_all[word] = tf_all[word] + tf

    # Check if word selected not in non_important word
    filtered_words = {}
    for word, count in tf_all.items():
        if word not in non_important:
            filtered_words[word] = count

    # Sorts 'filtered_words' dictionary by value in descending order. 'filtered_words' is a dict where keys are words and values are their frequencies. 
    # The sorting is done based on frequencies (x[1]), with the most frequent words first.
    mots_tries = sorted(filtered_words.items(), key=lambda x: x[1], reverse=True)

    return mots_tries


# Our small but cool CLI
if __name__ == '__main__':
    tfidf_matrix = calculate_tfidf_matrix("cleaned")
    print("1 - Calculate the least important words")
    print("2 - Calculate the words with the highest TF-IDF score")
    print("3 - Calculate the most repeated words by President Chirac")
    print("4 - Calculate which president spoke of the 'Nation' and which repeated it most often")
    print("5 - Calculate which president was the first to speak about climate and/or ecology")
    print("6 - Calculate the words that all the presidents mentioned.")
    print()

    choix = int(input("Le Choix: "))

    if choix == 1:
        print(non_important_words(tfidf_matrix))
    if choix == 2:
        print(words_score_max(tfidf_matrix))
    if choix == 3:
        print(repeat_word("cleaned", "Chirac"))
    if choix == 4:
        nation_presidents = presidents_speaking_nation("cleaned")
        print("Presidents who have talked about nations",nation_presidents[0])
        print("The president who spoke most about nations",nation_presidents[1])
    if choix == 5:
        print(first_president_ecology("cleaned"))
    if choix == 6:
        print(words_mentioned_by_everyone("cleaned", tfidf_matrix))
