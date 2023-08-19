import os
import re
import random

def get_random_phrase_and_info():
    # Directory containing files
    cleaned_data_directory = "../cleaned_data"

    # File containing phrases to search
    phrases_file = "../cleaned_data/top_handpicked_phrases.txt"

    # Read the lines from the phrases file
    with open(phrases_file, 'r') as phrases_file:
        lines = [line.strip() for line in phrases_file]

    # Choose a random line
    random_line = random.choice(lines)
    random_phrase = random_line.strip().split('|')[0]

    # Find the file containing the random line
    random_file = None
    congress_number = "Unknown"
    start_date = "Unknown"
    end_date = "Unknown"
    for file_name in os.listdir(cleaned_data_directory):
        if file_name.endswith('.txt'):
            file_path = os.path.join(cleaned_data_directory, file_name)
            with open(file_path, 'r') as file:
                content = file.read()
                if random_line in content:
                    congress_number = re.search(r'_(\d{1,3})_', file_name).group(1)
                    date_matches = re.findall(r'\d{1,2}_\w{3}_\d{2}', file_name)
                    start_date = date_matches[0].replace('_', ' ')
                    end_date = date_matches[1].replace('_', ' ') if len(date_matches) > 1 else "Unknown"
                    random_file = file_name
                    break

    # Print the results
    if random_file:
        print(f"Random Line: {random_line}")
        print(f"Random Phrase: {random_phrase}")
        print(f"File Name: {random_file}")
        print(f"Congress Number: {congress_number}")
        print(f"Start Date: {start_date}")
        print(f"End Date: {end_date}\n")
        return random_line, random_phrase, random_file, congress_number, start_date, end_date
    else:
        print("No matching phrase found in any files.")


def get_line_info(input_line, cleaned_data_directory="../cleaned_data"):
    # Read the lines from the phrases file
    phrases_file = os.path.join(cleaned_data_directory, "top_handpicked_phrases.txt")
    with open(phrases_file, 'r') as phrases_file:
        lines = [line.strip() for line in phrases_file]

    # Check if the input line exists in the list
    if input_line not in lines:
        print("Input line not found in the phrases file.")
        return None

    # Find the file containing the input line
    random_file = None
    congress_number = "Unknown"
    start_date = "Unknown"
    end_date = "Unknown"
    for file_name in os.listdir(cleaned_data_directory):
        if file_name.endswith('.txt'):
            file_path = os.path.join(cleaned_data_directory, file_name)
            with open(file_path, 'r') as file:
                content = file.read()
                if input_line in content:
                    congress_num = re.search(r'_(\d{1,3})_', file_name).group(1)
                    date_matches = re.findall(r'\d{1,2}_\w{3}_\d{2}', file_name)
                    start_date = date_matches[0].replace('_', ' ')
                    end_date = date_matches[1].replace('_', ' ') if len(date_matches) > 1 else "Unknown"
                    random_file = file_name
                    break

    # Print the results
    if random_file:
        return input_line, random_file, congress_num, start_date, end_date
    else:
        print("No matching phrase found in any files.")

# Example usage
input_line = "interest rate|-104.352614858731"
get_line_info(input_line)