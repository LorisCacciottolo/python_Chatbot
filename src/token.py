import os
import re

# Clean all Speeches in "cleaned" folder

cleaned_folder = "cleaned"
os.makedirs(cleaned_folder, exist_ok=True)

# Iterates over files in the "speeches/" directory.
for file in os.listdir("speeches/"):
    # Opens and reads the file's content, converting it to lowercase.
    with open(f"speeches/{file}", 'r', encoding='utf-8') as contentFile:
        content = contentFile.read().lower()
        # Removes all apostrophes and characters following them within words.
        content = re.sub(r"\w[’']", '', content)
        # Replaces hyphens with spaces to avoid concatenation of words.
        content = re.sub(r"-", ' ', content)
        # Removes all characters except word characters (letters and numbers) and whitespace.
        content = re.sub(r"[^\w\s]", '', content)
        # Replaces multiple whitespace characters with a single space and trims leading/trailing spaces.
        content = re.sub(r"\s+", ' ', content).strip()
    
    # Write all change in cleaned folder
    with open(f"{cleaned_folder}/{file}", 'w', encoding='utf-8') as cleanedFile:
        cleanedFile.write(content)
