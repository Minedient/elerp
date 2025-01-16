# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'management.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QMainWindow, QMenuBar, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QStatusBar,
    QTabWidget, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 3, 1, 1)

        self.saveButton = QPushButton(self.groupBox)
        self.saveButton.setObjectName(u"saveButton")

        self.gridLayout.addWidget(self.saveButton, 0, 1, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.refreshButton = QPushButton(self.groupBox)
        self.refreshButton.setObjectName(u"refreshButton")

        self.gridLayout.addWidget(self.refreshButton, 0, 4, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 5, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 1, 2, 1, 1)

        self.editTrigger = QRadioButton(self.groupBox)
        self.editTrigger.setObjectName(u"editTrigger")
        self.editTrigger.setChecked(True)

        self.gridLayout.addWidget(self.editTrigger, 1, 1, 1, 1)

        self.tempMessageLabel = QLabel(self.groupBox)
        self.tempMessageLabel.setObjectName(u"tempMessageLabel")

        self.gridLayout.addWidget(self.tempMessageLabel, 1, 3, 1, 2)


        self.verticalLayout.addWidget(self.groupBox)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.databaseTabWidget = QTabWidget(self.centralwidget)
        self.databaseTabWidget.setObjectName(u"databaseTabWidget")
        self.worksheetWidget = QWidget()
        self.worksheetWidget.setObjectName(u"worksheetWidget")
        self.horizontalLayout = QHBoxLayout(self.worksheetWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.worksheetTable = QTableWidget(self.worksheetWidget)
        self.worksheetTable.setObjectName(u"worksheetTable")
        self.worksheetTable.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.worksheetTable.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)

        self.horizontalLayout.addWidget(self.worksheetTable)

        self.databaseTabWidget.addTab(self.worksheetWidget, "")
        self.pathWidget = QWidget()
        self.pathWidget.setObjectName(u"pathWidget")
        self.horizontalLayout_2 = QHBoxLayout(self.pathWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pathTable = QTableWidget(self.pathWidget)
        self.pathTable.setObjectName(u"pathTable")
        self.pathTable.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.pathTable.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.pathTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.horizontalLayout_2.addWidget(self.pathTable)

        self.databaseTabWidget.addTab(self.pathWidget, "")
        self.recordWidget = QWidget()
        self.recordWidget.setObjectName(u"recordWidget")
        self.horizontalLayout_3 = QHBoxLayout(self.recordWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.recordTable = QTableWidget(self.recordWidget)
        self.recordTable.setObjectName(u"recordTable")
        self.recordTable.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.recordTable.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.recordTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.horizontalLayout_3.addWidget(self.recordTable)

        self.databaseTabWidget.addTab(self.recordWidget, "")

        self.verticalLayout.addWidget(self.databaseTabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
#if QT_CONFIG(shortcut)
        self.label_3.setBuddy(self.refreshButton)
        self.label_2.setBuddy(self.editTrigger)
        self.label.setBuddy(self.saveButton)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(MainWindow)

        self.databaseTabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Database Management GUI", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Action", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Refresh Tables", None))
        self.saveButton.setText(QCoreApplication.translate("MainWindow", u"Click", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Edit Item", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Save Database", None))
        self.refreshButton.setText(QCoreApplication.translate("MainWindow", u"Click", None))
        self.editTrigger.setText(QCoreApplication.translate("MainWindow", u"Enabled", None))
        self.tempMessageLabel.setText("")
        self.databaseTabWidget.setTabText(self.databaseTabWidget.indexOf(self.worksheetWidget), QCoreApplication.translate("MainWindow", u"Worksheet", None))
        self.databaseTabWidget.setTabText(self.databaseTabWidget.indexOf(self.pathWidget), QCoreApplication.translate("MainWindow", u"Worksheet Path", None))
        self.databaseTabWidget.setTabText(self.databaseTabWidget.indexOf(self.recordWidget), QCoreApplication.translate("MainWindow", u"Record", None))
    # retranslateUi

