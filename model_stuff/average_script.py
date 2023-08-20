# Define a function to calculate the average of a list of numbers
def calculate_average(numbers):
    return sum(numbers) / len(numbers)

# Define a function to update the input file with the calculated averages and write them to the output file
def update_file_with_averages(input_file, output_file):
    # Read the lines from the input file
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Create a dictionary to store calculated averages for each phrase
    averages = {}

    # Iterate through the lines to calculate averages and store them in the averages dictionary
    for line in lines:
        line = line.strip()
        if line:
            parts = line.split(':')
            phrase = parts[0].strip()
            numbers = [int(x) for x in parts[1].strip(' []').split(',')]
            avg = calculate_average(numbers)
            averages[phrase] = avg

    # Create a list to store updated lines
    updated_lines = []

    # Iterate through the lines to update them with calculated averages
    for line in lines:
        line = line.strip()
        if line:
            parts = line.split(':')
            phrase = parts[0].strip()
            if phrase in averages:
                avg_value = averages[phrase]
                updated_line = f"{phrase}: [{avg_value:.2f}]"
                updated_lines.append(updated_line)
            else:
                updated_lines.append(line)

    # Write the updated lines to the output file
    with open(output_file, 'w') as f:
        for line in updated_lines:
            f.write(line + '\n')

# Define input and output file paths
input_file = '../gpt-4-results-dir/gpt-4-results-1.txt'
output_file = '../gpt-4-results-dir/gpt-4-results-1-average.txt'

# Call the function to update the file with averages
update_file_with_averages(input_file, output_file)
