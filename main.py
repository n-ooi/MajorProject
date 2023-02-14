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

    def calc_values(self, leaseBudget, annualDistance, term1, term2, term3, term4, size1, size2, size3, size4,
                    salaryResidual):
        term = 0
        print('\n\n' + "Lease Budget: " + str(int(leaseBudget)))
        print("Distance: " + str(annualDistance))
        for i in (f'12 months {term1}', f'24 months {term2}', f'36 months {term3}', f'48 months {term4}'):
            if "True" in i:
                print("Term Length: " + str(i.replace("True", "")))
                term = int(i[0:1])

        for i in (f'small {size1}', f'medium {size2}', f'large {size3}', f'sports {size4}'):
            if "True" in i:
                print("Car Size: " + str(i.replace("True", "")))
                size = i
        print("Salary: " + str(salaryResidual))

        car_cost_GST = float(leaseBudget)
        business_percentage = 0
        salary_income = float(salaryResidual)
        residual_value = 0.4688
        kms_travelled_per_year = float(annualDistance)
        lease_term = term
        novated_interest_rate = 0.075
        standard_interest_rate = 0.03
        monthly_fee = 20

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

        normal_total = normal_financing + normal_insurance + normal_fees + normal_registration + normal_fuel + normal_maintenance

        car_cost_GST_adjusted = car_cost_GST - (car_cost_GST/11)

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

        novated_total = novated_financing + novated_insurance + novated_fees + novated_registration + novated_fuel + novated_maintenance

        # less_pre_tax_deduction = novated_total + (less_post_tax_deduction/11 - less_post_tax_deduction)
        # less_post_tax_deduction =
        # taxable_income = salary_income - less_pre_tax_deduction


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
