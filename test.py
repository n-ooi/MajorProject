import json

with open("data.json", "r") as data:
    stuff = json.load(data)

formatted = str(stuff).replace(",", "\n")
print(formatted)

