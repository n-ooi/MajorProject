import json
from datetime import datetime

import numpy_financial as np
import pandas as pd
from cryptography.fernet import Fernet
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.textfield import MDTextField

results = ""
current_user = ""
entryNum = ""
pauseJSON = False

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


with open('login-details.csv', 'r') as f:
    if f.read()[0:8] == 'Username':
        encrypt('login-details.csv')

with open('user_data.json', 'r') as f:
    if f.read()[0] == '[':
        encrypt('user_data.json')


class Content(GridLayout):
    pass

class ItemConfirm(OneLineAvatarIconListItem):
    divider = None

    def set_icon(self, instance_check):
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False

        print(f"Selected {self.ids._lbl_primary.text}")
        global entryNum
        entryNum = int((self.ids._lbl_primary.text).split()[-1])


class SelectionButton(MDFlatButton):
    def test_fn(self):
        MDApp.get_running_app().switch_screen("Calc")


class Calc(Screen):
    def on_enter(self):
        print("Calc Page Loaded...")
        filename = "user_data.json"


    def update_entry(self, x):
        global entryNum
        global current_user
        print(f"searching for {current_user} - {entryNum}")
        filename = 'user_data.json'
        decrypt(filename)
        with open(filename, "r") as f:
            temp = json.load(f)
            i = 0
            entryIndex = 0

            for entry in temp:
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

                if username == current_user:
                    entryIndex = entryIndex + 1
                    if entryIndex == entryNum:
                        print(f"{current_user}'s {entryNum}th entry:")
                        print(f"Username: {username}")
                        print(f"Cost: {car_cost}")
                        print(f"Distance: {distance_travelled}")
                        print(f"Term: {lease_term}")
                        print(f"Size: {car_size}")
                        print(f"Salary: {salary_income}")

                        self.ids.carCost.value = car_cost
                        self.ids.annualDistance.value = distance_travelled
                        self.ids.preTaxIncome.value = salary_income

                        if lease_term == 1:
                            self.ids.term1.active = True
                        elif lease_term == 2:
                            self.ids.term2.active = True
                        elif lease_term == 3:
                            self.ids.term3.active = True
                        elif lease_term == 4:
                            self.ids.term4.active = True

                        if car_size == "small True":
                            self.ids.size1.active = True
                        elif car_size == "medium True":
                            self.ids.size2.active = True
                        elif car_size == "large True":
                            self.ids.size3.active = True
                        elif car_size == "sports True":
                            self.ids.size4.active = True

                        print(inc1, inc2, inc3, inc4)
                        if inc1:
                            self.ids.inc1.active = True
                        if inc2:
                            self.ids.inc2.active = True
                        if inc3:
                            self.ids.inc4.active = True
                        if inc4:
                            self.ids.inc4.active = True

                i = i + 1
        encrypt('user_data.json')
        global pauseJSON
        pauseJSON = True
        self.calc_values(self.ids.carCost.value, self.ids.annualDistance.value, self.ids.term1.active, self.ids.term2.active, self.ids.term3.active, self.ids.term4.active,
                            self.ids.size1.active, self.ids.size2.active, self.ids.size3.active, self.ids.size4.active, self.ids.preTaxIncome.value, self.ids.inc1.active, self.ids.inc2.active, self.ids.inc3.active, self.ids.inc4.active)
        pauseJSON = False



    def manager_screen(self):

        filename = "user_data.json"
        decrypt(filename)

        stuff = []

        with open(filename, "r") as f:
            temp = json.load(f)
            entryIndex = 0
            for entry in temp:
                username = entry["username"]
                time = entry["time"]
                if username == current_user:
                    entryIndex = entryIndex + 1
                    stuff.insert(0, ItemConfirm(text=f"{time} - Submission {entryIndex}"))

        window = MDDialog(
            title="Past Entries",
            type="confirmation",
            items=stuff,
            buttons=[
                SelectionButton(
                    text="SELECT", on_release=self.update_entry
                ),
            ],
        )
        window.open()
        encrypt(filename)

    def tax_calculate(self, taxable_income):
        tax = 0
        if 0 < taxable_income <= 18200:
            tax = 0
        elif 18200 < taxable_income <= 45000:
            tax = 0.19 * (taxable_income - 18200)
        elif 45000 < taxable_income <= 120000:
            tax = 5092 + .325 * (taxable_income - 45000)
        elif 120000 < taxable_income <= 180000:
            tax = 29467 + .37 * (taxable_income - 120000)
        elif taxable_income > 180000:
            tax = 51667 + .45 * (taxable_income - 180000)
        else:
            print("ERROR - Taxable income not valid: [", taxable_income, "]")

        # IDEK WHAT THESE DO
        if taxable_income > 18200:
            tax = tax + taxable_income * .02

        if 18200 <= taxable_income <= 37000:
            tax = tax - 255
        elif 37000 < taxable_income <= 48000:
            tax = tax - 255 - .075 * (taxable_income - 37000)
        elif 48000 < taxable_income <= 90000:
            tax = tax - 1080
        elif 90000 < taxable_income <= 126000:
            tax = tax - 1080 + .03 * (taxable_income - 90000)

        # return TAX values
        return tax

    def edit_json(self, cost, distance, term, size, salary, inc1, inc2, inc3, inc4):
        filename = "user_data.json"
        print("json editing...")

        new_user = True

        def view_data():
            with open(filename, "r") as f:
                temp = json.load(f)
                i = 0
                for entry in temp:
                    username = entry["username"]
                    car_cost = entry["cost"]
                    distance_travelled = entry["distance"]
                    lease_term = entry["term"]
                    car_size = entry["size"]
                    salary_income = entry["salary"]
                    insurance = entry["insurance"]
                    roadside = entry["roadside"]
                    cleaning = entry["cleaning"]
                    servicing = entry["servicing"]

                    print(f"Index Number {i}")
                    print(f"Username: {username}")
                    print(f"Cost: {car_cost}")
                    print(f"Distance: {distance_travelled}")
                    print(f"Term: {lease_term}")
                    print(f"Size: {car_size}")
                    print(f"Salary: {salary_income}")
                    print("\n\n")
                    i = i + 1

        def add_data():
            item_data = {}
            with open(filename, "r") as f:
                temp = json.load(f)
            item_data["time"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            item_data["username"] = current_user
            item_data["cost"] = cost
            item_data["distance"] = distance
            item_data["term"] = term
            item_data["size"] = size
            item_data["salary"] = salary
            item_data["insurance"] = inc1
            item_data["roadside"] = inc2
            item_data["cleaning"] = inc3
            item_data["servicing"] = inc4
            temp.append(item_data)
            with open(filename, "w") as f:
                json.dump(temp, f, indent=4)

        filename = "user_data.json"
        with open(filename, "r") as f:
            temp = json.load(f)
            for entry in temp:
                username = entry["username"]
                if username == current_user:
                    new_user = False

        if new_user:
            add_data()
        else:
            print("NOT NEW USER!!! EDITING EXISTING DATA")
            add_data()

    def entry_valid(self, carCost, annualDistance, term1, term2, term3, term4, size1, size2, size3, size4,
                    preTaxIncome, insurance, roadside, cleaning, servicing):
        print("checking validity...")
        if carCost == 0 or \
                annualDistance == 0 or \
                (term1 == False and term2 == False and term3 == False and term4 == False) or \
                (size1 == False and size2 == False and size3 == False and size4 == False):
            MDDialog(text="Check selections for errors.", ).open()
            return False
        else:
            return True

    def calc_values(self, carCost, annualDistance, term1, term2, term3, term4, size1, size2, size3, size4,
                    preTaxIncome, insurance, roadside, cleaning, servicing):
        if self.entry_valid(carCost, annualDistance, term1, term2, term3, term4, size1, size2, size3, size4,
                            preTaxIncome, insurance, roadside, cleaning, servicing):
            term = 0
            print('\n\n' + "Car Cost: " + str(int(carCost)))
            print("Distance: " + str(annualDistance))
            for i in (f'12 months {term1}', f'24 months {term2}', f'36 months {term3}', f'48 months {term4}'):
                if "True" in i:
                    print("Term Length: " + str(i.replace("True", "")))
                    term = int(i[0:1])

            for i in (f'small {size1}', f'medium {size2}', f'large {size3}', f'sports {size4}'):
                if "True" in i:
                    print("Car Size: " + str(i.replace("True", "")))
                    size = i
            print("Salary: " + str(preTaxIncome))

            # SETTING PARAMETERS UP
            car_size = size
            car_cost_GST = float(carCost)
            business_percentage = 0  # if there is time make this editable
            salary_income = float(preTaxIncome)
            residual_value = 0.4688  # if there is time make this editable
            kms_travelled_per_year = float(annualDistance)
            lease_term = term
            novated_interest_rate = 0.075  # if there is time make this editable
            standard_interest_rate = 0.03  # if there is time make this editable
            monthly_fee = 20  # if there is time make this editable

            if cleaning:
                cleaning_cost = 500
            else:
                cleaning_cost = 0

            if roadside:
                roadside_assist = 500
            else:
                roadside_assist = 0

            decrypt("user_data.json")
            global pauseJSON
            if not pauseJSON:
                self.edit_json(car_cost_GST, kms_travelled_per_year, lease_term, car_size, salary_income, insurance,roadside, cleaning, servicing)
            encrypt("user_data.json")

            # NORMAL COSTS CALCULATIONS
            aP = -(car_cost_GST - (car_cost_GST * residual_value))
            ar = standard_interest_rate / 12
            an = (lease_term * 12) - 2
            normal_financing = np.pmt(ar, an, aP) * 12
            if insurance:
                normal_insurance = (car_cost_GST * 0.04)
            else:
                normal_insurance = 0
            normal_fees = 0
            normal_registration = 800

            print(f"This is [{car_size}]")
            if car_size == "small True":
                fuel_consumption = 6
            elif car_size == "medium True":
                fuel_consumption = 7
            elif car_size == "large True":
                fuel_consumption = 8
            elif car_size == "sports True":
                fuel_consumption = 7.6

            normal_fuel = (((fuel_consumption * (kms_travelled_per_year / 100)) * 1.5) * 1.2)
            if servicing:
                normal_maintenance = 1500
            else:
                normal_maintenance = 0

            # NOVATED COSTS CALCULATIONS
            car_cost_GST_adjusted = car_cost_GST - (car_cost_GST / 11)
            if car_cost_GST > 69152:
                car_cost_GST_adjusted = car_cost_GST - (69152 * .1)
            bP = -(car_cost_GST_adjusted - (car_cost_GST_adjusted * residual_value))
            br = novated_interest_rate / 12
            bn = (lease_term * 12) - 2
            novated_financing = np.pmt(br, bn, bP) * 12
            novated_insurance = normal_insurance - normal_insurance / 11
            novated_roadside = roadside_assist - roadside_assist / 11
            novated_cleaning = cleaning_cost - cleaning_cost / 11
            novated_fees = 12 * monthly_fee
            novated_registration = normal_registration
            novated_fuel = (normal_fuel - normal_fuel / 11)
            novated_maintenance = normal_maintenance - normal_maintenance / 11

            # NOVATED TAX/INCOME CALCULATIONS
            novated_total = novated_roadside + novated_cleaning + novated_financing + novated_insurance + novated_fees + novated_registration + novated_fuel + novated_maintenance
            novated_less_post_tax_deduction = (car_cost_GST * .2) * (1 - business_percentage)
            novated_less_pre_tax_deduction = novated_total + (novated_less_post_tax_deduction / 11 - novated_less_post_tax_deduction)
            novated_taxable_income = salary_income - novated_less_pre_tax_deduction
            novated_less_tax = self.tax_calculate(novated_taxable_income)  # for some reason different to calculator
            novated_net_annual_income = novated_taxable_income - novated_less_tax
            novated_lease_final = novated_net_annual_income - novated_less_post_tax_deduction

            # NORMAL TAX/INCOME CALCULATIONS
            normal_total = roadside_assist + cleaning_cost + normal_financing + normal_insurance + normal_fees + normal_registration + normal_fuel + normal_maintenance
            normal_less_post_tax_deduction = normal_total
            normal_less_pre_tax_deduction = "-"
            normal_taxable_income = salary_income
            normal_less_tax = self.tax_calculate(normal_taxable_income)  #
            normal_net_annual_income = normal_taxable_income - normal_less_tax
            normal_lease_final = normal_net_annual_income - normal_less_post_tax_deduction


            # SAVINGS
            tax_savings = novated_lease_final - normal_lease_final
            money_savings = tax_savings + normal_total - novated_total

            print("Standard PMT: " + str(np.pmt(ar, an, aP) * 12))
            print("Normal Financing: " + str(normal_financing))
            print("Normal Insurance: " + str(normal_insurance))
            print("Normal Fuel: " + str(normal_fuel))
            print("Normal Maintenance: " + str(normal_maintenance))

            print("Novated PMT: " + str(np.pmt(br, bn, bP) * 12))
            print("Novated Financing: " + str(novated_financing))
            print("Novated Insurance: " + str(novated_insurance))
            print("Novated Fuel: " + str(novated_fuel))
            print("Novated Maintenance: " + str(novated_maintenance))

            print("\033[1;31;50m" + "Novated Total: " + str(novated_total) + "\033[0m")
            print("Novated Post Tax: " + str(novated_less_post_tax_deduction))
            print("Novated Pre Tax: " + str(novated_less_pre_tax_deduction))
            print("Novated Taxable Income: " + str(novated_taxable_income))
            print("Novated Less Tax: " + str(novated_less_tax))
            print("Novated Net Annual Income: " + str(novated_net_annual_income))
            print("\033[1;31;50m" + "Novated Final: " + str(novated_lease_final) + "\033[0m")
            print("\033[1;31;50m" + "Normal Total: " + str(normal_total) + "\033[0m")
            print("Normal Post Tax: " + str(normal_less_post_tax_deduction))
            print("Normal Pre Tax: " + str(normal_less_pre_tax_deduction))
            print("Normal Taxable Income: " + str(normal_taxable_income))
            print("Normal Less Tax: " + str(normal_less_tax))
            print("Normal Net Annual Income: " + str(normal_net_annual_income))
            print("\033[1;31;50m" + "Normal Final: " + str(normal_lease_final) + "\033[0m")
            print("\033[1;33;50m" + "Tax Savings: " + str(tax_savings) + "\033[0m")
            print("\033[1;33;50m" + "Money Savings: " + str(money_savings) + "\033[0m")

            label1 = Label(color="black", text=f"\n\nWithout Novated Lease: \n " + \
                                               f"------------------------------ \n" + \
                                               f"Financial Lease: ${round(normal_financing, 2)} \n" + \
                                               f"Registration: ${round(normal_registration, 2)} \n" + \
                                               f"Fuel: ${round(normal_fuel, 2)} \n" + \
                                               f"Maintenance/Servicing: ${round(normal_maintenance, 2)} \n" + \
                                               f"Insurance: ${round(normal_insurance, 2)} \n" + \
                                               f"Cleaning: ${round(cleaning_cost, 2)} \n" + \
                                               f"Roadside Assist: ${round(roadside_assist, 2)} \n" + \
                                               f"Fees: N/A \n" + \
                                               f"------------------------------ \n" + \
                                               f"Normal Total: ${round(normal_total, 2)} \n")

            label2 = Label(color="black", text=f"\n\nWith Novated Lease: \n " + \
                                               f"------------------------------ \n" + \
                                               f"Financial Lease: ${round(novated_financing, 2)} \n" + \
                                               f"Registration: ${round(novated_registration, 2)} \n" + \
                                               f"Fuel: ${round(novated_fuel, 2)} \n" + \
                                               f"Maintenance/Servicing: ${round(novated_maintenance, 2)} \n" + \
                                               f"Insurance: ${round(novated_insurance, 2)} \n" + \
                                               f"Cleaning: ${round(novated_cleaning, 2)} \n" + \
                                               f"Roadside Assist: ${round(novated_roadside, 2)} \n" + \
                                               f"Fees: ${round(novated_fees, 2)} \n" + \
                                               f"------------------------------ \n" + \
                                               f"Novated Total: ${round(novated_total, 2)} \n")

            label3 = Label(color="black", text=f"Totals: \n " + \
                                               f"------------------------------ \n" + \
                                               f"Tax Savings: $" + str(round(tax_savings, 2)) + \
                                               f"\nYearly Payment: $" + str(round(novated_total, 2)) + \
                                               f"\nMonthly Payment: $" + str(round(novated_total / 12, 2)))

            content = Content()
            window = MDDialog(title="Results", type="custom", content_cls=content)
            content.add_widget(label1)
            content.add_widget(label2)
            content.add_widget(label3)
            window.open()

        # MDApp.get_running_app().switch_screen("results")


class Login(Screen):
    def on_enter(self):
        pass

    def password_view(self, passIcon):
        if passIcon == 'eye-off-outline':
            self.ids.LoginPassword.password = False
            self.ids.view.icon = "eye-outline"
        else:
            self.ids.LoginPassword.password = True
            self.ids.view.icon = "eye-off-outline"

    def login_validation(self, LoginUsername, LoginPassword, root):
        decrypt('login-details.csv')
        check = pd.read_csv('login-details.csv')
        if LoginUsername not in check['Username'].unique():
            print("Username not found")
            MDDialog(text="Username or Password are incorrect.", ).open()
            pass  # deny access (Username not registered)
        else:
            user_info = check[['Username', 'Password']][check['Username'] == LoginUsername]
            user_password = user_info['Password'].values[0]
            if LoginPassword == user_password:
                if LoginUsername == 'admin':
                        MDApp.get_running_app().switch_screen("manager")
                else:
                    MDApp.get_running_app().switch_screen("Calc")
                print("Password Correct")
                global current_user
                current_user = LoginUsername
            else:
                print("Password Incorrect")
                MDDialog(text="Username or Password are incorrect.", ).open()
        encrypt('login-details.csv')


class SignUp(Screen):
    def on_enter(self):
        pass

    def password_view_su(self, passIcon, num):
        if num == 1:
            if passIcon == 'eye-off-outline':
                self.ids.SignUpPassword1.password = False
                self.ids.view1.icon = "eye-outline"
            else:
                self.ids.SignUpPassword1.password = True
                self.ids.view1.icon = "eye-off-outline"
        elif num == 2:
            if passIcon == 'eye-off-outline':
                self.ids.SignUpPassword2.password = False
                self.ids.view2.icon = "eye-outline"
            else:
                self.ids.SignUpPassword2.password = True
                self.ids.view2.icon = "eye-off-outline"

    def signupbtn(self, SignUpUsername, SignUpPassword1, SignUpPassword2, root):
        # creating a DataFrame of the info

        decrypt('login-details.csv')
        users = pd.read_csv('login-details.csv')
        user = pd.DataFrame([[SignUpUsername, SignUpPassword1]],
                            columns=['Username', 'Password'])
        if SignUpPassword2 != SignUpPassword1:
            MDDialog(text="Passwords don't match.", ).open()
        else:
            if SignUpUsername.isalnum():
                if SignUpUsername and SignUpPassword1:
                    if SignUpUsername not in users['Username'].unique():
                        # if Username does not exist already then append to the csv file
                        MDApp.get_running_app().switch_screen("login")  # to change current screen to log in the user now
                        user.to_csv('login-details.csv', mode='a', header=False, index=False)
                    else:
                        MDDialog(text="Username Taken.", ).open()
                else:
                    MDDialog(text="Some fields are missing or incorrect.", ).open()
            else:
                MDDialog(text="Username must be alphanumeric.", ).open()
        encrypt('login-details.csv')

data_stuff = []


class Manager(Screen):
    def on_enter(self):
        global data_stuff
        global current_user
        print(f"user = {current_user}")
        if current_user == 'admin':
            print("Access Approved - Building Screen...")
            filename = 'user_data.json'
            decrypt(filename)
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
                    data_stuff.insert(0,[i + 1, time, username, car_cost, distance_travelled, lease_term,
                                       car_size.replace(' True', '').replace(' False', ''), salary_income, inc1, inc2, inc3,
                                       inc4])
                    i = i + 1

            manager_data = BoxLayout(
                orientation='vertical',
                padding="20dp",
                spacing="20dp"
            )

            search_field = MDTextField(
                hint_text='Search',
                on_text_validate=self.update_data,
                size_hint_y=0.1,
            )

            toolbar = BoxLayout(
                orientation='horizontal',
                size_hint_y=.2,
            )

            toolbar.add_widget(Button(text="Return Home You Loser!", on_release=self.return_to_calc, background_color=(229/255,60/255,40/255,1),
                                      background_normal="off", font_name="font.otf", bold=True, font_size="50dp"))

            manager_data.add_widget(toolbar)
            manager_data.add_widget(search_field)

            self.data_tables = MDDataTable(
                use_pagination=True,
                pagination_menu_pos='center',
                rows_num=10,
                column_data=[
                    ("ID", dp(10)),
                    ("Time/Date", dp(40)),
                    ("Username", dp(30)),
                    ("Car Cost", dp(20)),
                    ("Annual Distance", dp(20)),
                    ("Lease Term", dp(10)),
                    ("Car Size", dp(20)),
                    ("Salary/Income", dp(25)),
                    ("Insurance", dp(20)),
                    ("Roadside Assist", dp(20)),
                    ("Cleaning", dp(20)),
                    ("Servicing", dp(20))
                ],
                row_data=data_stuff
            )
            manager_data.add_widget(self.data_tables)
            encrypt(filename)
            self.add_widget(manager_data)

            return self



    def update_data(self, instance):
        global data_stuff
        self.data_tables.row_data = data_stuff
        search_query = instance.text.lower()
        filtered_data = [row for row in self.data_tables.row_data if search_query in str(row).lower()]
        self.data_tables.row_data = filtered_data

    def return_to_calc(self, instance):
        MDApp.get_running_app().switch_screen("login")

    def on_leave(self, *args):
        self.clear_widgets()


class WindowManager(ScreenManager):  # this class defines the ScreenManager
    pass


decrypt('login-details.csv')
users = pd.read_csv('login-details.csv')
encrypt('login-details.csv')

WindowManager().add_widget(Login(name='login'))
WindowManager().add_widget(SignUp(name='signup'))
WindowManager().add_widget(Calc(name='Calc'))
WindowManager().add_widget(Manager(name='manager'))


class EasyPeasyLeasy(MDApp):
    dialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_kv("main.kv")

    def switch_screen(self, screen_name, *args):
        self.root.current = screen_name


Window.fullscreen = 'auto'  # Sets the app's default state to fullscreen

if __name__ == '__main__':
    EasyPeasyLeasy().run()  # Opens the app
