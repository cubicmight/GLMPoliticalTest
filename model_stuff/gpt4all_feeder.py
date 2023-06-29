import os
import random
import re
import gpt4all
import textwrap


def polarity_gen_gpt4all():
    speech_data = {}
    gptj = gpt4all.GPT4All("ggml-gpt4all-j-v1.3-groovy")
    cleaned_data_directory = '../cleaned_data'
    speeches_directory = '../speeches'

    cleaned_data_file_list = os.listdir(cleaned_data_directory)
    random_file = random.choice(cleaned_data_file_list)
    print(random_file)

    congress_num, start_date, end_date = get_congress_dates(random_file)
    print(congress_num)
    print(start_date)
    print(end_date)

    random_file_path = os.path.join(cleaned_data_directory, random_file)
    with open(random_file_path, 'r', encoding='utf-8') as file:
        data = file.readlines()

    random_phrase = random.choice(data).strip().split('|')[0]
    print(f"Random phrase from '{random_file}': {random_phrase}")

    load_speech_data(congress_num, speeches_directory, speech_data)
    speech_data_congress = speech_data.get(congress_num)

    keyword_pattern = rf"\b{re.escape(random_phrase)}\b"
    sentences_with_word = [line.strip() for line in speech_data_congress if re.search(keyword_pattern, line)]

    random_sentences = random.sample(sentences_with_word, min(3, len(sentences_with_word)))

    # Truncate sentences longer than 1925 characters
    for i in range(len(random_sentences)):
        if len(random_sentences[i]) > 1925:
            random_sentences[i] = random_sentences[i][:1925]

    conversation = [
        {
            "role": "system",
            "content": "Given the below statement, the congress the phrase was said in, and the fact that a positive "
                       "number means that the statement is a right-leaning Republican "
                       "statement, a negative number means that the statement is a left-leaning "
                       "Democratic statement, and 0 means that it is a neutral statement. The "
                       "polarity value should be on a scale of -100 to 100, where the polarity value can be any "
                       "number within that range. It does not have to be just -100 or 100."
                       "\nExample Output: 30"
                       "\nExample Output: -58"
                       "\nExample Output: -39"
        },
        {
            "role": "user",
            "content": f"Phrase: {random_phrase}\n"
                       f"Start Date: {start_date}\n"
                       f"End Date: {end_date}\n"
                       f"Congress: {congress_num}\n"
                       f"Random Sentences:\n{'                               1'.join(textwrap.wrap(' '.join(random_sentences), width=1925))}\n"
                       "Provide a polarity value."
        }
    ]

    response = gptj.chat_completion(conversation)
    polarity = response['choices'][-1]['message']['content']
    print(polarity)


def get_congress_dates(file_name):
    congress_number = re.findall(r'\d+', file_name)[0]
    date_matches = re.findall(r'\d{1,2}_\w{3}_\d{2}', file_name)
    start_date = date_matches[0].replace('_', ' ')
    end_date = date_matches[1].replace('_', ' ') if len(date_matches) > 1 else "Unknown"
    return congress_number, start_date, end_date


def load_speech_data(congress_num, speeches_directory, speech_data):
    if congress_num in speech_data:
        return

    speech_data[congress_num] = []

    speech_file = os.path.join(speeches_directory, f"speeches_{congress_num}.txt")
    with open(speech_file, 'r', encoding='ISO-8859-1') as file:
        speech_data[congress_num] = file.readlines()


polarity_gen_gpt4all()
