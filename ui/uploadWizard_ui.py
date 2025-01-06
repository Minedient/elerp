# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'uploadWizard.ui'
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
    QDialogButtonBox, QFormLayout, QFrame, QGridLayout,
    QGroupBox, QLabel, QLayout, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(320, 340)
        Dialog.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(9, -1, -1, -1)
        self.line = QFrame(self.frame)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line, 2, 0, 1, 3)

        self.groupBox = QGroupBox(self.frame)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.formLayout = QFormLayout(self.groupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.subjectsComboBox = QComboBox(self.groupBox)
        self.subjectsComboBox.setObjectName(u"subjectsComboBox")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.subjectsComboBox)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.formComboBox = QComboBox(self.groupBox)
        self.formComboBox.setObjectName(u"formComboBox")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.formComboBox)


        self.gridLayout.addWidget(self.groupBox, 3, 0, 1, 3)

        self.fileListWidget = QListWidget(self.frame)
        self.fileListWidget.setObjectName(u"fileListWidget")
        self.fileListWidget.setMinimumSize(QSize(0, 5))
        self.fileListWidget.setMaximumSize(QSize(16777215, 16777215))
        self.fileListWidget.setFrameShape(QFrame.Shape.StyledPanel)

        self.gridLayout.addWidget(self.fileListWidget, 0, 2, 1, 1)

        self.line_2 = QFrame(self.frame)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_2, 4, 0, 1, 3)

        self.textEdit = QTextEdit(self.frame)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setMaximumSize(QSize(16777215, 100))

        self.gridLayout.addWidget(self.textEdit, 5, 0, 1, 3)

        self.buttonFrame = QFrame(self.frame)
        self.buttonFrame.setObjectName(u"buttonFrame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.buttonFrame.sizePolicy().hasHeightForWidth())
        self.buttonFrame.setSizePolicy(sizePolicy1)
        self.buttonFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.buttonFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.buttonFrame)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.filesSelectorButton = QPushButton(self.buttonFrame)
        self.filesSelectorButton.setObjectName(u"filesSelectorButton")
        self.filesSelectorButton.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.filesSelectorButton.sizePolicy().hasHeightForWidth())
        self.filesSelectorButton.setSizePolicy(sizePolicy2)
        self.filesSelectorButton.setMaximumSize(QSize(100, 16777215))
        self.filesSelectorButton.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.filesSelectorButton.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.filesSelectorButton.setAutoFillBackground(False)
        self.filesSelectorButton.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))

        self.verticalLayout_2.addWidget(self.filesSelectorButton, 0, Qt.AlignmentFlag.AlignTop)

        self.resetButton = QPushButton(self.buttonFrame)
        self.resetButton.setObjectName(u"resetButton")
        self.resetButton.setCheckable(False)

        self.verticalLayout_2.addWidget(self.resetButton)


        self.gridLayout.addWidget(self.buttonFrame, 0, 0, 1, 1, Qt.AlignmentFlag.AlignTop)


        self.verticalLayout.addWidget(self.frame)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Upload Worksheet Wizard", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Informations/Details", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Subjects", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Form", None))
        self.filesSelectorButton.setText(QCoreApplication.translate("Dialog", u"Upload FIles", None))
        self.resetButton.setText(QCoreApplication.translate("Dialog", u"Reset", None))
    # retranslateUi

