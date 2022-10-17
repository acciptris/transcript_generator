import sys

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGridLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QWidget,
)

from utils import generate_transcript


def generate_for_range(start_roll: str, end_roll: str, seal: str, sign: str, w):
    if len(start_roll) != 8 and len(end_roll) != 8:
        QMessageBox.warning(w, "Error", "Roll numbers must be 8 characters long")
    elif start_roll[:-2].upper() == end_roll[:-2].upper():
        start_roll_num = int(start_roll[-2:])
        end_roll_num = int(end_roll[-2:])
        roll_list = []
        for i in range(start_roll_num, end_roll_num + 1):
            roll_list.append(start_roll[:-2].upper() + str(i).zfill(2))
        roll_list = list(set(roll_list))
        invalid_roll_numbers = generate_transcript(
            input_roll_numbers=roll_list, seal_dir=seal, sign_dir=sign
        )
        if len(invalid_roll_numbers) != 0:
            QMessageBox.warning(
                w,
                "Error",
                "Invalid roll numbers: "
                + str(invalid_roll_numbers)[1:-1]
                + "\nOthers have been generated",
            )
        else:
            QMessageBox.warning(
                w, "Success", "All transcripts for the given range have been generated"
            )
    else:
        QMessageBox.warning(w, "Error", "Roll numbers must be of same year and branch")


def generate_all(seal: str, sign: str):
    generate_transcript(seal_dir=seal, sign_dir=sign)
    QMessageBox.warning(w, "Success", "All transcripts have been generated")


def select_seal(w, seal):
    QFileDialog.getOpenFileName(w, "Choose seal image", "", "Images (*.png)")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = QWidget()
    w.resize(300, 300)
    w.setWindowTitle("Transcript Generator")

    seal = ""
    sign = ""

    grid = QGridLayout()
    grid.addWidget(QLabel("Start Roll No"), 0, 0)
    start_roll = QLineEdit()
    grid.addWidget(start_roll, 0, 1)
    grid.addWidget(QLabel("End Roll No"), 1, 0)
    end_roll = QLineEdit()
    grid.addWidget(end_roll, 1, 1)

    rollrangeBtn = QPushButton("Generate for roll no range")
    rollrangeBtn.clicked.connect(
        lambda: generate_for_range(start_roll.text(), end_roll.text(), seal, sign, w)
    )
    grid.addWidget(rollrangeBtn, 2, 0)

    generate_all_btn = QPushButton("Generate all Transcripts")
    generate_all_btn.clicked.connect(lambda: generate_all(seal, sign))
    grid.addWidget(generate_all_btn, 2, 1)

    seal_image = QLabel()
    seal_image.hide()
    grid.addWidget(seal_image, 3, 0)
    sign_image = QLabel()
    sign_image.hide()
    grid.addWidget(sign_image, 3, 1)

    upload_btn = QPushButton("Upload Seal")

    def on_seal_click():
        global seal
        seal = QFileDialog.getOpenFileName(
            w, "Choose seal image", "", "Images (*.png)"
        )[0]
        seal_image.setPixmap(QPixmap(seal))
        seal_image.show()

    upload_btn.clicked.connect(on_seal_click)
    grid.addWidget(upload_btn, 4, 0)

    upload_sign_btn = QPushButton("Upload Sign")

    def on_sign_click():
        global sign
        sign = QFileDialog.getOpenFileName(
            w, "Choose signature image", "", "Images (*.png)"
        )[0]
        sign_image.setPixmap(QPixmap(sign))
        sign_image.show()

    upload_sign_btn.clicked.connect(on_sign_click)
    grid.addWidget(upload_sign_btn, 4, 1)

    w.setLayout(grid)
    w.setGeometry(100, 100, 200, 100)

    w.show()
    sys.exit(app.exec())
