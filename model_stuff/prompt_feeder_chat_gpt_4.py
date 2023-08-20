import time
import openai
import re
from assign_info_for_handpicked import get_line_info


def polarity_gen():
    openai.api_key_path = '../model_stuff/API_KEY'
    phrase_results = {}  # Initialize outside the loop
    with open('../cleaned_data/top_handpicked_phrases.txt', 'r') as handpicked:
        handpicked_read = [line.strip() for line in handpicked.readlines()]
        for line in handpicked_read:
            input_line, random_file, congress_num, start_date, end_date = get_line_info(line)
            phrase = input_line.strip().split('|')[0]
            print("---------THE MODEL IS BEING PROMPTED WITH---------")
            print(f"Phrase: {phrase}")
            print(f"Congress Number: {congress_num}")
            print(f"Start Date: {start_date}")
            print(f"End Date: {end_date}\n")
            print("---------------------------------------------------")
            print("\n\n")
            # Initialize conversation list with system message
            conversation = [
                {
                    "role": "system",
                    "content": "Given the below phrase, the congress the phrase was said in, and the start and end date of that congress, and the fact that a positive "
                               "number means that the phrase is a right-leaning Republican "
                               "phrase, a negative number means that the phrase is a left-leaning "
                               "Democratic phrase, and 0 means that it is a neutral phrase, output the polarity value for the given phrase. The "
                               "polarity value should be on a scale of -110 to 110."
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
                    "content": f"Phrase: {phrase}"
                               f"\nStart Date: {start_date}"
                               f"\nEnd Date: {end_date}"
                               f"\nCongress: {congress_num}"
                },
            ]

            phrase_results.setdefault(phrase, [])
            # Run the model three times for each phrase
            for _ in range(3):
                response = openai.ChatCompletion.create(
                    model="gpt-4",
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
                phrase_results[phrase].append(polarity_value)

                # Print the model's reply and output of API call
                print('----------------MODEL RESPONSE----------------')
                print(response['choices'][0]['message']['content'])
                print("----------------------------------------------")

                # Print the stored phrase results
            print("Phrase Results:")
            for phrase, values in phrase_results.items():
                print(f"{phrase}: {values}")
            time.sleep(5)
    with open("../gpt-4-results-dir/gpt-4-results-1-average.txt", "w") as result_file:
        for phrase, values in phrase_results.items():
            result_file.write(f"{phrase}: {values}\n")


# Initialize conversation list with system message
results = []  # To store the results

# Run the polarity_gen function
polarity_gen()
