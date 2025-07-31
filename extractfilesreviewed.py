# Import necessary libraries for regular expressions and CSV handling
import re
import csv

# Function to extract info from a .txt file
def extract_info(file_path):
    # Open the file in read mode and read the entire text
    with open(file_path, 'r') as file:
        text = file.read()

    # Split the text into individual pull requests
    pull_requests = text.split('## Pull Request Overview')[1:]

    # Initialize an empty list to store the extracted data
    data = []
    
    # Iterate over each pull request
    for pr in pull_requests:
        # Search for patterns indicating files reviewed and comments generated
        match_reviewed = re.search(r'Copilot reviewed (\d+) out of (\d+) changed files.*generated (no|[0-9]+) comments?', pr)
        # Search for pattern indicating files not reviewed
        match_not_reviewed = re.search(r'Files not reviewed', pr)

        # If a match is found for files reviewed
        if match_reviewed:
            # Extract the number of files reviewed, total changed files, and comments generated
            files_reviewed = match_reviewed.group(1)
            total_changed_files = match_reviewed.group(2)
            comments_generated = match_reviewed.group(3)
            # Convert 'no' to 0 for comments generated
            if comments_generated == 'no':
                comments_generated = 0
            # Append the extracted data to the list
            data.append([files_reviewed, total_changed_files, comments_generated])
        # If a match is found for files not reviewed
        elif match_not_reviewed:
            # Append default values (0, 0, 0) to the list
            data.append([0, 0, 0])
        # If no match is found
        else:
            # Append 'N/A' values to the list
            data.append(['N/A', 'N/A', 'N/A'])

    # Return the extracted data
    return data

# Function to write the extracted data to a CSV file
def write_to_csv(data, output_path):
    # Open the output file in write mode
    with open(output_path, 'w', newline='') as csvfile:
        # Create a CSV writer
        writer = csv.writer(csvfile)
        # Write the header row
        writer.writerow(['Files Reviewed', 'Total Changed Files', 'Comments Generated'])
        # Write the extracted data rows
        writer.writerows(data)

# Main function
def main():
    # Specify the input file path and output CSV path
    file_path = 'reviewsbycopilot.txt'
    output_path = 'reviewcopilotdetails.csv'
    # Extract the data from the input file
    data = extract_info(file_path)
    # Write the extracted data to the output CSV file
    write_to_csv(data, output_path)

# Run the main function if the script is executed directly
if __name__ == '__main__':
    main()