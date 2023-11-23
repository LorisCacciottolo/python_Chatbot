import os
import re


extracted_info = []
files_content = {}

for file in os.listdir("speeches/"):
    match = re.match(r"Nomination_([a-zA-Z\s]+)(\d*)\.txt", file)
    if match:
        president_name = match.group(1)
        speech_number = match.group(2) if match.group(2) != "" else "1"
        extracted_info.append((president_name, speech_number))

        with open(f"speeches/{file}", 'r', encoding='utf-8') as contentFile:
            content = contentFile.read()
        files_content[file] = content


for info in extracted_info:
    print(f"Nomination, {info[0]}, {info[1]}")


def preprocess_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    tokens = text.split()
    return tokens

processed_texts = {}
for file_name, file_content in files_content.items():
    tokens = preprocess_text(file_content)
    processed_texts[file_name] = tokens


print()
print()
print()
print(processed_texts)