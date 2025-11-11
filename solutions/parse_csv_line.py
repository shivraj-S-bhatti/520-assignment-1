from typing import List

def parse_csv_line(line: str) -> List[str]:
    fields = []
    current_field = []
    in_quotes = False
    i = 0
    n = len(line)
    
    while i < n:
        if line[i] == '"':
            if in_quotes and i + 1 < n and line[i+1] == '"':
                # Handle escaped quote inside quoted field
                current_field.append('"')
                i += 2
            else:
                # Toggle quote state
                in_quotes = not in_quotes
                i += 1
        elif line[i] == ',' and not in_quotes:
            # End of field
            fields.append(''.join(current_field))
            current_field = []
            i += 1
        else:
            # Regular character
            current_field.append(line[i])
            i += 1
    
    # Add the last field
    fields.append(''.join(current_field))
    
    # Handle empty line case
    if not fields and not line:
        return ['']
    
    return fields