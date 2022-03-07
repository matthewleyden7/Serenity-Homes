import csv
import datetime

class DataBase:
    def __init__(self, filename):
        self.filename = filename
        self.users = {}
        self.rows = []
        self.file = None
        self.load_users()

    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(" ")[0]

    def load_users(self):
        with open('db/users.csv', 'r') as file:
            self.file = csv.reader(file)
            for row in self.file:
                self.users[row[0]] = (row[1], row[2], row[3])
                self.rows.append(row)


    def confirm(self, username, password):
        if self.get_user(username) != -1:
            return self.users[username][0] == password
        else:
            return False

    def get_user(self, username):
        if username in self.users:
            return self.users[username]
        else:
            return -1

    def add_user(self, username, password, name):
        if username.strip() not in self.users:
            self.users[username.strip()] = (password.strip(), name.strip(), DataBase.get_date())
            self.rows.append([username.strip(), password.strip(), name.strip(), DataBase.get_date()])
            self.save()
            return 1
        else:
            print("Username already exists")
            return -1

    def save(self):
        with open('db/users.csv', 'w', newline='') as file:
            csvwriter = csv.writer(file)
            csvwriter.writerows(self.rows)

