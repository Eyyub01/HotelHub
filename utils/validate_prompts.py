import re

def validate_prompt(prompt):
    valid_patterns = ['room', 'hotel', 'price', 'availability']
    if any(re.search(pattern, prompt.lower()) for pattern in valid_patterns):
        return True
    return False