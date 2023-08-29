import json

# Your JSON-formatted string
json_string = '[{"cusip":"912797FA0","issueDate":"2023-08-31T00:00:00","securityType":"Bill", ...}]'

# Convert the string to a Python list of dictionaries
data = json.loads(json_string)