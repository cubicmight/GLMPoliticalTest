import os
import nltk
from nltk.corpus import wordnet
from nltk.probability import FreqDist
from nltk.util import ngrams

nltk.download('words')
nltk.download('wordnet')

# Load English word dictionary
english_words = set(nltk.corpus.words.words())

# Function to check if a phrase is composed of English words with a frequency threshold
def is_english(phrase, threshold=0):
    words = phrase.split()
    bigrams = list(ngrams(words, 2))  # Get bigrams from the words
    freq_dist = FreqDist(words)
    return all(
        all(
            word.lower() in english_words
            and any(wordnet.synsets(word.lower()))
            and nltk.corpus.words.words().count(word.lower()) >= threshold
            for word in bigram
        )
        for bigram in bigrams
    )

# Directory paths
dataset_directory = '../dataset'
cleaned_data_directory = '../cleaned_data'

# Create the cleaned_data directory if it doesn't exist
if not os.path.exists(cleaned_data_directory):
    os.makedirs(cleaned_data_directory)

# Specify the frequency threshold
threshold = 2  # Adjust the threshold as needed

# Iterate over files in the dataset directory
for filename in os.listdir(dataset_directory):
    if filename.startswith('partisan_phrases'):
        # Read data from file
        file_path = os.path.join(dataset_directory, filename)
        with open(file_path, 'r') as file:
            data = file.readlines()

        # Clean the data
        cleaned_data = []
        for line in data[1:]:  # Skip the column titles in the first line
            phrase, _ = line.strip().split('|')
            if is_english(phrase, threshold):
                cleaned_data.append(line)

        # Write cleaned data to a new file
        cleaned_file_path = os.path.join(cleaned_data_directory, f'cleaned_new_{filename}')
        with open(cleaned_file_path, 'w') as file:
            file.writelines(cleaned_data)

