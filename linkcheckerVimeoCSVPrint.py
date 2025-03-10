import requests
import os
import re
import csv

path = "."
output_csv = "vimeo_links_cleaned.csv"

def try_link_connection(website):
    try:
        r = requests.head(website)
        return str(r.status_code)
    except:
        return "ERR"

def color_error_codes(code):
    red = "\u001b[31m"
    green = "\u001b[32m"
    yellow = "\u001b[33m"
    reset = "\u001b[0m"
    switcher = {
        '1': f"{green}{code}{reset}",
        '2': f"{green}{code}{reset}",
        '3': f"{yellow}{code}{reset}",
        '4': f"{red}{code}{reset}",
        'E': f"{red}{code}{reset}",
    }
    first_digit = code[0] if code else 'E'
    return switcher.get(first_digit, code)

# Regex for Vimeo links only (excluding unwanted api/player.js links)
url_regex = r"(https?:\/\/(?:www\.)?(vimeo\.com|player\.vimeo\.com|youtube\.com)\/(?!api\/player\.js)[^\s\"'>]+)"

# Collect HTML files
files = []
for root, dirs, file_names in os.walk(path):
    for file_name in file_names:
        if file_name.endswith(".html"):
            files.append(os.path.join(root, file_name))

# Open CSV file for writing
with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Module Name", "Cleaned Vimeo Link"])  # CSV headers

    # Dictionary to track unique links per module
    unique_links = {}

    for file_path in files:
        # Extract the module name from the directory path
        module_name_match = re.search(r"module(\d+)", file_path, re.IGNORECASE)
        module_name = module_name_match.group(0) if module_name_match else "Unknown"

        # Read file content
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read().replace('\n', '')

        print(f"\nLinks found from module [{file_path}]:")
        
        # Extract URLs
        urls = re.findall(url_regex, data)
        for url in urls:
            full_url = url[0]
            # Remove query parameters
            cleaned_url = full_url.split('?')[0]

            if cleaned_url not in unique_links:
                code = color_error_codes(try_link_connection(cleaned_url))
                print(f"[{code}] -> {cleaned_url}")
                # Save the cleaned URL alongside the module name
                unique_links[cleaned_url] = module_name
                # Write module name and cleaned URL to CSV
                writer.writerow([module_name, cleaned_url])

print(f"CSV file generated successfully: {output_csv}")