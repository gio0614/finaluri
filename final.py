import sqlite3

import sys
conn = sqlite3.connect("Movies.db")
cursor = conn.cursor()


saxeli=input("ფილმის სახელი რომელსაც აქვს ახალი ნახვები:")
raodenoba=int(input("ახალი ნახვების რაოდენობა : "))
reitingis_shecvla=input("ფილმის სახელი რომლის რეიტინგის ცვლილება გსურთ:")
axali_reitingi=float(input('ახალი რეიტინგი:'))
if axali_reitingi<=0 or axali_reitingi>=10:
    cursor.execute('''UPDATE imdb_top_1000 SET IMDB_rating=? WHERE Series_Title = ?''',
                   (axali_reitingi, reitingis_shecvla))

#აქ ხდება რომელიმე ფილმის ნახვების ცვლილება ოღონდ კონსოლიდან
cursor.execute('''UPDATE imdb_top_1000 SET No_of_Views = No_of_Views + ? WHERE Series_Title = ?''',(raodenoba,saxeli))



cursor.execute("SELECT * FROM imdb_top_1000")

# მონაცემთა ბაზიდან წამოღებული თითო კინოს Movie კლასის ობიექტად გადაკათება და მათი ფილმში დასეივება(იმ შემთხვევისთვის თუ რაიმეში დაგვჭირდა)
List_Of_Each_Film = cursor.fetchall()
Films = []
for each in List_Of_Each_Film:
    Film = Movie(*each)
    Films.append(Film)
#აქ ხდება ფილმის წაშლა მონაცემთა ბაზიდან მომხმარებლის მიერ
movie_erase=input('"შეიყვანე ფილმის სახელი რომელიც გინდა წაშალო: ')
cursor.execute('''DELETE FROM imdb_top_1000 WHERE Series_Title = ?''', (movie_erase,))
print(f'ფილმი "{movie_erase}" წარმატებით წაიშალა (თუ არსებობდა ბაზაში).')


def add_movie():
    print("შეიყვანე ახალი ფილმის მონაცემები:")
    Link = input("Link: ")
    Series_Title = input("ფილმის სახელი: ")
    Released_Year = input("გამოშვების წელი: ")
    Certificate = input("Certificate : ")
    Runtime = input("ხანგრძლივობა : ")
    Genre = input("ჟანრი : ")
    IMDB_Rating = float(input("IMDB რეიტინგი : "))
    Overview = input("მოკლე აღწერა: ")
    Meta_Score = input("Meta Score : ")
    Director = input("რეჟისორი: ")
    Star1 = input("მსახიობი 1: ")
    Star2 = input("მსახიობი 2: ")
    Star3 = input("მსახიობი 3: ")
    Star4 = input("მსახიობი 4: ")
    No_of_Views = int(input("ნახვების რაოდენობა: "))
    Gross = input("შემოსავალი : ")

    cursor.execute('''
        INSERT INTO imdb_top_1000
        (Poster_Link, Series_Title, Released_Year, Certificate, Runtime, Genre, IMDB_Rating,
         Overview, Meta_Score, Director, Star1, Star2, Star3, Star4, No_of_Views, Gross)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (Poster_Link, Series_Title, Released_Year, Certificate, Runtime, Genre, IMDB_Rating,
          Overview, Meta_Score, Director, Star1, Star2, Star3, Star4, No_of_Views, Gross))

    print(f"ფილმი '{Series_Title}' წარმატებით დაემატა ბაზაში.")
#add_movie()
from PyQt5.QtWidgets import *
#სხვანაირად ვერ მოვიფიქრეთ როგორ უნდა გვექნა და
class MovieTableApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Movies")
        self.setGeometry(100, 100, 1200, 700)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)


        self.table = QTableWidget()
        self.layout.addWidget(self.table)


        form_layout = QHBoxLayout()
        # აქ შეგვყავს იმ ფილმის სახელი რომლის ვახვებიც გვინდა რომ შევცვალოთ
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("შეიყვანე ფილმის სახელი")
        # აქ ხდება იმ რიცხვის შეყვანა რამდენითაც გვინდა რომ გაიზარდოს ჩვენი ნახვები
        self.views_input = QSpinBox()
        self.views_input.setRange(0, 10000000)
        self.views_input.setPrefix("ნახვები: ")
        # ამ ღილაკით ხდება ნავების დამატება
        self.add_button = QPushButton("დამატება")
        self.add_button.clicked.connect(self.update_views)
        # ამით კი ცხრილის განახლება რომ დასევდეს დამატებული რიცხვები მონაცემთა ბაზაში
        self.refresh_button = QPushButton("განახლება")
        self.refresh_button.clicked.connect(self.load_data)

        self.status_label = QLabel("სტატუსი: მზად")
        #ამ კოდით ვამატებთ ზემოთ უკვე აღწერილე ღილაკებს და სხვა ვიჯეტებს
        form_layout.addWidget(self.title_input)
        form_layout.addWidget(self.views_input)
        form_layout.addWidget(self.add_button)
        form_layout.addWidget(self.refresh_button)
        self.layout.addLayout(form_layout)
        self.layout.addWidget(self.status_label)


        self.load_data()
#ამ კოდით ჩვენ გადავიტანეთ ჩვენი დათაბეისი pyqt ფანჯარაში
    def load_data(self):
        conn = sqlite3.connect("Movies.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM imdb_top_1000")
        data = cursor.fetchall()
        headers = [description[0] for description in cursor.description]
        #აქ ხდება დათაბეისის სვეტებისა და სტრიქონების დათვლა
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        #აქ ხდება ჩვენი მონაცამების ცხრილში ჩასმა და დანომვრა enumerate ჩაშენებული ფუნქციით
        for row_index, row_data in enumerate(data):
            for column_index, cell in enumerate(row_data):
                self.table.setItem(row_index, column_index, QTableWidgetItem(str(cell)))

        conn.close()
        self.status_label.setText("ცხრილი განახლდა")

    def update_views(self):
        title = self.title_input.text()
        views = self.views_input.value()

        if not title:
            self.status_label.setText("გთხოვ შეიყვანე ფილმის სახელი")
            return


        self.status_label.setText(f"'{title}'-ს დაემატა {views} ნახვა")
        self.load_data()

if __name__ == "__main__":
    app = QApplication([])
    window = MovieTableApp()
    window.show()
    sys.exit(app.exec_())
conn.commit()
conn.close()