import os
import shutil

# Path to the cleaned data directory
cleaned_data_dir = "../cleaned_data"

# Dictionary of congress session dates
congress_dates = {
    "114": {"Begin Date": "6-Jan-15", "Adjourn Date": "3-Jan-17"},
    "113": {"Begin Date": "3-Jan-13", "Adjourn Date": "3-Jan-15"},
    "112": {"Begin Date": "5-Jan-11", "Adjourn Date": "3-Jan-13"},
    "111": {"Begin Date": "6-Jan-09", "Adjourn Date": "3-Jan-11"},
    "110": {"Begin Date": "4-Jan-07", "Adjourn Date": "3-Jan-09"},
    "109": {"Begin Date": "4-Jan-05", "Adjourn Date": "3-Jan-07"},
    "108": {"Begin Date": "7-Jan-03", "Adjourn Date": "3-Jan-05"},
    "107": {"Begin Date": "3-Jan-01", "Adjourn Date": "2-Jan-03"},
    "106": {"Begin Date": "6-Jan-99", "Adjourn Date": "3-Jan-01"},
    "105": {"Begin Date": "7-Jan-97", "Adjourn Date": "3-Jan-99"},
    "104": {"Begin Date": "4-Jan-95", "Adjourn Date": "3-Jan-97"},
    "103": {"Begin Date": "5-Jan-93", "Adjourn Date": "3-Jan-95"},
    "102": {"Begin Date": "3-Jan-91", "Adjourn Date": "2-Jan-93"},
    "101": {"Begin Date": "3-Jan-89", "Adjourn Date": "2-Jan-91"},
    "100": {"Begin Date": "6-Jan-87", "Adjourn Date": "2-Jan-89"},
    "099": {"Begin Date": "3-Jan-85", "Adjourn Date": "2-Jan-87"},
    "098": {"Begin Date": "4-Jan-83", "Adjourn Date": "3-Jan-85"},
    "097": {"Begin Date": "5-Jan-81", "Adjourn Date": "4-Jan-83"},
    "096": {"Begin Date": "3-Jan-79", "Adjourn Date": "2-Jan-81"},
    "095": {"Begin Date": "4-Jan-77", "Adjourn Date": "3-Jan-79"},
    "094": {"Begin Date": "5-Jan-75", "Adjourn Date": "3-Jan-77"},
    "093": {"Begin Date": "3-Jan-73", "Adjourn Date": "3-Jan-75"},
    "092": {"Begin Date": "4-Jan-71", "Adjourn Date": "3-Jan-73"},
    "091": {"Begin Date": "3-Jan-69", "Adjourn Date": "3-Jan-71"},
    "090": {"Begin Date": "4-Jan-67", "Adjourn Date": "2-Jan-69"}
}

# Iterate over the files in the cleaned data directory
for filename in os.listdir(cleaned_data_dir):
    file_path = os.path.join(cleaned_data_dir, filename)

    # Extract the congress number from the file name
    congress_number = filename.split("_")[-1].split(".")[0]

    # Get the session number from the congress number
    session_number = congress_number[-1]

    # Check if the congress number is valid
    if congress_number not in congress_dates:
        print(f"Invalid congress number found in file name: {filename}")
        continue

    # Get the corresponding session dates
    session_dates = congress_dates[congress_number]
    begin_date = session_dates["Begin Date"]
    adjourn_date = session_dates["Adjourn Date"]

    # Generate the new file name with the date
    new_filename = f"{filename.split('.')[0]}_{begin_date.replace('-', '_')}_{adjourn_date.replace('-', '_')}.txt"
    new_file_path = os.path.join(cleaned_data_dir, new_filename)

    # Copy the file to the new file name
    shutil.copy(file_path, new_file_path)

    print(f"File {filename} copied to {new_filename}")
