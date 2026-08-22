import json

def extract_json_from_string(string):
    try:
        first = string.find('{')
        last = string.rfind('}')
        if first != -1 and last != -1:
            json_str = string[first:last+1]
            return json.loads(json_str)
    except json.JSONDecodeError:    
        return None