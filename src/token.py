import os
import re

cleaned_folder = "cleaned"
os.makedirs(cleaned_folder, exist_ok=True)

for file in os.listdir("speeches/"):
    with open(f"speeches/{file}", 'r', encoding='utf-8') as contentFile:
        content = contentFile.read().lower()
        content = re.sub(r"\w[’']", '', content)
        content = re.sub(r"-", ' ', content)
        content = re.sub(r"[^\w\s]", '', content)
        content = re.sub(r"\s+", ' ', content).strip()
    
    with open(f"{cleaned_folder}/{file}", 'w', encoding='utf-8') as cleanedFile:
        cleanedFile.write(content)
