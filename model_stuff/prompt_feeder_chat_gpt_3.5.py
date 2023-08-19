import openai
import re
from assign_info_for_handpicked import get_random_phrase_and_info

def polarity_gen():
    openai.api_key_path = '../model_stuff/API_KEY'

    random_line, random_phrase, random_file, congress_num, start_date, end_date = get_random_phrase_and_info()

    print("\n\n\n\n")
    # Initialize conversation list with system message
    conversation = [
        {
            "role": "system",
            "content": "Given the below phrase, the congress the phrase was said in, and the fact that a positive number means that the phrase is a right-leaning Republican "
                       "phrase, a negative number means that the phrase is a left-leaning "
                       "Democratic phrase, and 0 means that it is a neutral phrase. The "
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
    ]

    phrase_results = {}

    # Run the model three times for each phrase
    for _ in range(3):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation
        )

        # Get model's reply
        reply = response['choices'][0]['message']['content']

        # Extract numerical value from the response using regular expression
        polarity_value = re.search(r'(-?\d+)', reply)
        if polarity_value:
            polarity_value = int(polarity_value.group(0))
        else:
            polarity_value = 0  # Default value if no number is found

        # Store the result in the phrase_results dictionary
        phrase_results.setdefault(random_phrase, []).append(polarity_value)

        # Print the model's reply and output of API call
        print(response['choices'][0]['message']['content'])

    # Print the stored phrase results
    print("Phrase Results:")
    for phrase, values in phrase_results.items():
        print(f"{phrase}: {values}")


# Initialize conversation list with system message
results = []  # To store the results




# Run the polarity_gen function
polarity_gen()
