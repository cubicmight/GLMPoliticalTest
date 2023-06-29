import os
import random
import re
import gpt4all


def polarity_gen_gpt4all():
    speech_data = {}  # Define speech_data variable
    gptj = gpt4all.GPT4All("ggml-gpt4all-j-v1.3-groovy")
    # Directory path for cleaned data
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

    # Load speech data for the congress number
    load_speech_data(congress_num, speeches_directory, speech_data)

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
        },
        {
            "role": "system",
            "content": "Here are some sentences containing the word:"
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

    # Prompt gpt-4all using gpt4all library
    response = gptj.chat_completion(conversation, streaming=False)
    reply = response['completions'][0]['message']['content']

    # Print the model's reply
    print(reply)


def get_congress_dates(file_name):
    cleaned_data_directory = '../cleaned_data'
    congress_num = re.search(r'\d+', file_name).group()
    start_date = ""
    end_date = ""
    cleaned_data_file_path = os.path.join(cleaned_data_directory, file_name)
    with open(cleaned_data_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith("Start Date"):
                start_date = line.split(":")[1].strip()
            elif line.startswith("End Date"):
                end_date = line.split(":")[1].strip()
    return congress_num, start_date, end_date



def load_speech_data(congress_num, speeches_directory, speech_data):
    if congress_num in speech_data:
        return

    speech_data[congress_num] = []

    # Read speech data for the congress number
    speech_file = os.path.join(speeches_directory, f"speeches_{congress_num}.txt")
    with open(speech_file, 'r', encoding='ISO-8859-1') as file:
        speech_data[congress_num] = file.readlines()


# Run the polarity_gen_gpt4all function
polarity_gen_gpt4all()
