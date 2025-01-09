from rest_framework.exceptions import ParseError
import json


def preprocess_request_data(data):
    """
    Preprocesses the request data (multipart form data) by:
    - Removing unnecessary lists from dictionary values.
    - Parsing 'variants' from JSON string to a Python object.
    - Converting 'ProductID' to a BigInteger (int in Python).
    """
    processed_data = {}
    for key, value in data.items():
        if isinstance(value, list) and value:
            processed_value = value[0]
            
            if key == "variants":
                try:
                    processed_value = json.loads(processed_value)
                except json.JSONDecodeError:
                    raise ParseError({"variants": "Invalid JSON format for variants."})
            
            if key == "ProductID":
                try:
                    processed_value = int(processed_value)
                except ValueError:
                    raise ParseError({"ProductID": "Invalid integer value for ProductID."})
            
            processed_data[key] = processed_value
        else:
            processed_data[key] = value
    return processed_data
