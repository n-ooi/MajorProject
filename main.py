from kivymd.app import MDApp

from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
import pandas as pd
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton


class Calc(Screen):
    def on_enter(self):
        pass

    def calc_values(self, leaseBudget, annualDistance, term1, term2, term3, term4, size1, size2, size3, size4, salaryResidual):
        term, size = 0
        print('\n\n'+str(int(leaseBudget)))
        print(int(annualDistance))
        for i in (f'12 months {term1}', f'24 months {term2}', f'36 months {term3}', f'48 months {term4}'):
            if "True" in i:
                print(str(i.replace("True", "")))
                term = i

        for i in (f'small {size1}', f'medium {size2}', f'large {size3}', f'sports {size4}'):
            if "True" in i:
                print(str(i.replace("True", "")))
                size = i
        print(int(salaryResidual))

        car_cost_GST = leaseBudget
        business_percentage = 0
        taxable_income = salaryResidual
        residual_value = ("65%", "56%", "46%", "37%")
        kms_travelled_per_year = annualDistance
        lease_term = term
        novated_interest_rate = "between 5% and 10%"
        standard_interest_rate = "between 3% and 4%"
        monthly_fee = 20
        car_size = size


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
            pass # deny access (Username not registered)
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
                    MDApp.get_running_app().switch_screen("login") # to change current screen to log in the user now
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
