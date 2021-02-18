# Project Twitter Sentiment Analysis

import os
import sys
# sys.setrecursionlimit(10**5)
# import pandas as pd
import sqlite3
import tweepy, csv, re
from textblob import TextBlob
from datetime import datetime
from matplotlib import pyplot as plt#, mpld3
from PyQt5.QtWidgets import QApplication, QMessageBox, QPushButton, QDialog, QLineEdit, QGridLayout, QLabel

database = sqlite3.connect("db.sqlite3")
database.execute('''CREATE TABLE IF NOT EXISTS "record" (
                "username"	        TEXT NOT NULL UNIQUE,
                "name"	            TEXT NOT NULL,
                "email"	            TEXT NOT NULL UNIQUE,
                "pwd"	            TEXT NOT NULL,
                "customerkey"	    TEXT NOT NULL,
                "customersecret"    TEXT NOT NULL,
                "accesstoken"	    TEXT NOT NULL,
                "accesstokensecret"	TEXT NOT NULL)''')
database.execute('''CREATE TABLE IF NOT EXISTS "result" (
                "id"	    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                "keyword"   TEXT,
                "tweet"	    TEXT)''')
cursor = database.cursor()


class SentimentAnalysis(QDialog):
    def __init__(self, extras):
        QDialog.__init__(self)

        # Creating Grid Layout
        layout = QGridLayout()

        # Window Title
        self.setWindowTitle("Sentiment Analysis")

        # Labels
        self.text1 = QLabel()
        self.text2 = QLabel()
        self.text1.setText("Keyword")
        self.text2.setText("Number of Tweets")

        # Push Buttons
        submit_button = QPushButton("Submit")
        close_button = QPushButton("Close")

        # Line Edit
        self.loc1 = QLineEdit(self)
        self.loc1.setPlaceholderText("Enter the keyword to search")

        self.loc2 = QLineEdit(self)
        self.loc2.setPlaceholderText("Enter the no. of tweets to search")

        # Layout
        layout.addWidget(self.loc1, 0, 1)
        layout.addWidget(self.loc2, 1, 1)
        layout.addWidget(self.text1, 0, 0)
        layout.addWidget(self.text2, 1, 0)
        layout.addWidget(submit_button, 2, 0)
        layout.addWidget(close_button, 2, 1)

        self.setLayout(layout)
        self.setFocus()
        self.extras = extras
        
        # Events and Signals
        submit_button.clicked.connect(self.DownloadData)
        close_button.clicked.connect(self.close)

        self.tweets = []
        self.tweetText = []

    # Remove Links, Special Characters etc from tweet
    def cleanTweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    # function to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    # def openPiePlotFigUsingPIL(self):
    #     from PIL import Image
    #     img = Image.open("plot1.png")
    #     img.show()
    
    # def openPiePlotFigUsingOpenCV(self):
    #     import cv2
    #     img = cv2.imread("plot1.png")
    #     cv2.imshow("Pie Chart", img)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()

    # Plotting a pie chart
    def plotPieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, noOfSearchTerms):
        filename = datetime.today().strftime('%Y-%m-%d-%H-%M-%S') + '.png'
        labels = ['Positive [' + str(positive) + '%]',
                  'Weakly Positive [' + str(wpositive) + '%]',
                  'Strongly Positive [' + str(spositive) + '%]',
                  'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]',
                  'Weakly Negative [' + str(wnegative) + '%]',
                  'Strongly Negative [' + str(snegative) + '%]']

        labels2 = ["Positive",
                  "Weakly Positive",
                  "Strongly Positive",
                  "Neutral",
                  "Negative",
                  "Weakly Negative",
                  "Strongly Negative"]

        sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
        colors = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
        patches, texts = plt.pie(sizes, labels = labels2)#, colors = colors, startangle = 90    , autopct='%1.2f%%')

        # plt.ioff()
        plt.legend(patches, labels, loc = "best")
        # plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()

        if not os.path.exists('plots'):
            os.makedirs('plots')

        plt.savefig('plots/{}'.format(str(filename)), dpi = 180)
        plt.show()

        # self.openPiePlotFigUsingPIL()
        # self.openPiePlotFigUsingOpenCV()
        # self.plotPieChartUsingPandas(sizes, labels)

        # # To show the pie chart onto browser
        # plt.plot([3,1,4,1,5], 'ks-', mec = 'w', mew = 5, ms = 20)
        # mpld3.enable_notebook()
        # mpld3.show()
    
    # def plotPieChartUsingPandas(self, sizes, labels):
    #     filename = datetime.today().strftime('%Y-%m-%d-%H-%M-%S') + '.png'
    #     import pandas as pd
    #     sizes = [float(i) for i in sizes]
    #     # df = pd.DataFrame({'sizes': sizes},
    #     #                   index = labels)
    #     df = pd.DataFrame({'sizes': sizes},
    #                       index = labels)
    #     # Only Plotting
    #     # df.plot.pie(y = 'sizes', figsize = (15, 15))
    #     # Plotting and saving
    #     plot = df.plot.pie(y = 'sizes', figsize = (10, 10)).get_figure().savefig("plots/{}".format(str(filename)))
    #     # plot.show()
    #     plt.show()

    # To enter the data into the database
    def data_entry(self, tweetText, key):
        for item in self.tweetText:
            database.execute('''INSERT INTO result(keyword, tweet) VALUES(?, ?)''', (self.key, item))
        database.commit()

    # Download Twitter Data
    def DownloadData(self, extras):
        try:
            (consumerKey, consumerSecret, accessToken, accessTokenSecret) = self.extras

            auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
            auth.set_access_token(accessToken, accessTokenSecret)
            api = tweepy.API(auth)

            # input for term to be searched and how many tweets to search
            # searchTerm = input("Enter Keyword/Tag to search about: ")
            # NoOfTerms = int(input("Enter how many tweets to search: "))   
            searchTerm = self.loc1.text()
            NoOfTerms = int(self.loc2.text())
            
            if type(NoOfTerms) == type(int()):
                # searching for tweets
                self.tweets = tweepy.Cursor(api.search, q = searchTerm, lang = "en").items(NoOfTerms)

                # # Open/create a file to append data to
                # csvFile = open('result.csv', 'a')

                # # Use csv writer
                # csvWriter = csv.writer(csvFile)

                # creating some variables to store info
                polarity = 0
                positive = 0
                wpositive = 0
                spositive = 0
                negative = 0
                wnegative = 0
                snegative = 0
                neutral = 0

                # iterating through tweets fetched
                for tweet in self.tweets:
                    # Append to temp so that we can store in csv later. I use encode UTF-8
                    self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))

                    # print (tweet.text.translate(non_bmp_map))    #print tweet's text
                    analysis = TextBlob(tweet.text)

                    # Tweet's Polarity
                    # print(analysis.sentiment)
                    # print(analysis.sentiment.polarity)
                    polarity = polarity + analysis.sentiment.polarity  # adding up polarities to find the average later

                    # adding reaction of how people are reacting to find average later
                    if (analysis.sentiment.polarity == 0):
                        neutral += 1
                    elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                        wpositive += 1
                    elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                        positive += 1
                    elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                        spositive += 1
                    elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                        wnegative += 1
                    elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                        negative += 1
                    elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                        snegative += 1

                # # Write to csv and close csv file
                # csvWriter.writerow(self.tweetText)
                # csvFile.close()

                self.key = searchTerm
                self.data_entry(self.tweetText, self.key)

                database.execute('''SELECT tweet FROM result ORDER BY id DESC LIMIT {}'''.format(NoOfTerms))
                # for record in data:
                #     print(record)

                # finding average of how people are reacting
                positive = self.percentage(positive, NoOfTerms)
                wpositive = self.percentage(wpositive, NoOfTerms)
                spositive = self.percentage(spositive, NoOfTerms)
                negative = self.percentage(negative, NoOfTerms)
                wnegative = self.percentage(wnegative, NoOfTerms)
                snegative = self.percentage(snegative, NoOfTerms)
                neutral = self.percentage(neutral, NoOfTerms)

                # finding average reaction
                polarity = float(polarity / NoOfTerms)

                # printing out data
                # print("How people are reacting on " + searchTerm + " by analyzing " + str(NoOfTerms) + " tweets.")
                # print()
                # print("General Report: ")

                # if (polarity == 0):
                #     print("Neutral")
                # elif (polarity > 0 and polarity <= 0.3):
                #     print("Weakly Positive")
                # elif (polarity > 0.3 and polarity <= 0.6):
                #     print("Positive")
                # elif (polarity > 0.6 and polarity <= 1):
                #     print("Strongly Positive")
                # elif (polarity > -0.3 and polarity <= 0):
                #     print("Weakly Negative")
                # elif (polarity > -0.6 and polarity <= -0.3):
                #     print("Negative")
                # elif (polarity > -1 and polarity <= -0.6):
                #     print("Strongly Negative")

                # print()
                # print("Detailed Report: ")
                # print(str(positive) + "% people thought it was positive")
                # print(str(wpositive) + "% people thought it was weakly positive")
                # print(str(spositive) + "% people thought it was strongly positive")
                # print(str(negative) + "% people thought it was negative")
                # print(str(wnegative) + "% people thought it was weakly negative")
                # print(str(snegative) + "% people thought it was strongly negative")
                # print(str(neutral) + "% people thought it was neutral")

                self.plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, NoOfTerms)
            else:
                QMessageBox.warning(self, "Error-1", "Please enter integer number in \'Number of Tweets\' field, please check your internet connection or your Tweeter Keys...".format(QMessageBox.warning))
        except:
            QMessageBox.warning(self, "Error-2", "Some error has occurred, please check your internet connection or your Twitter Keys...".format(QMessageBox.warning))


class Login(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        # Creating Grid Layout
        layout = QGridLayout()

        # Window Title
        self.setWindowTitle("Login")

        # Labels
        self.text1 = QLabel()
        self.text2 = QLabel()
        self.text1.setText("Login ID")
        self.text2.setText("Password")

        # Line Edit
        self.loc1 = QLineEdit(self)
        self.loc1.setPlaceholderText("Enter Your Username")

        self.loc2 = QLineEdit(self)
        self.loc2.setPlaceholderText("Enter Your Password")
        self.loc2.setEchoMode(QLineEdit.Password)

        # Push Buttons
        login_button = QPushButton("Login")
        signup_button = QPushButton("Sign Up")
        close_button = QPushButton("Close")
        forgot_pwd_button = QPushButton("Forgot Password")

        # Layout
        layout.addWidget(self.text1, 0, 0)
        layout.addWidget(self.text2, 1, 0)
        layout.addWidget(self.loc1, 0, 1)
        layout.addWidget(self.loc2, 1, 1)
        layout.addWidget(login_button, 2, 0, 1, 2)
        layout.addWidget(signup_button, 3, 0, 1, 2)
        layout.addWidget(forgot_pwd_button, 4, 0, 1, 2)
        layout.addWidget(close_button, 5, 0, 1, 2)

        self.setLayout(layout)
        self.setFocus()

        # Events and Signals
        login_button.clicked.connect(self.login)
        signup_button.clicked.connect(self.signup)
        forgot_pwd_button.clicked.connect(self.forgot_pwd)
        close_button.clicked.connect(self.close)

    def login(self):
        try:
            login = (str(self.loc1.text()), str(self.loc2.text()))
            try:
                # database = sqlite3.connect("database.sqlite3")
                # cursor = database.cursor()
                data = database.execute('''SELECT username, pwd FROM record where username == "{}" and pwd == "{}"'''.format(login[0], login[1]))
                keys = database.execute('''SELECT customerkey, customersecret, accesstoken, accesstokensecret FROM record where username == "{}" and pwd == "{}"'''.format(login[0], login[1]))
                data2 = []
                data3 = []
                for record in data:
                    data2.append(record)

                for key in keys:
                    data3.append(key)
                data2 = data2[0]
                extras = data3[0]

                if(data2 == login):
                    QMessageBox.information(self, "Success", "Logged in successfully...!!!".format(QMessageBox.warning))
                    dialogl.close()
                    dialogs = SentimentAnalysis(extras)
                    dialogs.show()
                    dialogs.exec_()
                    dialogs.close()
                    database.close()
                database.close()
                if(data2 != login):
                    QMessageBox.warning(self, "Error-1", "Username or Password is incorrect, try again...".format(QMessageBox.warning))
                    database.close()
                # elif (data2 != login):
                #         QMessageBox.warning(self, "Error", "Username or Password is incorrect, try again...".format(QMessageBox.warning))
                #         database.close()
                database.close()
            except:
                QMessageBox.warning(self, "Error-2", "Username or Password is incorrect, try again...".format(QMessageBox.warning))
        except:
            QMessageBox.information(self, "Error-3", "Some error has occurred...".format(QMessageBox.warning))

    def signup(self):
        dialogs1 = Signup()
        dialogs1.show()
        dialogs1.exec_()
        dialogs1.close()
    
    def forgot_pwd(self):
        pass


class Signup(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        # Creating Grid Layout
        layout = QGridLayout()

        # Window Title
        self.setWindowTitle("Sign Up")

        # Labels
        self.text1 = QLabel()
        self.text2 = QLabel()
        self.text3 = QLabel()
        self.text4 = QLabel()
        self.text5 = QLabel()
        self.text6 = QLabel()
        self.text7 = QLabel()
        self.text8 = QLabel()
        self.text9 = QLabel()
        self.text1.setText("Username")
        self.text2.setText("Name")
        self.text3.setText("e-Mail")
        self.text4.setText("Password")
        self.text5.setText("Confirm Password")
        self.text6.setText("Customer Key")
        self.text7.setText("Customer Secret")
        self.text8.setText("Access Token")
        self.text9.setText("Access Token Secret")

        self.loc1 = QLineEdit(self)
        self.loc1.setPlaceholderText("Enter Your username")

        self.loc2 = QLineEdit(self)
        self.loc2.setPlaceholderText("Enter Your Name")

        self.loc3 = QLineEdit(self)
        self.loc3.setPlaceholderText("Enter Your e-Mail")

        self.loc4 = QLineEdit(self)
        self.loc4.setPlaceholderText("Enter Your Password")
        self.loc4.setEchoMode(QLineEdit.Password)

        self.loc5 = QLineEdit(self)
        self.loc5.setPlaceholderText("Confirm Your Password")
        self.loc5.setEchoMode(QLineEdit.Password)

        self.loc6 = QLineEdit(self)
        self.loc6.setPlaceholderText("Enter Your Customer Key")

        self.loc7 = QLineEdit(self)
        self.loc7.setPlaceholderText("Enter Your Customer Secret")

        self.loc8 = QLineEdit(self)
        self.loc8.setPlaceholderText("Enter Your Access Token")

        self.loc9 = QLineEdit(self)
        self.loc9.setPlaceholderText("Enter Your Access Token Secret")

        # Push Buttons
        # login_button = QPushButton("Login")
        signup_button = QPushButton("Sign Up")
        close_button = QPushButton("Close")

        # Layout
        layout.addWidget(self.text1, 0, 0)
        layout.addWidget(self.text2, 1, 0)
        layout.addWidget(self.text3, 2, 0)
        layout.addWidget(self.text4, 3, 0)
        layout.addWidget(self.text5, 4, 0)
        layout.addWidget(self.text6, 5, 0)
        layout.addWidget(self.text7, 6, 0)
        layout.addWidget(self.text8, 7, 0)
        layout.addWidget(self.text9, 8, 0)
        layout.addWidget(self.loc1, 0, 1)
        layout.addWidget(self.loc2, 1, 1)
        layout.addWidget(self.loc3, 2, 1)
        layout.addWidget(self.loc4, 3, 1)
        layout.addWidget(self.loc5, 4, 1)
        layout.addWidget(self.loc6, 5, 1)
        layout.addWidget(self.loc7, 6, 1)
        layout.addWidget(self.loc8, 7, 1)
        layout.addWidget(self.loc9, 8, 1)
        layout.addWidget(signup_button, 9, 0)
        layout.addWidget(close_button, 9, 1)

        self.setLayout(layout)
        self.setFocus()

        # Events and Signals
        signup_button.clicked.connect(self.signup2)
        close_button.clicked.connect(self.close)

    def signup2(self):
        try:
            username = self.loc1.text()
            name = self.loc2.text()
            email = self.loc3.text()
            pwd1 = self.loc4.text()
            pwd2 = self.loc5.text()
            customerkey = self.loc6.text()
            customersecret = self.loc7.text()
            accesstoken = self.loc8.text()
            accesstokensecret = self.loc9.text()

            # print("username {}, name {}, email {}, pwd1 {}, pwd2 {}, customerkey {}, customersecret {}, accesstoken {}, accesstokensecret {}".format
            #       (username, name, email, pwd1, pwd2, customerkey, customersecret, accesstoken, accesstokensecret))

            if pwd1 == '' or pwd2 == '':
                QMessageBox.information(self, "Password can not be blank", "Password can not be blank...".format(QMessageBox.warning))

            elif pwd1 == pwd2:
                # database = sqlite3.connect("database.sqlite3")
                # database.execute('''CREATE TABLE IF NOT EXISTS "record" (
                #                 "username"	TEXT NOT NULL UNIQUE,
                #                 "name"	TEXT NOT NULL,
                #                 "email"	TEXT NOT NULL UNIQUE,
                #                 "pwd"	TEXT NOT NULL,
                #                 "customerkey"	TEXT NOT NULL,
                #                 "customersecret"	TEXT NOT NULL,
                #                 "accesstoken"	TEXT NOT NULL,
                #                 "accesstokensecret"	TEXT NOT NULL)
                #                 ''')
                database.execute('''INSERT INTO record(username, name, email, pwd, customerkey, customersecret, accesstoken, accesstokensecret)
                                VALUES (?,?,?,?,?,?,?,?)''',
                                (username, name, email, pwd1, customerkey, customersecret, accesstoken, accesstokensecret))
                database.commit()
                database.close()

                QMessageBox.information(self, "Sign Up Success", "Successfully signed up...".format(QMessageBox.information))

                extras = (customerkey, customersecret, accesstoken, accesstokensecret)
                dialogl.close()
                app.closeAllWindows()

                dialogsa1 = SentimentAnalysis(extras)
                dialogsa1.show()
                dialogsa1.exec_()
                dialogsa1.close()
            elif pwd1 != pwd2:
                QMessageBox.warning(self, "Password Mismatch Error", "Your Password do not match...".format(QMessageBox.warning))
        except:
            QMessageBox.warning(self, "Error", "Some error 2 has occurred...".format(QMessageBox.warning))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialogl = Login()
    dialogl.show()
    dialogl.exec_()

# extras = ('KjzmXyvQuTsAp1YoWL7vYvIMA',
#           'dyWVO2sqR5npp2nPa4etMDsBuj79FnwjcIyqzR5mhG4vCT5GEc',
#           '1231294931160850432-m5kHYPFUdtXx8GKsulENsmgGkAXJsy',
#           'X7CEWJo5ZxAOPgbLH7bH0etVdlFYOn0oNfqMIJKFFkvvs')