from kivymd.app import MDApp
from cryptography.fernet import Fernet
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
import pandas as pd
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import numpy_financial as np
import json

current_user = ""

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


class Calc(Screen):
    def on_enter(self):
        filename = "user_data.json"
        decrypt('user_data.json')
        with open(filename, "r") as f:
            temp = json.load(f)
            i = 0
            new = True
            for entry in temp:
                username = entry["username"]
                car_cost = entry["cost"]
                distance_travelled = entry["distance"]
                lease_term = entry["term"]
                car_size = entry["size"]
                salary_income = entry["salary"]

                if username == current_user:

                    new = False

                    print(f"Index Number {i}")
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

                i = i + 1
        encrypt('user_data.json')

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

    def edit_json(self, cost, distance, term, size, salary):
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

                    print(f"Index Number {i}")
                    print(f"Username: {username}")
                    print(f"Cost: {car_cost}")
                    print(f"Distance: {distance_travelled}")
                    print(f"Term: {lease_term}")
                    print(f"Size: {car_size}")
                    print(f"Salary: {salary_income}")
                    print("\n\n")
                    i = i + 1

        def edit_data():
            new_data = []
            with open(filename, "r") as f:
                temp = json.load(f)
                i = 0
                edit_option = 0
                for entry in temp:
                    if current_user == entry["username"]:
                        edit_option = i
                    i = i + 1
            i = 0

            for entry in temp:
                if i == int(edit_option):
                    new_data.append(
                        {"username": current_user, "cost": cost, "distance": distance, "term": term, "size": size,
                         "salary": salary})
                    i = i + 1
                    "doing stuff"
                else:
                    new_data.append(entry)
                    i = i + 1

            print(new_data)
            with open(filename, "w") as f:
                json.dump(new_data, f, indent=4)

        def add_data():
            item_data = {}
            with open(filename, "r") as f:
                temp = json.load(f)
            item_data["username"] = current_user
            item_data["cost"] = cost
            item_data["distance"] = distance
            item_data["term"] = term
            item_data["size"] = size
            item_data["salary"] = salary
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
            edit_data()

    def calc_values(self, carCost, annualDistance, term1, term2, term3, term4, size1, size2, size3, size4,
                    preTaxIncome):

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

        decrypt("user_data.json")
        self.edit_json(car_cost_GST, kms_travelled_per_year, lease_term, car_size, salary_income)
        encrypt("user_data.json")

        # NORMAL COSTS CALCULATIONS
        aP = -(car_cost_GST - (car_cost_GST * residual_value))
        ar = standard_interest_rate / 12
        an = (lease_term * 12) - 2

        print("Standard PMT: " + str(np.pmt(ar, an, aP) * 12))

        normal_financing = np.pmt(ar, an, aP) * 12
        normal_insurance = (car_cost_GST * 0.04)
        normal_fees = 0
        normal_registration = 800
        normal_fuel = (((7.6 * (kms_travelled_per_year / 100)) * 1.5) * 1.2)
        normal_maintenance = 1500

        print("Normal Financing: " + str(normal_financing))
        print("Normal Insurance: " + str(normal_insurance))
        print("Normal Fuel: " + str(normal_fuel))
        print("Normal Maintenance: " + str(normal_maintenance))

        # NOVATED COSTS CALCULATIONS
        car_cost_GST_adjusted = car_cost_GST - (car_cost_GST / 11)
        if car_cost_GST > 69152:
            car_cost_GST_adjusted = car_cost_GST - (69152 * .1)

        bP = -(car_cost_GST_adjusted - (car_cost_GST_adjusted * residual_value))
        br = novated_interest_rate / 12
        bn = (lease_term * 12) - 2

        print("Novated PMT: " + str(np.pmt(br, bn, bP) * 12))

        novated_financing = np.pmt(br, bn, bP) * 12
        novated_insurance = normal_insurance - normal_insurance / 11
        novated_fees = 12 * monthly_fee
        novated_registration = normal_registration
        novated_fuel = (normal_fuel - normal_fuel / 11)
        novated_maintenance = normal_maintenance - normal_maintenance / 11

        print("Novated Financing: " + str(novated_financing))
        print("Novated Insurance: " + str(novated_insurance))
        print("Novated Fuel: " + str(novated_fuel))
        print("Novated Maintenance: " + str(novated_maintenance))

        # NOVATED TAX/INCOME CALCULATIONS
        novated_total = novated_financing + novated_insurance + novated_fees + novated_registration + novated_fuel + novated_maintenance
        print("\033[1;31;50m" + "Novated Total: " + str(novated_total) + "\033[0m")

        novated_less_post_tax_deduction = (car_cost_GST * .2) * (1 - business_percentage)
        print("Novated Post Tax: " + str(novated_less_post_tax_deduction))

        novated_less_pre_tax_deduction = novated_total + (
                novated_less_post_tax_deduction / 11 - novated_less_post_tax_deduction)
        print("Novated Pre Tax: " + str(novated_less_pre_tax_deduction))

        novated_taxable_income = salary_income - novated_less_pre_tax_deduction
        print("Novated Taxable Income: " + str(novated_taxable_income))

        novated_less_tax = self.tax_calculate(novated_taxable_income)  # for some reason different to calculator
        print("Novated Less Tax: " + str(novated_less_tax))

        novated_net_annual_income = novated_taxable_income - novated_less_tax
        print("Novated Net Annual Income: " + str(novated_net_annual_income))

        novated_lease_final = novated_net_annual_income - novated_less_post_tax_deduction
        print("\033[1;31;50m" + "Novated Final: " + str(novated_lease_final) + "\033[0m")

        # NORMAL TAX/INCOME CALCULATIONS
        normal_total = normal_financing + normal_insurance + normal_fees + normal_registration + normal_fuel + normal_maintenance
        print("\033[1;31;50m" + "Normal Total: " + str(normal_total) + "\033[0m")

        normal_less_post_tax_deduction = normal_total
        print("Normal Post Tax: " + str(normal_less_post_tax_deduction))

        normal_less_pre_tax_deduction = "-"
        print("Normal Pre Tax: " + str(normal_less_pre_tax_deduction))

        normal_taxable_income = salary_income
        print("Normal Taxable Income: " + str(normal_taxable_income))

        normal_less_tax = self.tax_calculate(normal_taxable_income)  # for some reason different to calculator
        print("Normal Less Tax: " + str(normal_less_tax))

        normal_net_annual_income = normal_taxable_income - normal_less_tax
        print("Normal Net Annual Income: " + str(normal_net_annual_income))

        normal_lease_final = normal_net_annual_income - normal_less_post_tax_deduction
        print("\033[1;31;50m" + "Normal Final: " + str(normal_lease_final) + "\033[0m")

        # SAVINGS
        tax_savings = novated_lease_final - normal_lease_final
        print("\033[1;33;50m" + "Tax Savings: " + str(tax_savings) + "\033[0m")

        money_savings = tax_savings + normal_total - novated_total
        print("\033[1;33;50m" + "Money Savings: " + str(money_savings) + "\033[0m")

        window = MDDialog(text="Tax Savings: \n$" + str(round(tax_savings, 2)), )
        window.open()


class Login(Screen):
    def on_enter(self):
        pass

    def login_validation(self, LoginUsername, LoginPassword, root):
        decrypt('login-details.csv')
        check = pd.read_csv('login-details.csv')
        print(LoginUsername)
        print(LoginPassword)
        if LoginUsername not in check['Username'].unique():
            print("Username not found")
            MDDialog(text="Username or Password are incorrect.", ).open()
            pass  # deny access (Username not registered)
        else:
            user_info = check[['Username', 'Password']][check['Username'] == LoginUsername]
            print(user_info)
            user_password = list(str(user_info).split(" "))[-1]
            print(user_password)
            if LoginPassword == user_password:
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

    def signupbtn(self, SignUpUsername, SignUpPassword1, SignUpPassword2, root):
        # creating a DataFrame of the info

        decrypt('login-details.csv')
        users = pd.read_csv('login-details.csv')
        user = pd.DataFrame([[SignUpUsername, SignUpPassword1]],
                            columns=['Username', 'Password'])
        if SignUpPassword2 != SignUpPassword1:
            MDDialog(text="Passwords don't match.", ).open()
        else:
            if SignUpUsername and SignUpPassword1:
                if SignUpUsername not in users['Username'].unique():
                    print("UNIQUE USERNAME: " + SignUpUsername + "\n")
                    print(users['Username'].unique())
                    # if Username does not exist already then append to the csv file
                    MDApp.get_running_app().switch_screen("login")  # to change current screen to log in the user now
                    user.to_csv('login-details.csv', mode='a', header=False, index=False)
                else:
                    MDDialog(text="Username Taken.", ).open()
            else:
                MDDialog(text="Some fields are missing or incorrect.", ).open()
        encrypt('login-details.csv')

class WindowManager(ScreenManager):  # this class defines the ScreenManager
    pass

decrypt('login-details.csv')
users = pd.read_csv('login-details.csv')
encrypt('login-details.csv')

WindowManager().add_widget(Login(name='login'))
WindowManager().add_widget(SignUp(name='signup'))
WindowManager().add_widget(Calc(name='Calc'))


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
