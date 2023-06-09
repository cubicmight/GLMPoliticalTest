import os
import nltk
nltk.download('words')
# Use nltk count to see frequency of word in corpus
# Load English word dictionary
english_words = set(nltk.corpus.words.words())

# Function to check if a phrase is composed of English words
def is_english(phrase):
    words = phrase.split()
    return all(word.lower() in english_words for word in words)

# Directory paths
dataset_directory = '../dataset'
cleaned_data_directory = '../cleaned_data'

# Create the cleaned_data directory if it doesn't exist
if not os.path.exists(cleaned_data_directory):
    os.makedirs(cleaned_data_directory)

# Iterate over files in the dataset directory
for filename in os.listdir(dataset_directory):
    if filename.startswith('partisan_phrases'):
        # Read data from file
        file_path = os.path.join(dataset_directory, filename)
        with open(file_path, 'r') as file:
            data = file.readlines()

        # Clean the data
        cleaned_data = []
        for line in data:
            phrase, _ = line.strip().split('|')
            if is_english(phrase):
                cleaned_data.append(line)

        # Write cleaned data to a new file
        cleaned_file_path = os.path.join(cleaned_data_directory, f'cleaned2_{filename}')
        with open(cleaned_file_path, 'w') as file:
            file.writelines(cleaned_data)