def calculate_average(numbers):
    return sum(numbers) / len(numbers)

def update_file_with_averages(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    averages = {}

    for line in lines:
        line = line.strip()
        if line:
            parts = line.split(':')
            phrase = parts[0].strip()
            numbers = [int(x) for x in parts[1].strip(' []').split(',')]
            avg = calculate_average(numbers)
            averages[phrase] = avg

    with open(output_file, 'w') as f:
        for line in lines:
            line = line.strip()
            if line:
                parts = line.split(':')
                phrase = parts[0].strip()
                if phrase in averages:
                    avg_value = averages[phrase]
                    line = f"{phrase}: {numbers} (avg: {avg_value:.2f})"
            f.write(line + '\n')

input_file = '../bard-results-dir/bard-results-1.txt'
output_file = '../bard-results-dir/bard-results-1-average.txt'
update_file_with_averages(input_file, output_file)
