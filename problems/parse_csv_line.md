# Parse CSV Line

**Function signature:**

```python
from typing import List

def parse_csv_line(line: str) -> List[str]:
```

**Task:** Parse a single CSV line into fields.

**Details & Constraints:**

Rules (RFC 4180 subset):
- Fields separated by commas.
- Fields may be quoted with double quotes.
- Inside quoted fields, double-double-quotes "" represent a literal quote.
- Commas inside quoted fields do not split.
- Leading/trailing spaces are preserved unless inside quotes.
- Empty line -> ['']
Examples:
- 'a,b,"c,d"' -> ['a','b','c,d']
- '"a""b",c' -> ['a"b','c']
