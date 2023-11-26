import os
import re
from calculate_tfidf_matrix import calculate_tfidf_matrix
from calculate_tf import calculate_tf

# Afficher la liste des mots les moins importants dans le corpus de documents. Un mot est dit non important, si son TD-IDF = 0 dans tous les fichiers. 
def mots_non_importants(tfidf_matrix):
    non_important_words = []
    for word, scores in tfidf_matrix.items():
        if all(score == 0 for score in scores):
            non_important_words.append(word)
    return non_important_words

# Afficher le(s) mot(s) ayant le score TF-IDF le plus élevé
def mots_score_max(tfidf_matrix):
    max_score = 0
    mots_max = []

    for word, scores in tfidf_matrix.items():
        for score in scores:
            if score > max_score:
                max_score = score
                mots_max = [word]
            elif score == max_score:
                mots_max.append(word)

    return mots_max


# Indiquer le(s) mot(s) le(s) plus répété(s) par le président Chirac
def repeat_word(directory, president_name):
    tf_chirac = {}
    for file in os.listdir(directory):
        if president_name not in str(file): continue
        with open(f"{directory}/{file}", 'r', encoding='utf-8') as file:
            tf_dict = calculate_tf(file.read())
            for word, tf in tf_dict.items():
                if word not in tf_chirac:
                    tf_chirac[word] = 0
                tf_chirac[word] = tf_chirac[word] + tf

    maxTuple = max(tf_chirac.items(), key = lambda i : int(i[1]))
    return maxTuple


# Indiquer le(s) nom(s) du (des) président(s) qui a (ont) parlé de la « Nation » et celui qui l’a répété le plus de fois
def presidents_parlant_nation(directory):
    freq_nation = {}
    max_freq = 0
    president_max = ""

    for file in os.listdir(directory):
        with open(f"{directory}/{file}", 'r', encoding='utf-8') as file_content:
            content = file_content.read()
            count = content.count("nation")
            if count > 0:
                president = re.match(r"Nomination_([a-zA-Z\s]+)(\d*)\.txt", file).group(1)
                freq_nation[president] = freq_nation.get(president, 0) + count
                if freq_nation[president] > max_freq:
                    max_freq = freq_nation[president]
                    president_max = president

    return freq_nation, president_max


# Indiquer le premier président à parler du climat et/ou de l’écologie
def premier_president_ecologie(directory):
    for file in sorted(os.listdir(directory)):
        with open(f"{directory}/{file}", 'r', encoding='utf-8') as file_content:
            if "climat" in file_content.read() or "écologie" in file_content.read():
                return re.match(r"Nomination_([a-zA-Z\s]+)(\d*)\.txt", file).group(1)
    return None


# Hormis les mots dits « non importants », quel(s) est(sont) le(s) mot(s) que tous les présidents ont évoqués
def mots_evoques_par_tous(directory, tfidf_matrix):
    non_importants = mots_non_importants(tfidf_matrix)
    all_text = ""
    for file in os.listdir(directory):
        with open(f"{directory}/{file}", 'r', encoding='utf-8') as file:
            all_text += file.read() + " "
    tf_all = {}
    for file in os.listdir(directory):
        with open(f"{directory}/{file}", 'r', encoding='utf-8') as file:
            tf_dict = calculate_tf(file.read())
            for word, tf in tf_dict.items():
                if word not in all_text: continue
                if word not in tf_all:
                    tf_all[word] = 0
                tf_all[word] = tf_all[word] + tf

    mots_filtrés = {}
    for word, count in tf_all.items():
        if word not in non_importants:
            mots_filtrés[word] = count

    mots_tries = sorted(mots_filtrés.items(), key=lambda x: x[1], reverse=True)

    return mots_tries[:10]




tfidf_matrix = calculate_tfidf_matrix("cleaned")

print()
print(mots_non_importants(tfidf_matrix))
print()
print(mots_score_max(tfidf_matrix))
print()
print(repeat_word("cleaned", "Chirac"))
print()
print(presidents_parlant_nation("cleaned"))
print()
print(premier_president_ecologie("cleaned"))
print()
print(mots_evoques_par_tous("cleaned", tfidf_matrix))