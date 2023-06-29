import openai
import os
import random
import re
import chardet

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
    openai.api_key_path = '../model_stuff/API_KEY'

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
    load_speech_data(congress_num)

    # Retrieve congress-specific speech data
    speech_data_congress = speech_data.get(congress_num)

    # Filter sentences containing the word using regular expressions
    keyword_pattern = rf"\b{re.escape(random_phrase)}\b"
    sentences_with_word = [line.strip() for line in speech_data_congress if re.search(keyword_pattern, line)]

    # Randomly select a few sentences with the word
    random_sentences = random.sample(sentences_with_word, min(3, len(sentences_with_word)))

    # Print the randomly selected sentences
    print("Sentences containing the word:")
    for sentence in random_sentences:
        print(sentence)

    print("\n\n\n\n")
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
                       "\nOutput: -100"
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
        },
        {
            "role": "system",
            "content": "Here are some sentences containing the word, only reply with the polarity value:"
        }
    ]

    # Add sentences to the conversation
    character_count = sum(len(sentence) for sentence in conversation[2]['content'])  # Initial character count
    cutoff_index = None
    for i, sentence in enumerate(random_sentences):
        if character_count + len(sentence) > 4000:
            cutoff_index = i
            break
        conversation.append({
            "role": "system",
            "content": sentence
        })
        character_count += len(sentence)

    # If cutoff_index is set, remove remaining sentences
    if cutoff_index is not None:
        random_sentences = random_sentences[:cutoff_index]

    # Add selected sentences as user messages to the conversation
    for sentence in random_sentences:
        conversation.append({
            "role": "user",
            "content": sentence
        })

    # Prompt gpt-3.5-turbo using openai api
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )

    # Get model's reply
    reply = response['choices'][0]['message']['content']

    # Print the model's reply
    print(reply)

    # Print output of API call
    print(response['choices'][0]['message']['content'])


# Run the polarity_gen function
polarity_gen()
