# Calculate the total number of remaining phrases
import os

dataset_directory = '../dataset'
cleaned_data_directory = '../cleaned_data'

total_phrases = 0
for filename in os.listdir(cleaned_data_directory):
    with open(os.path.join(cleaned_data_directory, filename), 'r') as file:
        data = file.readlines()
        total_phrases += len(data)

# Print the total number of remaining phrases
print(f"Total number of remaining phrases: {total_phrases}")