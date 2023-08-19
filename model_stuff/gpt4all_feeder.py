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

    response = gptj.generate(f"Given the below statement, the congress the phrase was said in, and the fact that a positive number "
             f"means that the statement is a right-leaning Republican " 
             f"statement, a negative number means that the statement is a left-leaning " 
             f"Democratic statement, and 0 means that it is a neutral statement. The " 
             f"polarity value should be on a scale of -100 to 100. Answer with only a polarity value." 
             f"\n\nExample:" 
             f"\nPhrase: red tape" 
             f"\nStart Date: January 4, 1977" 
             f"\nEnd Date: January 3, 1979" 
             f"\nCongress: 95" 
             f"\nOutput: 30" 
             f"\n\nExample:" 
             f"\nPhrase: interest rate" 
             f"\nStart Date: January 3, 2013"
             f"\nEnd Date: January 3, 2015"
             f"\nCongress: 113"
             f"\nOutput: -100"
             f"\n\nExample:"
             f"\nPhrase: repeal afford"
             f"\nStart Date: January 3, 2013" 
             f"\nEnd Date: January 3, 2015" 
             f"\nCongress: 113"
             f"\nOutput: -39"
             f"\n\nPhrase: {random_phrase}" 
             f"\nStart Date: {start_date}"
             f"\nEnd Date: {end_date}" 
             f"\nCongress: {congress_num}")
    print(response)


def get_congress_dates(file_name):
    congress_number = re.findall(r'\d+', file_name)[0]
    date_matches = re.findall(r'\d{1,2}_\w{3}_\d{2}', file_name)
    start_date = date_matches[0].replace('_', ' ')
    end_date = date_matches[1].replace('_', ' ') if len(date_matches) > 1 else "Unknown"
    return congress_number, start_date, end_date


# def load_speech_data(congress_num, speeches_directory, speech_data):
#     if congress_num in speech_data:
#         return
#
#     speech_data[congress_num] = []
#
#     speech_file = os.path.join(speeches_directory, f"speeches_{congress_num}.txt")
#     with open(speech_file, 'r', encoding='ISO-8859-1') as file:
#         speech_data[congress_num] = file.readlines()


polarity_gen_gpt4all()
