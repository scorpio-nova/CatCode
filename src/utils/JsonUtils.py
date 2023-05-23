import json

def read_json(filename: str) -> dict:
    with open(filename, 'r') as f:
        data = json.load(f)
    return data
 ## TODO: add write_json and remove all json occurances in other files