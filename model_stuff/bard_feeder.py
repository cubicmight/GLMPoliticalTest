from bardapi import Bard
import re
from assign_info_for_handpicked import get_random_phrase_and_info

# Set the Bard API token
token = 'aAjsv4s_cZzKx4pycdtkxOfjo_IIOopxKxQwwduF4XXvPcTFIntoppq0JQ1jEAtf4GhAgw.'
bard = Bard(token=token)

def polarity_gen():

    random_line, random_phrase, random_file, congress_num, start_date, end_date = get_random_phrase_and_info()

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
