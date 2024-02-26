from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QInputDialog, QMessageBox, QVBoxLayout, \
    QLabel, QLineEdit, QFileDialog
from PyQt6 import QtCore, QtWidgets
import sys
import json
import pydicom
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas



from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_dataimaging(object):
    def setupUi(self, dataimaging):
        dataimaging.setObjectName("dataimaging")
        dataimaging.resize(400, 300)
        self.pushButton = QtWidgets.QPushButton(parent=dataimaging)
        self.pushButton.setGeometry(QtCore.QRect(260, 20, 121, 32))
        self.pushButton.setObjectName("pushButton")
        self.data = QtWidgets.QTextEdit(parent=dataimaging)
        self.data.setGeometry(QtCore.QRect(20, 120, 351, 171))
        self.data.setObjectName("data")
        self.Cleandata = QtWidgets.QPushButton(parent=dataimaging)
        self.Cleandata.setGeometry(QtCore.QRect(260, 50, 121, 32))
        self.Cleandata.setObjectName("Cleandata")
        self.pushButton_2 = QtWidgets.QPushButton(parent=dataimaging)
        self.pushButton_2.setGeometry(QtCore.QRect(260, 80, 121, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_3 = QtWidgets.QLabel(parent=dataimaging)
        self.label_3.setGeometry(QtCore.QRect(10, 60, 58, 16))
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.splitter_2 = QtWidgets.QSplitter(parent=dataimaging)
        self.splitter_2.setGeometry(QtCore.QRect(10, 30, 151, 21))
        self.splitter_2.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.label_2 = QtWidgets.QLabel(parent=self.splitter_2)
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(parent=self.splitter_2)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.splitter = QtWidgets.QSplitter(parent=dataimaging)
        self.splitter.setGeometry(QtCore.QRect(10, 10, 157, 21))
        self.splitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.splitter.setObjectName("splitter")
        self.label = QtWidgets.QLabel(parent=self.splitter)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(parent=self.splitter)
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_3 = QtWidgets.QPushButton(parent=dataimaging)
        self.pushButton_3.setGeometry(QtCore.QRect(140, 80, 111, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(parent=dataimaging)
        self.pushButton_4.setGeometry(QtCore.QRect(30, 80, 100, 32))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(parent=dataimaging)
        self.pushButton_5.setGeometry(QtCore.QRect(30, 50, 100, 32))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(parent=dataimaging)
        self.pushButton_6.setGeometry(QtCore.QRect(140, 50, 111, 32))
        self.pushButton_6.setText("")
        self.pushButton_6.setObjectName("pushButton_6")

        self.retranslateUi(dataimaging)
        QtCore.QMetaObject.connectSlotsByName(dataimaging)
        
        self.pushButton.clicked.connect(self.show_raw_data)
        self.Cleandata.clicked.connect(self.clean_data)
        self.pushButton_2.clicked.connect(self.show_image)
        self.pushButton_4.clicked.connect(self.find_data)
        self.pushButton_3.clicked.connect(self.clean_data_by_keyword)
        self.pushButton_5.clicked.connect(self.add_data_to_json)
        self.pushButton_6.clicked.connect(self.add_data_to_json)
    
    def show_raw_data(self):
        file_path = self.lineEdit.text()
        try:
            with open(file_path, 'r') as file:
                data = file.read()
                self.data.setPlainText(data)
        except FileNotFoundError:
            self.data.setPlainText("File not found.")

    def clean_data(self):
        self.data.clear()
        layout = self.data.layout()
        if layout:
            item = layout.itemAt(0)
            if item:
                widget = item.widget()
                if widget:
                    widget.close()

    def show_image(self):
        file_path = self.lineEdit_2.text()
        if not file_path:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please enter a valid file path.")
            return

        try:
            dicom_image = pydicom.dcmread(file_path)
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.imshow(dicom_image.pixel_array, cmap=plt.cm.bone)
            ax.axis('off')
            canvas = FigureCanvas(fig)
            layout = QtWidgets.QVBoxLayout()
            layout.addWidget(canvas)
            self.data.setLayout(layout)
        except Exception as e:
            self.data.setPlainText("Error: " + str(e))

    def find_data(self):
        file_name, _ = QFileDialog.getOpenFileName(None, 'Open JSON File', '.', 'JSON Files (*.json)')
        if file_name:
            keyword, ok = QInputDialog.getText(None, 'Find Data', 'Enter keyword to find:')
            if ok:
                try:
                    with open(file_name, 'r') as file:
                        json_data = json.load(file)
                        if keyword in json_data:
                            value = json_data[keyword]
                            self.data.setPlainText(f"Keyword: {keyword}\nValue: {value}")
                        else:
                            self.data.setPlainText("Keyword not found in JSON file.")
                except FileNotFoundError:
                    self.data.setPlainText("File not found.")
                except Exception as e:
                    self.data.setPlainText(f"An error occurred: {str(e)}")
    def clean_data_by_keyword(self):
        keyword, ok = QInputDialog.getText(None, 'Clean Data by Keyword', 'Enter keyword to clean data:')
        if ok:
            try:
                file_name, _ = QFileDialog.getOpenFileName(None, 'Open JSON File', '.', 'JSON Files (*.json)')
                if file_name:
                    with open(file_name, 'r') as file:
                        json_data = json.load(file)

                    if keyword in json_data:
                        del json_data[keyword]
                        with open(file_name, 'w') as file:
                            json.dump(json_data, file, indent=4)
                        QMessageBox.information(None, 'Clean Data by Keyword', 'Keyword data successfully cleaned.')
                    else:
                        QMessageBox.information(None, 'Clean Data by Keyword', 'Keyword not found in JSON file.')

                    self.data.clear()

            except FileNotFoundError:
                QMessageBox.warning(None, 'Clean Data by Keyword', 'File not found.')
            except Exception as e:
                QMessageBox.warning(None, 'Clean Data by Keyword', f'An error occurred: {str(e)}')
    def add_data_to_json(self):
        keyword, ok = QInputDialog.getText(None, 'Add Data to JSON', 'Enter keyword:')
        if ok:
            value, ok = QInputDialog.getText(None, 'Add Data to JSON', f'Enter value for "{keyword}":')
            if ok:
                try:
                    file_name, _ = QFileDialog.getOpenFileName(None, 'Open JSON File', '.', 'JSON Files (*.json)')
                    if file_name:
                        with open(file_name, 'r') as file:
                            json_data = json.load(file)

                        json_data[keyword] = value

                        with open(file_name, 'w') as file:
                            json.dump(json_data, file, indent=4)
                        QMessageBox.information(None, 'Add Data to JSON', 'Data successfully added to JSON file.')

                except FileNotFoundError:
                    QMessageBox.warning(None, 'Add Data to JSON', 'File not found.')
                except Exception as e:
                    QMessageBox.warning(None, 'Add Data to JSON', f'An error occurred: {str(e)}')

    def retranslateUi(self, dataimaging):
        _translate = QtCore.QCoreApplication.translate
        dataimaging.setWindowTitle(_translate("dataimaging", "Data imaging"))
        self.pushButton.setText(_translate("dataimaging", "Show Raw Data"))
        self.Cleandata.setText(_translate("dataimaging", "Clean"))
        self.pushButton_2.setText(_translate("dataimaging", "Show Image"))
        self.label_2.setText(_translate("dataimaging", "Image:"))
        self.label.setText(_translate("dataimaging", "Data:"))
        self.pushButton_3.setText(_translate("dataimaging", "Clean Data"))
        self.pushButton_4.setText(_translate("dataimaging", "Find Data"))
        self.pushButton_5.setText(_translate("dataimaging", "ADD Data"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dataimaging = QtWidgets.QWidget()
    ui = Ui_dataimaging()
    ui.setupUi(dataimaging)
    dataimaging.show()
    sys.exit(app.exec())
