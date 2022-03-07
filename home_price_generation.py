from kivy.config import Config
Config.set('graphics', 'resizable', False)
import pandas as pd
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.core.window import Window
import pickle
import numpy as np
import os
import csv
import time
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from db.database import DataBase
from k_means_clustering import create_k_means_clusters
from csv import writer
from train_model import train_decision_regressor

# This program provides the logic of the application. The design and structure is programmed in the accompanying
# serenity.kv file.


# Uses the database.py file to load the users
db = DataBase("users.csv")


class Widgets(Widget):
    def btn(self):
        show_message()

# Logic of the Login screen. Access the database to verify username and password.
class Login(Screen):

    username = ObjectProperty(None)
    password = ObjectProperty(None)
    verification = ObjectProperty(None)

    def reset(self):
        self.username.text = ''
        self.password.text = ''
        self.verification.text = ''

    def btn(self):

        if self.username.text == '':
            show_message('Please enter a username')

        elif self.password.text == '':
            show_message('Please enter a password')

        else:
            if db.confirm(self.username.text, self.password.text):
                self.ids.verification.text = 'validated'
            else:
                show_message('You entered an invalid username or password. Please try again.')

# Used to add a new user
class AddNewUser(Screen):
    employee_name = ObjectProperty(None)
    username = ObjectProperty(None)
    password = ObjectProperty(None)

    def add_user(self):
        db.add_user(self.ids.username.text, self.ids.password.text, self.ids.employee_name.text)
        show_message(f'User {self.ids.username.text} has been added!')

# Logic of the train new model screen. Uses the train method of train_model.py
class TrainModel(Screen):
    training_label = StringProperty("")
    saved_label = ObjectProperty(None)
    accuracy_label = ObjectProperty(None)

    def set_training_label(self):
        self.training_label = 'Training the model. Please wait...'
        time.sleep(1)
        self.train_new_model()

    def train_new_model(self):

        accuracy = train_decision_regressor('data/modified_house_data.csv')
        self.ids.saved_label.text = 'New model saved'
        self.ids.accuracy_label.text = f'Test accuracy of new model is {str(accuracy)}'

# Used to show popup messages and error messages
def show_message(message):
    show = P()
    popupWindow = Popup(title=message, content=show, size_hint=(None, None), size=(400, 75))
    popupWindow.open()

# Logic of the properties screen. Grabs data from the homes.csv file and arranges house pictures and information in
# a grid layout.
class Properties(Screen):

    def __init__(self, **kwargs):
        # Initiate Box Layout and change orientation to vertical
        super().__init__(**kwargs)

        self.orientation = "vertical"

        # Create the Gridlayout for the Scroll View and add height bounding
        self.contend_scroll_view = GridLayout(size_hint_y=None, row_default_height=200, cols=2, padding=50)
        self.contend_scroll_view.bind(minimum_height=self.contend_scroll_view.setter('height'))


        all_rows = []
        with open('homes.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                # row = row[:12] + row[14:]
                all_rows.append(row)

        for i, item in enumerate(all_rows):
            self.contend_scroll_view.add_widget(AsyncImage(source=item[-1], size_hint=(None, None), height=150, width=200))
            self.contend_scroll_view.add_widget(Label(text=f'Price: {item[0]}\nBedrooms: {item[1]}\nBathrooms: {item[2]}\nSquare Feet: {item[3]}'))
        # Add the contend to the Scroll View
        self.scroll_view = ScrollView()
        self.scroll_view.add_widget(self.contend_scroll_view)

        # Add the two Widgets to Home Screen
        #self.add_widget(self.top_bar)
        self.add_widget(self.scroll_view)


class MainScreen(Screen):
    pass

class P(FloatLayout):
    pass

# Provides the algorithms for the Price Quote screen. When a user enters features of home and presses the generate price
# button, checks for errors, converts user-entered strings to float values, arranges into a numpy array, and queries the
# the model. The model predicts a price which is then shown on the screen through the pricequote object property. The
# values are recorded on the prev_values.txt so user can reload the values later.
class PriceGenerator(Screen):
    with open('model/new_model.pkl', 'rb') as fid:
        generator = pickle.load(fid)

    bedrooms = ObjectProperty(None)
    bathrooms = ObjectProperty(None)
    sqft_living = ObjectProperty(None)
    sqft_lot = ObjectProperty(None)
    floors = ObjectProperty(None)
    waterfront = ObjectProperty(None)
    view = ObjectProperty(None)
    condition = ObjectProperty(None)
    grade = ObjectProperty(None)
    year_built = ObjectProperty(None)
    year_renovated = ObjectProperty(None)
    zip = ObjectProperty(None)
    pricequote = ObjectProperty(None)
    answer = 0
    row = []

    # Dictionaries used to convert float values to understandable strings and back
    condition_dict = {'very poor': 1.0, 'poor': 2.0, 'fair': 3.0, 'good': 4.0, 'very good': 5.0}
    condition_dict_reversed = {'1.0': 'very poor', '2.0': 'poor', '3.0': 'fair', '4.0': 'good', '5.0': 'very good'}
    view_dict = {'none': 0.0, 'somewhat': 1.0, 'nice': 2.0, 'very nice': 3.0, 'beautiful': 4.0}
    view_dict_reversed = {'0.0': 'none', '1.0': 'somewhat', '2.0': 'nice', '3.0': 'very nice', '4.0': 'beautiful'}
    yesno_dict = {'no': 0.0, 'yes': 1.0}
    yesno_dict_reversed = {'0.0': 'no', '1.0': 'yes'}

    # If user presses the load previous values button, values are loaded from the prev_values.txt and text input boxes
    # are set with previous values
    def set_values(self):
        if os.path.isfile('prev_values.txt'):
            with open('prev_values.txt', 'r') as f:
                values = f.read().split(',')

            self.ids.bedrooms.text, self.ids.bathrooms.text, self.ids.sqft_living.text, self.ids.sqft_lot.text,\
            self.ids.floors.text, self.ids.waterfront.text, self.ids.view.text, self.ids.condition.text, self.ids.grade.text,\
            self.ids.year_built.text, self.ids.year_renovated.text, self.ids.zip.text = values
            self.ids.waterfront.text = self.yesno_dict_reversed[self.ids.waterfront.text]
            self.ids.condition.text = self.condition_dict_reversed[self.ids.condition.text]
            self.ids.view.text = self.view_dict_reversed[self.ids.view.text]

        else:
            pass

    # Process the user entered values. Check for errors. Convert to float values. Query the model. Display results.
    def process_values(self):

        try: bedrooms = float(self.bedrooms.text)
        except:
            self.show_message('Please type a number for bedrooms')
            return
        try: bathrooms = float(self.bathrooms.text)
        except:
            self.show_message('Please type a number for bathrooms')
            return
        try:
            sqft_living = float(self.sqft_living.text)
        except:
            self.show_message('Please type a number for square feet of living space')
            return
        try:
            sqft_lot = float(self.sqft_lot.text)
        except:
            self.show_message('Please type a number for the square feet of the lot')
            return
        try:
            floors = float(self.floors.text)
        except:
            self.show_message('Please type the number of floors')
            return
        try:
            waterfront = self.yesno_dict[self.waterfront.text]
        except:
            self.show_message('Please type the number of waterfront')
            return
        try:
            view = self.view_dict[self.view.text]
        except:
            self.show_message('Please type the number of view')
            return
        try:
            condition = self.condition_dict[self.condition.text]
        except:
            self.show_message('Please type the number of condition')
            return
        try:
            grade = float(self.grade.text)
        except:
            self.show_message('Please choose the grade.')
            return
        try:
            year_built = float(self.year_built.text)
        except:
            self.show_message('Please type the year this property was built.')
            return
        try:
            year_renovated = float(self.year_renovated.text)
        except:
            self.show_message('Please type the year this property was renovated.')
            return
        try:
            zip = float(self.zip.text)
        except:
            self.show_message('Please type the zip code for this property')
            return
        if sqft_living > sqft_lot:
            self.show_message('The square footage of the lot should be greater than the square footage of living space.')
            return

        self.row = [bedrooms, bathrooms, sqft_living, sqft_lot, floors, waterfront, view, condition, grade, year_built, year_renovated, zip]

        array1 = np.array([self.row])
        self.answer = self.generator.predict(array1)

        self.answer = int(list(self.answer)[0])

        self.ids.pricequote.text = f'Suggested Price: {self.answer}'
        f = open('prev_values.txt', 'r+')
        f.truncate(0)
        with open('prev_values.txt', 'a', encoding='utf-8') as f:
            f.write(','.join([str(c) for c in self.row]))

    # Used to show popup messages and error messages
    def show_message(self, message):
        show = P()
        popupWindow = Popup(title=message, content=show, size_hint=(None, None), size=(400, 75))
        popupWindow.open()

# Logic of the DataKMeans screen.
class DataKMeans(Screen):
    variable1 = ObjectProperty(None)
    variable2 = ObjectProperty(None)
    num_clusters = ObjectProperty(None)
    elbow = StringProperty('k_means_images/elbow.png')
    clusters = StringProperty('k_means_images/clusters.png')
    scaled_clusters = StringProperty('k_means_images/scaled_clusters.png')
    centroids = StringProperty('k_means_images/centroids.png')
    cluster_button = ObjectProperty(None)
    count = 0

    # Evaluates user selected conditions, creates cluster images from the create_k_means_clusters method of k_means_clustering.py,
    # and updates the images on the screen.
    def evaluate(self):

        self.count += 1
        create_k_means_clusters(self.ids.variable1.text, self.ids.variable2.text, int(self.ids.num_clusters.text), self.count)

        self.elbow = f'k_means_images/elbow{self.count}.png'
        self.clusters = f'k_means_images/clusters{self.count}.png'
        self.scaled_clusters = f'k_means_images/scaled_clusters{self.count}.png'
        self.centroids = f'k_means_images/centroids{self.count}.png'
        #(os.remove(file) for file in os.listdir('k_means_images') if file.endswith('.png'))


# Method to display user selected graph on the explore the data screen
class DataExplorer(Screen):
    display = ObjectProperty(None)
    illustrations = ObjectProperty(None)
    def set_image(self):
        self.ids.display.source = 'data_images/' + self.ids.illustrations.text + '.png'

# Establish the WindowManager. The WindowManager handles all the screens listed at the top of the serenity.kv file
class WindowManager(ScreenManager):
    pass

# Load the .kv file which provides the majority of the design of the application
kv = Builder.load_file('serenity.kv')

# Starts the application and returns the loaded serenity.kv file.
class SerenityApp(App):
    def build(self):

        return kv

if __name__ == '__main__':
    SerenityApp().run()