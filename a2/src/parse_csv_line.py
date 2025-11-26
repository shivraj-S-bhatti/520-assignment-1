from typing import List

def parse_csv_line(line: str) -> List[str]:
    """Parse a single CSV line into fields."""
    if not line:
        return ['']

    fields = []
    current_field = ""
    in_quotes = False
    i = 0
    while i < len(line):
        char = line[i]
        if char == '"':
            if in_quotes:
                if i + 1 < len(line) and line[i + 1] == '"':
                    current_field += '"'
                    i += 1  # Skip the next quote
                else:
                    in_quotes = False
            else:
                in_quotes = True
        elif char == ',' and not in_quotes:
            fields.append(current_field)
            current_field = ""
        else:
            current_field += char
        i += 1
    fields.append(current_field)
    return fields