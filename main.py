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


class Login(Screen):
    def on_enter(self):
        pass

    def loginFail(self):
        window = MDDialog(text="Email or Password are incorrect.", )
        window.open()

    def login_validation(self, LoginEmail, LoginPassword, root):
        check = pd.read_csv('login-details.csv')
        print(LoginEmail)
        print(LoginPassword)
        if LoginEmail not in check['Email'].unique():
            print("Email not found")
            self.loginFail()
            pass # deny access (email not registered)
        else:
            user_info = check[['Email', 'Password']][check['Email'] == LoginEmail]
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
        pass

    def passwordMismatch(self):
        window = MDDialog(text="Passwords don't match.", )
        window.open()

    def missingFields(self):
        window = MDDialog(text="Some fields are missing or incorrect.", )
        window.open()

    def signupbtn(self, SignUpEmail, SignUpPassword1, SignUpPassword2, root):
        # creating a DataFrame of the info
        user = pd.DataFrame([[SignUpEmail, SignUpPassword1]],
                            columns=['Email', 'Password'])
        if SignUpPassword2 != SignUpPassword1:
            self.passwordMismatch()
        else:
            if SignUpEmail != "" and SignUpPassword1 != "":
                if SignUpEmail not in users['Email'].unique():
                    # if email does not exist already then append to the csv file
                    MDApp.get_running_app().switch_screen("login") # to change current screen to log in the user now
                    user.to_csv('login-details.csv', mode='a', header=False, index=False)
                    # self.SignUpEmail.text = ""
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
