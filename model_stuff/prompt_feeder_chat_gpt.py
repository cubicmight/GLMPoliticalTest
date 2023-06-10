import openai
import os
import random


def polarity_gen():
    openai.api_key_path = 'model_stuff/API_KEY'

    # Directory path for cleaned data
    cleaned_data_directory = 'cleaned_data'

    # List all files in the cleaned data directory
    file_list = os.listdir(cleaned_data_directory)

    # Pick a random file
    random_file = random.choice(file_list)

    # Read data from the random file
    random_file_path = os.path.join(cleaned_data_directory, random_file)
    with open(random_file_path, 'r') as file:
        data = file.readlines()

    # Pick a random phrase from the data
    random_phrase = random.choice(data).strip().split('|')[0]

    # Print the random phrase
    print(f"Random phrase from '{random_file}': {random_phrase}")

    # Prompt gpt-3.5-turbo using openai api
    output = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        # you can also give it a role and a context and then use system role to give it a persona. with this context it will answer the question
        messages=[
            {"role": "system",
             "content": "Given the statement" + random_phrase + " and the fact that a positive number means that the statement is a right-leaning Republican "
                                                                "statement, a negative number means that the statement is a left-leaning "
                                                                "Democratic statement, and 0 means that it is a neutral statement. The "
                                                                "polarity value should be on a scale of -100 to 100."},
            {"role": "user", "content": "What would the polarity value be given these constraints and the statement?"}
        ]
    )
    # Print output of api call
    return (output['choices'][0]['message']['content'])
