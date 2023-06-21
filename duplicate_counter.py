import os
from collections import Counter

def count_duplicates(directory):
    # Step 1: Gather file paths
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_paths.append(os.path.join(root, file))

    # Step 2-4: Read file contents and collect phrases
    phrases = []
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            for line in file:
                phrase = line.strip().split("|")[0]
                phrases.append(phrase)

    # Step 5: Count duplicates
    duplicate_counts = Counter(phrases)
    duplicates = {phrase: count for phrase, count in duplicate_counts.items() if count > 1}

    # Display duplicate information
    total_duplicate_count = sum(duplicates.values())
    if total_duplicate_count > 0:
        print(f"Total Duplicate Phrases: {total_duplicate_count}")
    for phrase, count in duplicates.items():
        print(f"Phrase: {phrase}\tCount: {count}")


# Example usage
directory_path = 'cleaned_data'  # Replace with the actual directory path
count_duplicates(directory_path)
