import os
import nltk
from nltk.corpus import wordnet
from nltk.probability import FreqDist

nltk.download('words')
nltk.download('wordnet')

# Load English word dictionary
english_words = set(nltk.corpus.words.words())

# Function to check if a phrase is composed of English words with a frequency threshold
def is_english(phrase, threshold=0):
    words = phrase.split()
    freq_dist = FreqDist(words)
    return all(word.lower() in english_words and wordnet.synsets(word.lower()) and FreqDist(wordnet.synsets(word.lower())[0].lemma_names()).freq(word.lower()) > threshold for word in words)

# Directory paths
dataset_directory = '../dataset'
cleaned_data_directory = '../cleaned_data'

# Create the cleaned_data directory if it doesn't exist
if not os.path.exists(cleaned_data_directory):
    os.makedirs(cleaned_data_directory)

# Specify the frequency threshold
threshold = 0

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
            words = phrase.split()
            if all(word.lower() in english_words and wordnet.synsets(word.lower()) and FreqDist(wordnet.synsets(word.lower())[0].lemma_names()).freq(word.lower()) > threshold for word in words):
                cleaned_data.append(line)

        # Write cleaned data to a new file
        cleaned_file_path = os.path.join(cleaned_data_directory, f'cleaned2_{filename}')
        with open(cleaned_file_path, 'w') as file:
            file.writelines(cleaned_data)
