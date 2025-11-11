from typing import List, Tuple

def merge_intervals(intervals: List[Tuple[int,int]]) -> List[Tuple[int,int]]:
    """Merges overlapping intervals."""

    if not intervals:
        return []

    intervals.sort()  # Sort by start time

    merged = []
    for interval in intervals:
        # If the list of merged intervals is empty or if the current
        # interval does not overlap with the last interval, append it
        if not merged or interval[0] > merged[-1][1]:
            merged.append(interval)
        else:
            # Otherwise, there is overlap, so we merge the current and last
            # intervals.
            merged[-1] = (merged[-1][0], max(merged[-1][1], interval[1]))

    return merged