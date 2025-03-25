# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'registerWizard.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QAbstractScrollArea, QApplication,
    QComboBox, QDialog, QDialogButtonBox, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QSizePolicy, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(640, 480)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox_2 = QGroupBox(self.frame)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout = QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.comboBox = QComboBox(self.groupBox_2)
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout.addWidget(self.comboBox, 0, 1, 1, 1)

        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)

        self.subTeacherLabel = QLabel(self.groupBox_2)
        self.subTeacherLabel.setObjectName(u"subTeacherLabel")

        self.gridLayout.addWidget(self.subTeacherLabel, 1, 2, 1, 1)

        self.sectionLabel = QLabel(self.groupBox_2)
        self.sectionLabel.setObjectName(u"sectionLabel")

        self.gridLayout.addWidget(self.sectionLabel, 1, 0, 1, 1)

        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.nameEdit = QLineEdit(self.groupBox_2)
        self.nameEdit.setObjectName(u"nameEdit")

        self.gridLayout.addWidget(self.nameEdit, 0, 3, 1, 1)

        self.sectionCombox = QComboBox(self.groupBox_2)
        self.sectionCombox.addItem("")
        self.sectionCombox.addItem("")
        self.sectionCombox.addItem("")
        self.sectionCombox.addItem("")
        self.sectionCombox.addItem("")
        self.sectionCombox.addItem("")
        self.sectionCombox.addItem("")
        self.sectionCombox.addItem("")
        self.sectionCombox.addItem("")
        self.sectionCombox.addItem("")
        self.sectionCombox.addItem("")
        self.sectionCombox.setObjectName(u"sectionCombox")

        self.gridLayout.addWidget(self.sectionCombox, 1, 1, 1, 1)

        self.subTeacherEdit = QLineEdit(self.groupBox_2)
        self.subTeacherEdit.setObjectName(u"subTeacherEdit")

        self.gridLayout.addWidget(self.subTeacherEdit, 1, 3, 1, 1)


        self.verticalLayout_2.addWidget(self.groupBox_2)

        self.tableWidget = QTableWidget(self.frame)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.verticalLayout_2.addWidget(self.tableWidget)

        self.groupBox = QGroupBox(self.frame)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.worksheetEdit = QLineEdit(self.groupBox)
        self.worksheetEdit.setObjectName(u"worksheetEdit")

        self.horizontalLayout_2.addWidget(self.worksheetEdit)


        self.verticalLayout_2.addWidget(self.groupBox)


        self.verticalLayout.addWidget(self.frame)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"Details", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Name", None))
#if QT_CONFIG(tooltip)
        self.subTeacherLabel.setToolTip(QCoreApplication.translate("Dialog", u"The name of the teacher that will be subsituted (initial only!)", None))
#endif // QT_CONFIG(tooltip)
        self.subTeacherLabel.setText(QCoreApplication.translate("Dialog", u"Subsituted Teacher", None))
        self.sectionLabel.setText(QCoreApplication.translate("Dialog", u"Section", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Class", None))
        self.sectionCombox.setItemText(0, QCoreApplication.translate("Dialog", u"--Please Select--", None))
        self.sectionCombox.setItemText(1, QCoreApplication.translate("Dialog", u"1", None))
        self.sectionCombox.setItemText(2, QCoreApplication.translate("Dialog", u"2", None))
        self.sectionCombox.setItemText(3, QCoreApplication.translate("Dialog", u"3", None))
        self.sectionCombox.setItemText(4, QCoreApplication.translate("Dialog", u"4", None))
        self.sectionCombox.setItemText(5, QCoreApplication.translate("Dialog", u"5", None))
        self.sectionCombox.setItemText(6, QCoreApplication.translate("Dialog", u"6", None))
        self.sectionCombox.setItemText(7, QCoreApplication.translate("Dialog", u"7", None))
        self.sectionCombox.setItemText(8, QCoreApplication.translate("Dialog", u"8", None))
        self.sectionCombox.setItemText(9, QCoreApplication.translate("Dialog", u"9", None))
        self.sectionCombox.setItemText(10, QCoreApplication.translate("Dialog", u"10", None))

        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Result", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Selected Worksheet", None))
    # retranslateUi

