from bardapi import Bard
import re
from assign_info_for_handpicked import get_random_phrase_and_info, get_line_info
import time

# Set the Bard API token
token = 'aAjsv9DcNcKW_RW63m6oqvrz4-ktPVoK0-axqCKVgqqr6XkCLK7CySLAvzto4_Y6RTA8vw.'
bard = Bard(token=token)

def polarity_gen():
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
                     f"\n\nPhrase: {phrase}" \
                     f"\nStart Date: {start_date}" \
                     f"\nEnd Date: {end_date}" \
                     f"\nCongress: {congress_num}" \
                     f"\nKeep your entire response to a maximum of 10 characters. " \
                     f"Answer with just the polarity value number and nothing else " \
                     f"No explanation needed."\


            phrase_results.setdefault(phrase, [])
            # Run the model three times for each phrase

            # Run the model three times for each phrase
            for _ in range(3):
                response = bard.get_answer(prompt)  # Change 'bard' to your appropriate API object

                # Get the model's reply
                reply = response['content']
                if reply.startswith('Response Error'):
                    with open("bard-results.txt", "w") as result_file:
                        for phrase, values in phrase_results.items():
                            result_file.write(f"{phrase}: {values}\n")
                    exit()

                # Store the result in the phrase_results dictionary
                phrase_results[phrase].append(reply)

                # Print the model's reply
                print('----------------MODEL RESPONSE----------------')
                print(reply)
                print("----------------------------------------------")

            # Print the stored results
            print("Phrase Results:")
            for phrase, values in phrase_results.items():
                print(f"{phrase}: {values}")
            time.sleep(20)
    with open("bard-results.txt", "w") as result_file:
        for phrase, values in phrase_results.items():
            result_file.write(f"{phrase}: {values}\n")

# Run the polarity_gen function
polarity_gen()
