import re
import boto3
import requests

# Initialize the S3 client
s3 = boto3.client('s3')


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

# List all the objects in your S3 bucket
objects = s3.list_objects(Bucket='your-s3-bucket-name')

# Check if the 'Contents' key is in the response
if 'Contents' in objects:
    for obj in objects['Contents']:
        # Check if the object key ends with .html
        if obj['Key'].endswith('.html'):
            print(f"Links found from [{obj['Key']}]:")
            try:
                # Get the object's content as bytes
                response = s3.get_object(Bucket='your-s3-bucket-name', Key=obj['Key'])
                html_content = response['Body'].read().decode('utf-8')

                url_regex = "(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"
                urls = re.findall(url_regex, html_content)
                for url in urls:
                    code = color_error_codes(try_link_connection(url))
                    print(f"[{code}] -> {url}")

            except Exception as e:
                print(f"Failed to retrieve content from {obj['Key']}: {e}")
else:
    print("No objects found in the S3 bucket.")

print("Done")