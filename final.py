import sqlite3

import sys
conn = sqlite3.connect("Movies.db")
cursor = conn.cursor()

def add_movie():
    print("შეიყვანე ახალი ფილმის მონაცემები:")
    Poster_Link = input("Link: ")
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
    conn.commit()
add_movie()

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
        #აქ ვამატებთ წასაშლელ ღილაკს
        self.delete_input = QLineEdit()
        self.delete_input.setPlaceholderText("წასაშლელი ფილმის სახელი")

        self.delete_button = QPushButton("წაშლა")
        self.delete_button.clicked.connect(self.delete_movie)

        form_layout.addWidget(self.delete_input)
        form_layout.addWidget(self.delete_button)
        #რეიტინგის შეცვლის ღილაკი
        self.rating_title_input = QLineEdit()
        self.rating_title_input.setPlaceholderText("შეიყვანე ფილმის სახელი (რეიტინგის ცვლილება)")

        self.new_rating_input = QDoubleSpinBox()
        self.new_rating_input.setRange(0.0, 10.0)
        self.new_rating_input.setSingleStep(0.1)
        self.new_rating_input.setPrefix("რეიტინგი: ")

        self.change_rating_button = QPushButton("რეიტინგის შეცვლა")
        self.change_rating_button.clicked.connect(self.update_rating)

        # ფორმ ლეიაუტში ვიჯეტების დამატება
        form_layout.addWidget(self.rating_title_input)
        form_layout.addWidget(self.new_rating_input)
        form_layout.addWidget(self.change_rating_button)
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
#ეს არის რეიტინგის შეცვლის ფუნქცია
    def update_rating(self):
        title = self.rating_title_input.text().strip()
        new_rating = self.new_rating_input.value()

        if not title:
            self.status_label.setText("გთხოვ შეიყვანე ფილმის სახელი რეიტინგის ცვლილებისთვის")
            return

        conn = sqlite3.connect("Movies.db")
        cursor = conn.cursor()

        # ვამოწმებთ არსებობს თუ არა ფილმი
        cursor.execute("SELECT IMDB_Rating FROM imdb_top_1000 WHERE Series_Title = ?", (title,))
        result = cursor.fetchone()

        if result is None:
            self.status_label.setText(f"ფილმი '{title}' ვერ მოიძებნა ბაზაში")
        else:
            cursor.execute("UPDATE imdb_top_1000 SET IMDB_Rating = ? WHERE Series_Title = ?", (new_rating, title))
            conn.commit()
            self.status_label.setText(f"ფილმს '{title}' რეიტინგი განახლდა: {new_rating}")
            self.load_data()

        conn.close()
    #ეს არის ფილმის წაშლის მეთოდი
    def delete_movie(self):
        title = self.delete_input.text().strip()
        if not title:
            self.status_label.setText("გთხოვ შეიყვანე წასაშლელი ფილმის სახელი")
            return

        conn = sqlite3.connect("Movies.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM imdb_top_1000 WHERE Series_Title = ?", (title,))
        result = cursor.fetchone()

        if result is None:
            self.status_label.setText(f"ფილმი '{title}' ვერ მოიძებნა")
        else:
            cursor.execute("DELETE FROM imdb_top_1000 WHERE Series_Title = ?", (title,))
            conn.commit()
            self.status_label.setText(f"ფილმი '{title}' წარმატებით წაიშალა")
            self.load_data()

    def update_views(self):
        # აქ ხდება შეყვანილი ფილმის სახელის და ნახვების რაოდენობის ამოღება
        title = self.title_input.text()
        views = self.views_input.value()

        if not title:
            self.status_label.setText("გთხოვ შეიყვანე ფილმის სახელი")
            return

        # აქ ვუკავშირდებით მონაცემთა ბაზას და ვამოწმებთ ფილმი არსებობს თუ არა
        conn = sqlite3.connect("Movies.db")
        cursor = conn.cursor()

        cursor.execute("SELECT No_of_Views FROM imdb_top_1000 WHERE Series_Title = ?", (title,))
        result = cursor.fetchone()

        if result is None:
            self.status_label.setText(f"ფილმი '{title}' ვერ მოიძებნა")
        else:
            current_views = result[0]
            new_views = current_views + views
            # ვაახლებთ ფილმის ნახვების რაოდენობას
            cursor.execute("UPDATE imdb_top_1000 SET No_of_Views = ? WHERE Series_Title = ?", (new_views, title))
            conn.commit()
            self.status_label.setText(f"'{title}'-ს დაემატა {views} ნახვა (სულ: {new_views})")
            self.load_data()

        conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MovieTableApp()
    window.show()
    sys.exit(app.exec_())
