import matplotlib.pyplot as plt


def read_average_file(file_path):
    averages = {}
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            parts = line.strip().split(':')
            phrase = parts[0]
            avg_value = float(parts[1].split('[')[1].split(']')[0])
            averages[phrase] = avg_value
    return averages


def read_polarity_file(file_path):
    polarities = {}
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            parts = line.strip().split('|')
            if len(parts) == 2:
                phrase = parts[0]
                polarity = float(parts[1])
                polarities[phrase] = polarity
            else:
                print(f"Issue with line: {line}")
    return polarities


def plot_graph(averages, polarities):
    phrases = list(averages.keys())
    average_values = list(averages.values())
    polarity_values = [polarities[phrase] for phrase in phrases]

    plt.figure(figsize=(10, 8))
    plt.barh(phrases, average_values, color='blue', label='Average')
    plt.scatter(polarity_values, phrases, color='red', label='Polarity')
    plt.xlabel('Value')
    plt.ylabel('Phrase')
    plt.title('Phrase Averages and Polarity Values')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Save the graph as an image
    output_image_path = '../gpt-4-results-dir/gpt-4-results-5-graph.png'  # Change this to your desired output image path
    plt.savefig(output_image_path)
    print(f"Graph saved as {output_image_path}")

    plt.show()


average_file_path = '../gpt-4-results-dir/gpt-4-results-5-average.txt'
polarity_file_path = '../cleaned_data/top_handpicked_phrases.txt'

averages = read_average_file(average_file_path)
polarities = read_polarity_file(polarity_file_path)

plot_graph(averages, polarities)
