import re
import os

president_names = {
    "Chirac": "Jacques",
    "Mitterrand": "François",
    "Sarkozy": "Nicolas",
    "Hollande": "François",
    "Macron": "Emmanuel",
    "Giscard dEstaing": "Valéry"
}

extracted_info = []
# Iterate through the files in speeches directory
for file in os.listdir("speeches/"):
    # Extracts the president's name from the file name using regex, assuming the format 'Nomination_[President's Name][Year].txt'
    # ([a-zA-Z\s]+) matches and captures a sequence of alphabetic characters (both uppercase and lowercase) and spaces.
    # (\d*) matches and captures zero or more digits. It's used here to extract the year from the file name.
    match = re.match(r"Nomination_([a-zA-Z\s]+)(\d*)\.txt", file)
    if match:
        # Extracts the president's first name from the regex match and removes any leading/trailing whitespace.
        president_name = match.group(1).strip()
        # Retrieves the speech number from the regex match; defaults to "1" if no number is found.
        speech_number = match.group(2) if match.group(2) != "" else "1"
        # Looks up the president's first name in a dictionary 'president_names'; defaults to "PrénomInconnu" if not found.
        firstname = president_names.get(president_name, "PrénomInconnu")
        # Appends a tuple with the first name, last name, and speech number to the list 'extracted_info'.
        extracted_info.append((firstname, president_name, speech_number))

presidents = set([info[1] for info in extracted_info])
print("Liste des présidents :", presidents)