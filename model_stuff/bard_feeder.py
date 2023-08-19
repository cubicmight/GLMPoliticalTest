from bardapi import Bard
import os
import random
import re
import chardet

# Set the Bard API token
token = 'aAjsv4s_cZzKx4pycdtkxOfjo_IIOopxKxQwwduF4XXvPcTFIntoppq0JQ1jEAtf4GhAgw.'
bard = Bard(token=token)

# Load speech data
speeches_directory = '../speeches'
speech_data = {}


def load_speech_data(congress_number):
    global speech_data
    if congress_number in speech_data:
        # Speech data for the congress number is already loaded
        return

    print(f"Loading speech data for Congress {congress_number}...")
    file_name = f"speeches_{congress_number.zfill(3)}.txt"  # Update the file name format
    speech_file_path = os.path.join(speeches_directory, file_name)
    speech_file_encoding = get_file_encoding(speech_file_path)
    with open(speech_file_path, 'r', encoding=speech_file_encoding, errors='ignore') as file:
        speech_data[congress_number] = file.readlines()
    print(f"Speech data for Congress {congress_number} loaded successfully.")


def get_file_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
        encoding = result.get('encoding')
        if encoding is None:
            # Fallback to a default encoding (e.g., UTF-8) if detection fails
            encoding = 'utf-8'
        return encoding


def get_congress_dates(file_name):
    congress_number = re.findall(r'\d+', file_name)[0]
    date_matches = re.findall(r'\d{1,2}_\w{3}_\d{2}', file_name)
    start_date = date_matches[0].replace('_', ' ')
    end_date = date_matches[1].replace('_', ' ') if len(date_matches) > 1 else "Unknown"
    return congress_number, start_date, end_date


def polarity_gen():
    # Directory path for cleaned data
    cleaned_data_directory = '../cleaned_data'

    # List all files in the cleaned data directory
    cleaned_data_file_list = os.listdir(cleaned_data_directory)

    # Pick a random file from the cleaned data directory
    random_file = random.choice(cleaned_data_file_list)
    print(random_file)

    # Get congress number and dates from file name
    congress_num, start_date, end_date = get_congress_dates(random_file)
    print(congress_num)
    print(start_date)
    print(end_date)

    # Read data from the random file in the cleaned data directory
    random_file_path = os.path.join(cleaned_data_directory, random_file)
    with open(random_file_path, 'r') as file:
        data = file.readlines()

    # Pick a random phrase from the data
    random_phrase = random.choice(data).strip().split('|')[0]

    # Print the random phrase
    print(f"Random phrase from '{random_file}': {random_phrase}")

    # Load speech data for the congress number
    # load_speech_data(congress_num)

    # Retrieve congress-specific speech data
    # speech_data_congress = speech_data.get(congress_num)

    # Filter sentences containing the word using regular expressions
    # keyword_pattern = rf"\b{re.escape(random_phrase)}\b"
    # sentences_with_word = [line.strip() for line in speech_data_congress if re.search(keyword_pattern, line)]

    # Randomly select a few sentences with the word
    # random_sentences = random.sample(sentences_with_word, min(3, len(sentences_with_word)))

    # Print the randomly selected sentences
    # print("Sentences containing the word:")
    # for sentence in random_sentences:
    #     print(sentence)

    print("\n\n\n\n")

    # Define the prompt
    prompt = f"Given the below phrase, the congress the phrase was said in, and the fact that a positive number " \
             f"means that the phrase is a right-leaning Republican " \
             f"phrase, a negative number means that the phrase is a left-leaning " \
             f"Democratic statement, and 0 means that it is a neutral statement. The " \
             f"polarity value should be on a scale of -100 to 100. Answer with only a polarity value." \
             f"\n\nExample:" \
             f"\nPhrase: red tape" \
             f"\nStart Date: January 4, 1977" \
             f"\nEnd Date: January 3, 1979" \
             f"\nCongress: 95" \
             f"\nOutput: 30" \
             f"\n\nExample:" \
             f"\nPhrase: interest rate" \
             f"\nStart Date: January 3, 2013" \
             f"\nEnd Date: January 3, 2015" \
             f"\nCongress: 113" \
             f"\nOutput: -100" \
             f"\n\nExample:" \
             f"\nPhrase: repeal afford" \
             f"\nStart Date: January 3, 2013" \
             f"\nEnd Date: January 3, 2015" \
             f"\nCongress: 113" \
             f"\nOutput: -39" \
             f"\n\nPhrase: {random_phrase}" \
             f"\nStart Date: {start_date}" \
             f"\nEnd Date: {end_date}" \
             f"\nCongress: {congress_num}" \
             f"\nKeep your entire response to a maximum of 15 characters. " \
             f"Answer with just the polarity value number and nothing else " \
             f"No explanation needed."\


    phrase_results = {}

    # Run the model three times for each phrase
    for _ in range(3):
        response = bard.get_answer(prompt)  # Change 'bard' to your appropriate API object

        # Get the model's reply
        reply = response['content']

        congress_pattern = re.escape(congress_num)
        num_pattern = r'[-+]?\d*\.\d+|\d+'
        combined_pattern = fr'{congress_pattern}.*({num_pattern})$'

        polarity_value_match = re.search(combined_pattern, reply)
        if polarity_value_match and polarity_value_match.group(1):
            polarity_value = float(polarity_value_match.group(1))
        else:
            polarity_value = 0.0

        phrase_results.setdefault(random_phrase, []).append(polarity_value)

        # Print the model's reply
        print(reply)

    # Print the stored phrase results
    print("Phrase Results:")
    for phrase, values in phrase_results.items():
        print(f"{phrase}: {values}")


# Initialize conversation list with system message
results = []  # To store the results

# Run the polarity_gen function
polarity_gen()
