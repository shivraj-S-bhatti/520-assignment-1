def normalize_path(path: str) -> str:
    """
    Normalizes a Unix-style path by resolving '.', '..', and redundant slashes.
    Preserves absolute vs relative semantics and handles edge cases like root and leading '..'.
    """
    is_absolute = path.startswith('/')
    segments = []
    
    for segment in path.split('/'):
        if segment == '' or segment == '.':
            continue
        elif segment == '..':
            if segments:
                if segments[-1] != '..':
                    segments.pop()
                else:
                    if not is_absolute:
                        segments.append(segment)
            else:
                if not is_absolute:
                    segments.append(segment)
        else:
            segments.append(segment)
    
    normalized = '/'.join(segments)
    if is_absolute:
        normalized = '/' + normalized
    if path.endswith('/') and normalized == '':
        normalized = '/'
    
    return normalized