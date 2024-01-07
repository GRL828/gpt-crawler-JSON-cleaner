import json
import re

def remove_unicode_characters(text):
    # Decode escaped Unicode characters to actual Unicode characters
    text = text.encode('utf-8').decode('unicode-escape')
    # Replace non-breaking spaces and other unwanted Unicode characters
    text = text.replace('\u00a0', ' ')  # Replace non-breaking spaces with regular spaces
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII characters
    return text

def remove_updated_string(text):
    # Regular expression pattern to match "Updated" strings
    updated_pattern = r'\nUpdated: \d{2} \w{3} \d{4} \d{2}:\d{2}\n'
    return re.sub(updated_pattern, '', text)

def remove_extra_newlines(text):
    # Regular expression pattern to match two or more newline characters
    newline_pattern = r'\n{2,}'
    return re.sub(newline_pattern, '\n', text)

def remove_paragraphs(text):
    # Regex pattern to remove the first paragraph
    first_section_pattern = re.escape("YOUR_TEXT_HERE")
    # Regex pattern to remove everything between 2 text strings
    second_section_pattern = r"YOUR_TEXT_HERE*?YOUR_TEXT_HERE"
    # Remove the first section
    text = re.sub(first_section_pattern, '', text, flags=re.DOTALL)
    # Remove the second section
    text = re.sub(second_section_pattern, '', text, flags=re.DOTALL)
    # Remove Unicode characters
    text = remove_unicode_characters(text)
    # Remove "Updated" strings
    text = remove_updated_string(text)
    # Remove extra newlines
    text = remove_extra_newlines(text)
    return text

def is_valid_json(json_data):
    try:
        json.dumps(json_data)  # Try converting the data to a JSON string
        return True
    except (TypeError, ValueError):
        return False

def split_json_data(data, max_size_mb, base_output_filename):
    max_size = max_size_mb * 1024 * 1024  # Convert MB to bytes
    current_size = 0
    current_part = 1
    current_data = []

    for item in data:
        item_string = json.dumps(item, indent=4)
        item_size = len(item_string.encode('utf-8'))

        if current_size + item_size > max_size and current_data:
            # Write the current_data to a file
            with open(f"{base_output_filename}_part{current_part}.json", 'w', encoding='utf-8') as file:
                json.dump(current_data, file, indent=4)
            current_part += 1
            current_data = []
            current_size = 0

        current_data.append(item)
        current_size += item_size

    # Write the remaining data to a file
    if current_data:
        with open(f"{base_output_filename}_part{current_part}.json", 'w', encoding='utf-8') as file:
            json.dump(current_data, file, indent=4)

def process_json_file(input_file, base_output_filename, max_size_mb):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    valid_data = []
    for entry in data:
        entry['html'] = remove_paragraphs(entry['html'])
        if is_valid_json(entry):
            valid_data.append(entry)
        else:
            print("Invalid JSON entry found and skipped.")

    split_json_data(valid_data, max_size_mb, base_output_filename)

# Replace 'input.json', 'output', and '5' (max size in MB) with your file names and desired max size
process_json_file('input.json', 'output', 5)
