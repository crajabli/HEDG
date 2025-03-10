import re
import boto3
import requests
import boto3
import boto3

# Initialize the S3 client
# pip install boto3
#     ```

# 2. Import Boto3: Import the Boto3 library in your Python script:
#     ```python
#     ```

# 3. Create an S3 Client: Create an S3 client object by calling the `boto3.client()` method and passing the service name as `'s3'`:
#     ```python
#     s3 = boto3.client('s3')
#     ```

# 4. Use the S3 Client: You can now use the `s3` object to interact with Amazon S3. For example, you can list objects in a bucket, upload files, download files, etc.

# Here's an example of listing objects in a bucket:

# Connect to the S3 client
s3 = boto3.client('s3')

# Navigate to the "modules" directory
bucket_name = 'cppr-institute-prod'
prefix = 'modules/'

response = s3.list_objects(Bucket=bucket_name, Prefix=prefix)

if 'Contents' in response:
    for obj in response['Contents']:
        print(obj['Key'])
else:
    print("No objects found in the 'modules' directory.")


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