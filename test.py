import json

filename = "data.json"


def Choices():
    print("\n\nJSON Editor Template\n"
          "(1) View Data\n"
          "(2) Add Data\n"
          "(3) Edit Data\n"
          "(4) Delete Data\n"
          "(5) Exit")


def view_data():
    with open (filename, "r") as f:
        temp = json.load(f)
        i = 0
        for entry in temp:
            username = entry["username"]
            stat_1 = entry["stat1"]
            stat_2 = entry["stat2"]
            stat_3 = entry["stat3"]
            print(f"Index Number {i}")
            print(f"Username: {username}")
            print(f"Stat 1: {stat_1}")
            print(f"Stat 2: {stat_2}")
            print(f"Stat 3: {stat_3}")
            print("\n\n")
            i = i+1


def delete_data():
    view_data()
    new_data = []
    with open(filename, "r") as f:
        temp = json.load(f)
        data_length = len(temp)-1
    print("Which index would you like to delete?")
    delete_option = input(f"Select number from 0 - {data_length}")
    i = 0
    for entry in temp:
        if i == int(delete_option):
            pass
            i = i+1
        else:
            new_data.append(entry)
            i = i+1
    with open(filename, "w") as f:
        json.dump(new_data, f, indent=4)


def edit_data():
    view_data()
    new_data = []
    with open(filename, "r") as f:
        temp = json.load(f)
        data_length = len(temp)-1
    print("Which index would you like to edit?")
    edit_option = input(f"Select number from 0 - {data_length}")
    i = 0
    for entry in temp:
        if i == int(edit_option):
            username = input(f"Username: ")
            stat_1 = input(f"Stat 1: ")
            stat_2 = input(f"Stat 2: ")
            stat_3 = input(f"Stat 3: ")
            new_data.append({"username": username, "stat1": stat_1, "stat2": stat_2, "stat3": stat_3})
            i = i + 1
        else:
            new_data.append(entry)
            i = i+1
    with open(filename, "w") as f:
        json.dump(new_data, f, indent=4)


def add_data():
    item_data = {}
    with open(filename, "r") as f:
        temp = json.load(f)
    item_data["username"] = input("Username: ")
    item_data["stat1"] = input("Stat 1: ")
    item_data["stat2"] = input("Stat 2: ")
    item_data["stat3"] = input("Stat 3: ")
    temp.append(item_data)
    with open(filename, "w") as f:
        json.dump(temp, f, indent=4)
        

while True:
    Choices()
    choice = input("\n Enter Number: ")
    if choice == "1":
        view_data()
    if choice == "2":
        add_data()
    if choice == "3":
        edit_data()
    if choice == "4":
        delete_data()
    if choice == "5":
        break
