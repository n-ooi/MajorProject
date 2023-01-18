import pandas as pd

users = pd.read_csv('login-details.csv')

user_info = users[['Email', 'Password']][users['Email'] == "hello"]

print(list(str(user_info).split(" "))[-1])