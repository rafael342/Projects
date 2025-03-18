import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox

class ClientManager(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Client Management System")
        self.setGeometry(300, 200, 600, 400)

        self.init_db()
        layout = QVBoxLayout()

        # Name input
        self.name_label = QLabel("Nume Complet:")
        self.name_input = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        # CNP input
        self.ssn_label = QLabel("CNP:")
        self.ssn_input = QLineEdit()
        layout.addWidget(self.ssn_label)
        layout.addWidget(self.ssn_input)

        # Serie De Buletin
        self.serieb_label = QLabel("Serie De Buletin:")
        self.serieb_input = QLineEdit()
        layout.addWidget(self.serieb_label)
        layout.addWidget(self.serieb_input)

        # Serie De Masina
        self.serie_label = QLabel("Serie De Masina:")
        self.serie_input = QLineEdit()
        layout.addWidget(self.serie_label)
        layout.addWidget(self.serie_input)

        # Data Intrarii (Date of Entry)
        self.data_label = QLabel("Data Intrarii:")
        self.data_input = QLineEdit()
        layout.addWidget(self.data_label)
        layout.addWidget(self.data_input)

        # Buttons
        self.add_button = QPushButton("Adauga Client")
        self.add_button.clicked.connect(self.add_client)
        layout.addWidget(self.add_button)

        # Search for clients
        self.search_button = QPushButton("Cautare Client")
        self.search_button.clicked.connect(self.search_client)
        layout.addWidget(self.search_button)

        # Delete client
        self.remove_button = QPushButton("Sterge Client")
        self.remove_button.clicked.connect(self.remove_client)
        layout.addWidget(self.remove_button)

        # Table to display clients
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Nume", "CNP", "Serie De Buletin", "Serie De Masina", "Data Intrarii"])
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.load_clients()

    def init_db(self):
        conn = sqlite3.connect("clients.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                ssn TEXT UNIQUE,
                serieb TEXT,
                serie TEXT,
                data_intrare TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def add_client(self):
        name = self.name_input.text()
        ssn = self.ssn_input.text()
        serieb = self.serieb_input.text()
        serie = self.serie_input.text()
        data = self.data_input.text()

        if not name or not ssn or not data:
            QMessageBox.warning(self, "Input Error", "Nume, CNP si Data Intrarii sunt necesare!")
            return

        conn = sqlite3.connect("clients.db")
        cursor = conn.cursor()
        try:
            # Insert client into the database including data_intrare
            cursor.execute("INSERT INTO clients (name, ssn, serieb, serie, data_intrare) VALUES (?, ?, ?, ?, ?)",
                           (name, ssn, serieb, serie, data))
            conn.commit()
            QMessageBox.information(self, "Success", "Client adaugat cu succes!")
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "CNP-ul trebuie sa fie unic!")
        conn.close()

        # Clear input fields after adding client
        self.name_input.clear()
        self.ssn_input.clear()
        self.serieb_input.clear()
        self.serie_input.clear()
        self.data_input.clear()

        # Reload the list of clients (including date of entry)
        self.load_clients()

    def search_client(self):
        name = self.name_input.text()
        conn = sqlite3.connect("clients.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, ssn, serieb, serie, data_intrare FROM clients WHERE name LIKE ?", ('%' + name + '%',))
        results = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(results))
        for row_index, row_data in enumerate(results):
            for col_index, data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(data)))

    def remove_client(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Selection Error", "Selecteaza un client pentru a-l sterge!")
            return

        client_name = self.table.item(selected_row, 0).text()
        client_ssn = self.table.item(selected_row, 1).text()

        reply = QMessageBox.question(self, 'Confirmare', f"Esti sigur ca vrei sa stergi clientul '{client_name}' (CNP: {client_ssn})?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            conn = sqlite3.connect("clients.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clients WHERE ssn = ?", (client_ssn,))
            conn.commit()
            conn.close()

            self.load_clients()
            QMessageBox.information(self, "Succes", f"Clientul '{client_name}' a fost sters cu succes!")

    def load_clients(self):
        conn = sqlite3.connect("clients.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, ssn, serieb, serie, data_intrare FROM clients")
        results = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(results))
        for row_index, row_data in enumerate(results):
            for col_index, data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(data)))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClientManager()
    window.show()
    sys.exit(app.exec())


