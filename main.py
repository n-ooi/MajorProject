from kivymd.app import MDApp

from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
import pandas as pd
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import numpy_financial as np


class Calc(Screen):
    def on_enter(self):
        pass

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
            tax = tax - 1080 + .03*(taxable_income - 90000)

        # return TAX values
        return tax

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
        car_cost_GST = float(carCost)
        business_percentage = 0   # if there is time make this editable
        salary_income = float(preTaxIncome)
        residual_value = 0.4688  # if there is time make this editable
        kms_travelled_per_year = float(annualDistance)
        lease_term = term
        novated_interest_rate = 0.075  # if there is time make this editable
        standard_interest_rate = 0.03  # if there is time make this editable
        monthly_fee = 20  # if there is time make this editable

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
            car_cost_GST_adjusted = car_cost_GST - (69152*.1)

        bP = -(car_cost_GST_adjusted - (car_cost_GST_adjusted * residual_value))
        br = novated_interest_rate / 12
        bn = (lease_term * 12) - 2

        print("Novated PMT: " + str(np.pmt(br, bn, bP) * 12))

        novated_financing = np.pmt(br, bn, bP) * 12
        novated_insurance = normal_insurance - normal_insurance / 11
        novated_fees = 12 * monthly_fee
        novated_registration = normal_registration
        novated_fuel = normal_fuel - normal_fuel / 11
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

        # TAX SAVINGS
        tax_savings = novated_lease_final - normal_lease_final
        print("\033[1;33;50m" + "Tax Savings: " + str(tax_savings) + "\033[0m")


class Login(Screen):
    def on_enter(self):
        pass

    def loginFail(self):
        window = MDDialog(text="Username or Password are incorrect.", )
        window.open()

    def login_validation(self, LoginUsername, LoginPassword, root):
        check = pd.read_csv('login-details.csv')
        print(LoginUsername)
        print(LoginPassword)
        if LoginUsername not in check['Username'].unique():
            print("Username not found")
            self.loginFail()
            pass  # deny access (Username not registered)
        else:
            user_info = check[['Username', 'Password']][check['Username'] == LoginUsername]
            print(user_info)
            user_password = list(str(user_info).split(" "))[-1]
            print(user_password)
            if LoginPassword == user_password:
                MDApp.get_running_app().switch_screen("Calc")
                print("Password Correct")
            else:
                print("Password Incorrect")
                self.loginFail()


class SignUp(Screen):
    def on_enter(self):
        self.clearValues()

    def clearValues(self):
        pass

    def passwordMismatch(self):
        window = MDDialog(text="Passwords don't match.", )
        window.open()

    def missingFields(self):
        window = MDDialog(text="Some fields are missing or incorrect.", )
        window.open()

    def signupbtn(self, SignUpUsername, SignUpPassword1, SignUpPassword2, root):
        # creating a DataFrame of the info
        user = pd.DataFrame([[SignUpUsername, SignUpPassword1]],
                            columns=['Username', 'Password'])
        if SignUpPassword2 != SignUpPassword1:
            self.passwordMismatch()
        else:
            if SignUpUsername and SignUpPassword1:
                if SignUpUsername not in users['Username'].unique():
                    # if Username does not exist already then append to the csv file
                    MDApp.get_running_app().switch_screen("login")  # to change current screen to log in the user now
                    user.to_csv('login-details.csv', mode='a', header=False, index=False)
                    # self.SignUpUsername.text = ""
                    # self.SignUpPassword1.text = ""
            else:
                self.missingFields()


class WindowManager(ScreenManager):  # this class defines the ScreenManager
    pass


users = pd.read_csv('login-details.csv')

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
