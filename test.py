import json

from cryptography.fernet import Fernet
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable

with open('filekey.key', 'rb') as filekey:
    key = filekey.read()

fernet = Fernet(key)

file_name = 'data.json'


# noinspection PyShadowingNames
def decrypt(file_name):
    with open(file_name, 'rb') as enc_file:
        encrypted = enc_file.read()

    decrypted = fernet.decrypt(encrypted)

    with open(file_name, 'wb') as dec_file:
        dec_file.write(decrypted)


# noinspection PyShadowingNames
def encrypt(file_name):
    with open(file_name, 'rb') as file:
        original = file.read()

    encrypted = fernet.encrypt(original)

    with open(file_name, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)


class Example(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        data_stuff = []
        filename = 'user_data.json'
        with open(filename, "r") as f:
            temp = json.load(f)
            i = 0
            for entry in temp:
                time = entry["time"]
                username = entry["username"]
                car_cost = entry["cost"]
                distance_travelled = entry["distance"]
                lease_term = entry["term"]
                car_size = entry["size"]
                salary_income = entry["salary"]
                inc1 = entry["insurance"]
                inc2 = entry["roadside"]
                inc3 = entry["cleaning"]
                inc4 = entry["servicing"]
                data_stuff.append([i+1, time, username, car_cost, distance_travelled, lease_term, car_size.replace(' True', '').replace(' False', ''), salary_income, inc1, inc2, inc3, inc4])
                i = i + 1

        layout = AnchorLayout()
        data_tables = MDDataTable(
            size_hint=(0.9, 0.6),
            use_pagination=True,
            column_data=[
                ("No.", dp(30)),
                ("Time", dp(30)),
                ("Username", dp(30)),
                ("Car Cost", dp(30)),
                ("Annual Distance", dp(30)),
                ("Lease Term", dp(30)),
                ("Car Size", dp(30)),
                ("Salary/Income", dp(30)),
                ("Insurance", dp(30)),
                ("Roadside A", dp(30)),
                ("Cleaning", dp(30)),
                ("Servicing", dp(30))
            ],
            row_data=data_stuff
        )
        layout.add_widget(data_tables)
        return layout


Example().run()