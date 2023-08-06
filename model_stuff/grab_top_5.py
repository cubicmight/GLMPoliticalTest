import os
import shutil

# Path to the cleaned data directory
cleaned_data_dir = "../cleaned_data"

# List for phrases and phrase numbers
phrase_and_phrase_num = []

# Iterate over the files in the cleaned data directory
for filename in os.listdir(cleaned_data_dir):
    file_path = os.path.join(cleaned_data_dir, filename)
    with open(file_path, 'r') as file:
        data = file.readlines()
    for line in data[1:]:  # Skip the column titles in the first line
        phrase_and_num = line.strip().split('|')
        phrase = phrase_and_num[0]
        num = float(phrase_and_num[1])  # Convert the numeric value to float
        phrase_and_phrase_num.append((phrase, num))  # Store the phrase and its numeric value as a tuple

# Sort the data by absolute value in descending order
sorted_data = sorted(phrase_and_phrase_num, key=lambda x: abs(x[1]), reverse=True)

# Select the top 300 phrases
top_300_phrases = sorted_data[:300]

# Write the selected phrases to a new file
output_file = "top_phrases.txt"
with open(output_file, "w") as f:
    for phrase, value in top_300_phrases:
        f.write(f"{phrase}|{value}\n")

print(f"Top 300 phrases written to '{output_file}'.")

# Read the file and remove duplicates while considering absolute values
with open(output_file, 'r') as f:
    lines = f.readlines()

unique_phrases = {}
for line in lines:
    phrase, value = line.strip().split('|')
    numeric_value = float(value)
    if phrase in unique_phrases:
        existing_value = unique_phrases[phrase]
        if abs(numeric_value) > abs(existing_value):
            unique_phrases[phrase] = numeric_value
    else:
        unique_phrases[phrase] = numeric_value

# Ensure there are 300 unique phrases
if len(unique_phrases) < 300:
    additional_phrases = sorted_data[300 - len(unique_phrases):]
    for phrase, value in additional_phrases:
        if len(unique_phrases) >= 300:
            break
        if phrase not in unique_phrases:
            unique_phrases[phrase] = value

# Write the unique phrases to the file
with open(output_file, "w") as f:
    for phrase, value in unique_phrases.items():
        f.write(f"{phrase}|{value}\n")

print(f"Unique phrases written to '{output_file}'.")
