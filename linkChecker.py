import requests
import os
import re

path = "."

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
   # Dictionary-based switch case
   switcher = {
      '1': f"{green}{code}{reset}",
      '2': f"{green}{code}{reset}",
      '3': f"{yellow}{code}{reset}",
      '4': f"{red}{code}{reset}",
      '4': f"{red}{code}{reset}",
      'E': f"{red}{code}{reset}",
   }
   # split string and get first digit
   first_digit = [*code][0]
   return switcher.get(first_digit, code)

# temporary storage for .html filenames
files = []
# recursively traverses directory given as "path"
for r, d, f in os.walk(path):
    for file in f:
         # adding if .html is found in filename
        if '.html' in file:
            files.append(os.path.join(r, file))

for f in files:
   # converts file contents to string and placed in data
   with open(f, 'r') as file:
      data = file.read().replace('\n', '')
   print(f"\tlinks found from [{f}]:")
   # regex for parsing strings
   url_regex = "(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"
   urls = re.findall(url_regex, data)
   for url in urls:
      code = color_error_codes(try_link_connection(url))
      print(f"[{code}] -> {url}")
   

print("Done")
