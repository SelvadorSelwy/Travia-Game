
from faulthandler import disable
import sys
from tkinter import CENTER
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
import pandas as pd
from functions import login,grid

app = QApplication(sys.argv)
window= QWidget() 
window.setWindowTitle("Am I a Programmer!")
my_icon = QIcon(r"images/icon.png")

window.setWindowIcon(my_icon)
window.setWhatsThis("Test your IT knowledge!")
window.setStyleSheet(f"background:#161219; max-width: 500px; max-height: 450px;")

login()

window.setLayout(grid)

window.show()

sys.exit(app.exec())