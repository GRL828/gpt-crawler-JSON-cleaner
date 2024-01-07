# JSON-Cleaner
JSON Cleaner for gpt-crawler - https://github.com/GRL828/gpt-crawler

This script will process your JSON file, clean up its content, validate each entry, and then split the output into multiple files if it exceeds a certain size. Each output file will be a valid JSON file. 

Change the YOUR_TEXT_HERE in the remove_paragraphs section to the text you want to remove from the JSON

def remove_paragraphs(text):
    # Regex pattern to remove the first paragraph
    first_section_pattern = re.escape("YOUR_TEXT_HERE")
    # Regex pattern to remove everything between 2 text strings
    second_section_pattern = r"YOUR_TEXT_HERE*?YOUR_TEXT_HERE"


Remember to replace 'input.json', 'output', and 5 with your actual input file name, desired output file base name, and maximum file size in MB, respectively.
