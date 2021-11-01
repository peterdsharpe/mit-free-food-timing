import regex as re
from datetime import datetime

# Read file
with open("data/data.txt", "r") as f:
    raw_data = [line.strip() for line in f.readlines()]

times_str = []  # A list of strings like "7:15 PM"

i = 0
while i < len(raw_data):
    if not re.match("..:.M", raw_data[i]):
        if i + 1 != len(raw_data) and raw_data[i + 1].isnumeric():  # Account for weird Google Form format
            times_str.extend([raw_data[i]] * int(raw_data[i + 1]))
            i += 1
        else:
            times_str.append(raw_data[i])
    i += 1

# Fix data, assuming that all of the "AM" times are mistakes, since everyone says they got it on Oct. 31
times_str = [entry.replace("AM", "PM") for entry in times_str]

# Convert to datetime format, and sort
times = [
    datetime.strptime(entry, '%I:%M %p')
    for entry in times_str
]
times.sort() # `times` is now List[datetime]
