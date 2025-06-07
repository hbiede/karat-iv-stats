from typing import List, Tuple
from datetime import datetime
import sys
import re


class FileIterator:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def __iter__(self):
        with open(self.file_path, 'r') as file:
            while line := file.readline():
                yield line.strip()


def parse_file(file_path: str) -> List[Tuple[int, str, str]]:
    reader = FileIterator(file_path)

    pattern = re.compile(
        r'(?P<interview>\d{6})\s+(?P<date>\w{3} \d{2}, \d{4} \d{1,2}:\d{2}[ap]m) \w{3} (?P<timezone>\(-?\d{4}\))', re.IGNORECASE)

    last_interview = None
    last_date = None
    res = []
    for line in reader:
        if len(line) == 0:
            continue

        match = pattern.match(line)
        if match is None:
            res.append((last_interview, last_date, f"\"{line}\""))
        else:
            last_interview = match.group('interview')
            last_date_string = match.group('date')
            timezone = match.group('timezone')
            last_date = datetime.strptime(f"{last_date_string} {timezone}", '%b %d, %Y %I:%M%p (%z)').strftime('%Y-%m-%dT%H:%M:%S')

    return res


if __name__ == '__main__':
    for line in parse_file(sys.argv[1]):
        print(",".join(line))
