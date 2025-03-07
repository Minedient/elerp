# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'entryRemoveWizard.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QPushButton,
    QSizePolicy, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_EntryRemoveWizard(object):
    def setupUi(self, EntryRemoveWizard):
        if not EntryRemoveWizard.objectName():
            EntryRemoveWizard.setObjectName(u"EntryRemoveWizard")
        EntryRemoveWizard.resize(360, 342)
        self.verticalLayout = QVBoxLayout(EntryRemoveWizard)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(EntryRemoveWizard)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.label)

        self.tableCombox = QComboBox(self.groupBox)
        self.tableCombox.setObjectName(u"tableCombox")

        self.horizontalLayout.addWidget(self.tableCombox)


        self.verticalLayout.addWidget(self.groupBox)

        self.line = QFrame(EntryRemoveWizard)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.groupBox_2 = QGroupBox(EntryRemoveWizard)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy2)
        self.gridLayout = QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.rowCombox = QComboBox(self.groupBox_2)
        self.rowCombox.setObjectName(u"rowCombox")

        self.gridLayout.addWidget(self.rowCombox, 1, 1, 1, 1)

        self.removeButton = QPushButton(self.groupBox_2)
        self.removeButton.setObjectName(u"removeButton")

        self.gridLayout.addWidget(self.removeButton, 2, 0, 1, 2)

        self.tableWidget = QTableWidget(self.groupBox_2)
        self.tableWidget.setObjectName(u"tableWidget")

        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 2)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.buttonBox = QDialogButtonBox(EntryRemoveWizard)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(EntryRemoveWizard)
        self.buttonBox.accepted.connect(EntryRemoveWizard.accept)
        self.buttonBox.rejected.connect(EntryRemoveWizard.reject)

        QMetaObject.connectSlotsByName(EntryRemoveWizard)
    # setupUi

    def retranslateUi(self, EntryRemoveWizard):
        EntryRemoveWizard.setWindowTitle(QCoreApplication.translate("EntryRemoveWizard", u"Dialog", None))
        self.groupBox.setTitle(QCoreApplication.translate("EntryRemoveWizard", u"Table selector", None))
        self.label.setText(QCoreApplication.translate("EntryRemoveWizard", u"Please select the table to remove from:", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("EntryRemoveWizard", u"Table Viewer", None))
        self.label_2.setText(QCoreApplication.translate("EntryRemoveWizard", u"Please select the row you want to remove", None))
        self.removeButton.setText(QCoreApplication.translate("EntryRemoveWizard", u"Remove!", None))
    # retranslateUi

