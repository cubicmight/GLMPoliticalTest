import openai
import os
import random
import re
import chardet

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
    date_matches = re.findall(r'\d{1,2}_\w+_\d{2,4}', file_name)
    start_date = date_matches[0].replace('_', ' ')
    end_date = date_matches[1].replace('_', ' ') if len(date_matches) > 1 else "Unknown"
    return congress_number, start_date, end_date


def polarity_gen():
    openai.api_key_path = '../model_stuff/API_KEY'

    # Directory path for cleaned data and speeches
    cleaned_data_directory = '../cleaned_data'
    speeches_directory = '../speeches'

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

    # Retrieve congress-specific speech file
    speech_file = f"speeches_{congress_num}.txt"
    speech_file_path = os.path.join(speeches_directory, speech_file)

    # Read data from the congress-specific speech file
    speech_file_encoding = get_file_encoding(speech_file_path)
    with open(speech_file_path, 'r', encoding=speech_file_encoding, errors='ignore') as file:
        speech_data = file.readlines()

    # Retrieve sentences containing the word from the speech file
    sentences_with_word = []
    for line in speech_data:
        if random_phrase in line:
            sentences_with_word.append(line.strip())

    # Randomly select a few sentences with the word
    random_sentences = random.sample(sentences_with_word, min(3, len(sentences_with_word)))

    # Print the randomly selected sentences
    print("Sentences containing the word:")
    for sentence in random_sentences:
        print(sentence)

    # Initialize conversation list with system message
    conversation = [
        {
            "role": "system",
            "content": "Given the below statement, the congress the phrase was said in, and the fact that a positive number means that the statement is a right-leaning Republican "
                       "statement, a negative number means that the statement is a left-leaning "
                       "Democratic statement, and 0 means that it is a neutral statement. The "
                       "polarity value should be on a scale of -100 to 100."
                       "\n\nExample:"
                       "\nPhrase: red tape"
                       "\nStart Date: January 4, 1977"
                       "\nEnd Date: January 3, 1979"
                       "\nCongress: 95"
                       "\nOutput: 30"
                       "\n\nExample:"
                       "\nPhrase: interest rate"
                       "\nStart Date: January 3, 2013"
                       "\nEnd Date: January 3, 2015"
                       "\nCongress: 113"
                       "\nOutput: -104"
                       "\n\nExample:"
                       "\nPhrase: repeal afford"
                       "\nStart Date: January 3, 2013"
                       "\nEnd Date: January 3, 2015"
                       "\nCongress: 113"
                       "\nOutput: -39"
        },
        {
            "role": "user",
            "content": f"Phrase: {random_phrase}"
                       f"\nStart Date: {start_date}"
                       f"\nEnd Date: {end_date}"
                       f"\nCongress: {congress_num}"
        }
    ]

    # Conversation loop
    while True:
        # Prompt gpt-3.5-turbo using openai api
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation
        )

        # Get model's reply
        reply = response['choices'][0]['message']['content']

        # Print model's reply
        print(reply)

        # Add user's message and model's reply to the conversation
        conversation.append({
            "role": "user",
            "content": reply
        })

        # Break the loop if the conversation has ended
        if 'Polarity value:' in reply:
            break

    # Print output of API call
    print(response['choices'][0]['message']['content'])

polarity_gen()
