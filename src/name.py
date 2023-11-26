import re
import os

prenoms_presidents = {
    "Chirac": "Jacques",
    "Mitterrand": "François",
    "Sarkozy": "Nicolas",
    "Hollande": "François",
    "Macron": "Emmanuel",
    "Giscard dEstaing": "Valéry"
}

extracted_info = []
for file in os.listdir("speeches/"):
    match = re.match(r"Nomination_([a-zA-Z\s]+)(\d*)\.txt", file)
    if match:
        president_name = match.group(1).strip()
        speech_number = match.group(2) if match.group(2) != "" else "1"
        prenom = prenoms_presidents.get(president_name, "PrénomInconnu")
        extracted_info.append((prenom, president_name, speech_number))

presidents = set([info[1] for info in extracted_info])
print("Liste des présidents :", presidents)