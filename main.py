import json

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QMessageBox
import sys

from ui.home import Ui_Home
from ui.login import Ui_Login
from ui.register import Ui_Register
from ui.ticket import Ui_Ticket


class LoginUI(QWidget, Ui_Login):
    def __init__(self):
        super(LoginUI, self).__init__()
        self.setupUi(self)
        self.setFixedSize(816, 550)

        self.btn_login.clicked.connect(self.clicked_login)
        self.btn_to_register.clicked.connect(self.to_register)

    def clicked_login(self):
        username = self.field_username.text()
        password = self.field_pw.text()
        print(username, password)

        with open('accounts.json', 'r') as file:
            accounts = json.load(file)

        found = False
        for account in accounts:
            if account["username"] == username and account["password"] == password:
                found = True
                self.home_ui = HomeUI()
                self.home_ui.show()
                self.hide()
                break

        if not found:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Username atau password salah!")
            msg.setWindowTitle("Username atau password salah!")
            msg.exec()


    def to_register(self):
        self.register_ui = RegisterUI()
        self.register_ui.show()
        self.hide()


class RegisterUI(QWidget, Ui_Register):
    def __init__(self):
        super(RegisterUI, self).__init__()
        self.setupUi(self)
        self.setFixedSize(816, 550)

        self.btn_register.clicked.connect(self.clicked_register)
        self.btn_to_login.clicked.connect(self.to_login)

    def clicked_register(self):
        email = self.field_email.text()
        username = self.field_username.text()
        pw = self.field_pw.text()

        data = {
            "email": email,
            "username": username,
            "password": pw
        }

        existing_data = []
        with open("accounts.json", "r") as file:
            existing_data = json.load(file)
        existing_data.append(data)

        with open("accounts.json", "w") as file:
            json.dump(existing_data, file)

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Silahkan login dengan username dan password")
        msg.setWindowTitle("Akun berhasil dibuat!")
        msg.exec()

        self.to_login()

    def to_login(self):
        self.login_ui = LoginUI()
        self.login_ui.show()
        self.hide()


class HomeUI(QWidget, Ui_Home):
    def __init__(self):
        super(HomeUI, self).__init__()
        self.setupUi(self)
        self.setFixedSize(816, 550)

        self.cmb_destinasi.addItem("Pantai Manggar Balikpapan")
        self.cmb_destinasi.addItem("Pantai Seraya Balikpapan")
        self.cmb_destinasi.addItem("Pantai Tanah Merah Samboja")

        self.btn_beli.clicked.connect(self.clicked_beli)
        self.sb_pengunjung.textChanged.connect(self.hitung_harga)

    def hitung_harga(self):
        total_harga = int(self.sb_pengunjung.text()) * 1000000
        self.formatted_total_harga = "{:,}".format(total_harga)

        self.label_harga.setText(f"Total Harga: Rp {self.formatted_total_harga}")

    def clicked_beli(self):
        if int(self.sb_pengunjung.text()) > 0:
            tujuan = self.cmb_destinasi.currentText()
            tanggal = self.calendar.selectedDate().toString("dddd, dd MMM yyyy")
            pengunjung = self.sb_pengunjung.text()

            self.ticket = TicketUi(tujuan, tanggal, pengunjung, self.formatted_total_harga)
            self.ticket.show()
            self.hide()


class TicketUi(QWidget, Ui_Ticket):
    def __init__(self, tujuan, tanggal, pengunjung, harga):
        super(TicketUi, self).__init__()
        self.setupUi(self)
        self.setFixedSize(816, 550)

        self.label_tujuan.setText(f"Tujuan: {tujuan}")
        self.label_tanggal.setText(f"Hari/tanggal: {tanggal}")
        self.label_pengunjung.setText(f"Jumlah pengunjung {pengunjung}")
        self.label_harga.setText(f"Total harga: {harga}")
        self.btn_kembali.clicked.connect(self.clicked_kembali)

    def clicked_kembali(self):
        self.home = HomeUI()
        self.home.show()
        self.hide()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginUI()
    window.show()
    sys.exit(app.exec_())
