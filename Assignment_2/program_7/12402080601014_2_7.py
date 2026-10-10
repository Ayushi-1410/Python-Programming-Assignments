import json
from collections import defaultdict

def read_records(path):
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                yield None

path = input("Enter JSONL file path: ")

stats = defaultdict(lambda: {
    "count": 0,
    "min": None,
    "max": None,
    "sum": 0,
    "corrupted": 0
})

for record in read_records(path):
    if record is None:
        continue

    device = record.get("device_id", "UNKNOWN")

    try:
        temperature = float(record["temperature_c"])
        float(record["humidity"])
    except (KeyError, ValueError, TypeError):
        stats[device]["corrupted"] += 1
        continue

    item = stats[device]
    item["count"] += 1
    item["sum"] += temperature

    if item["min"] is None or temperature < item["min"]:
        item["min"] = temperature

    if item["max"] is None or temperature > item["max"]:
        item["max"] = temperature

for device in sorted(stats):
    item = stats[device]
    average = item["sum"] / item["count"] if item["count"] else 0

    print(
        device,
        "count=" + str(item["count"]),
        "min=" + str(item["min"]),
        "max=" + str(item["max"]),
        "avg=" + f"{average:.2f}",
        "corrupted=" + str(item["corrupted"])
    )