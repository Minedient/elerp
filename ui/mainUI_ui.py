# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainUI.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QStatusBar,
    QTableWidget, QTableWidgetItem, QTextBrowser, QVBoxLayout,
    QWidget)

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        if not mainWindow.objectName():
            mainWindow.setObjectName(u"mainWindow")
        mainWindow.setWindowModality(Qt.WindowModality.ApplicationModal)
        mainWindow.resize(1278, 719)
        self.actionAbout_The_App = QAction(mainWindow)
        self.actionAbout_The_App.setObjectName(u"actionAbout_The_App")
        self.actionFile_Naming_Convention = QAction(mainWindow)
        self.actionFile_Naming_Convention.setObjectName(u"actionFile_Naming_Convention")
        self.centralwidget = QWidget(mainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.actionBox = QGroupBox(self.centralwidget)
        self.actionBox.setObjectName(u"actionBox")
        self.gridLayout = QGridLayout(self.actionBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.worksheetCountLabel = QLabel(self.actionBox)
        self.worksheetCountLabel.setObjectName(u"worksheetCountLabel")

        self.gridLayout.addWidget(self.worksheetCountLabel, 0, 2, 1, 1)

        self.uploadWidgetButton = QPushButton(self.actionBox)
        self.uploadWidgetButton.setObjectName(u"uploadWidgetButton")

        self.gridLayout.addWidget(self.uploadWidgetButton, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 5, 1, 1)

        self.nextToProgramButton = QRadioButton(self.actionBox)
        self.nextToProgramButton.setObjectName(u"nextToProgramButton")

        self.gridLayout.addWidget(self.nextToProgramButton, 1, 3, 1, 1)

        self.registerWidgetButton = QPushButton(self.actionBox)
        self.registerWidgetButton.setObjectName(u"registerWidgetButton")

        self.gridLayout.addWidget(self.registerWidgetButton, 1, 1, 1, 1)

        self.label_2 = QLabel(self.actionBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.label_4 = QLabel(self.actionBox)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 1, 2, 1, 1)

        self.label_3 = QLabel(self.actionBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        self.downloadsFolderButton = QRadioButton(self.actionBox)
        self.downloadsFolderButton.setObjectName(u"downloadsFolderButton")

        self.gridLayout.addWidget(self.downloadsFolderButton, 1, 4, 1, 1)


        self.verticalLayout.addWidget(self.actionBox)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.groupBox = QGroupBox(self.frame)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.recentUsageTable = QTableWidget(self.groupBox)
        if (self.recentUsageTable.columnCount() < 4):
            self.recentUsageTable.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.recentUsageTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.recentUsageTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.recentUsageTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.recentUsageTable.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        if (self.recentUsageTable.rowCount() < 15):
            self.recentUsageTable.setRowCount(15)
        self.recentUsageTable.setObjectName(u"recentUsageTable")
        font = QFont()
        font.setPointSize(12)
        self.recentUsageTable.setFont(font)
        self.recentUsageTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.recentUsageTable.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.recentUsageTable.setTextElideMode(Qt.TextElideMode.ElideLeft)
        self.recentUsageTable.setRowCount(15)
        self.recentUsageTable.horizontalHeader().setCascadingSectionResizes(False)
        self.recentUsageTable.horizontalHeader().setStretchLastSection(True)
        self.recentUsageTable.verticalHeader().setStretchLastSection(False)

        self.horizontalLayout_2.addWidget(self.recentUsageTable)


        self.horizontalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.frame)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.recentUploadedTable = QTableWidget(self.groupBox_2)
        if (self.recentUploadedTable.columnCount() < 4):
            self.recentUploadedTable.setColumnCount(4)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.recentUploadedTable.setHorizontalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.recentUploadedTable.setHorizontalHeaderItem(1, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.recentUploadedTable.setHorizontalHeaderItem(2, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.recentUploadedTable.setHorizontalHeaderItem(3, __qtablewidgetitem7)
        if (self.recentUploadedTable.rowCount() < 15):
            self.recentUploadedTable.setRowCount(15)
        self.recentUploadedTable.setObjectName(u"recentUploadedTable")
        self.recentUploadedTable.setFont(font)
        self.recentUploadedTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.recentUploadedTable.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.recentUploadedTable.setRowCount(15)
        self.recentUploadedTable.horizontalHeader().setStretchLastSection(True)
        self.recentUploadedTable.verticalHeader().setCascadingSectionResizes(False)
        self.recentUploadedTable.verticalHeader().setProperty(u"showSortIndicator", False)

        self.horizontalLayout_3.addWidget(self.recentUploadedTable)


        self.horizontalLayout.addWidget(self.groupBox_2)


        self.verticalLayout.addWidget(self.frame)

        self.logBrowser = QTextBrowser(self.centralwidget)
        self.logBrowser.setObjectName(u"logBrowser")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.logBrowser.sizePolicy().hasHeightForWidth())
        self.logBrowser.setSizePolicy(sizePolicy1)
        self.logBrowser.setMaximumSize(QSize(16777215, 50))

        self.verticalLayout.addWidget(self.logBrowser)

        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(mainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1278, 33))
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(mainWindow)
        self.statusbar.setObjectName(u"statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuHelp.addAction(self.actionAbout_The_App)
        self.menuHelp.addAction(self.actionFile_Naming_Convention)

        self.retranslateUi(mainWindow)

        QMetaObject.connectSlotsByName(mainWindow)
    # setupUi

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(QCoreApplication.translate("mainWindow", u"ELERP", None))
        self.actionAbout_The_App.setText(QCoreApplication.translate("mainWindow", u"About the App", None))
        self.actionFile_Naming_Convention.setText(QCoreApplication.translate("mainWindow", u"File Naming Convention", None))
        self.label.setText(QCoreApplication.translate("mainWindow", u"Welcome to Extra Learning Exercise Report Platform (ELERP). Here you can upload and share exercise worksheet for other teacher to use during substition class.", None))
        self.actionBox.setTitle(QCoreApplication.translate("mainWindow", u"Please choose from one of the following action", None))
        self.worksheetCountLabel.setText(QCoreApplication.translate("mainWindow", u"Total worksheets: 0", None))
        self.uploadWidgetButton.setText(QCoreApplication.translate("mainWindow", u"Open", None))
        self.nextToProgramButton.setText(QCoreApplication.translate("mainWindow", u"Next to program", None))
        self.registerWidgetButton.setText(QCoreApplication.translate("mainWindow", u"Register", None))
        self.label_2.setText(QCoreApplication.translate("mainWindow", u"Add Exercise Worksheet to Server", None))
        self.label_4.setText(QCoreApplication.translate("mainWindow", u"File store location:", None))
        self.label_3.setText(QCoreApplication.translate("mainWindow", u"Register to use a worksheet", None))
        self.downloadsFolderButton.setText(QCoreApplication.translate("mainWindow", u"Downloads Folder", None))
        self.groupBox.setTitle(QCoreApplication.translate("mainWindow", u"Recent Registered Worksheet Usage", None))
        ___qtablewidgetitem = self.recentUsageTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("mainWindow", u"Teacher", None));
        ___qtablewidgetitem1 = self.recentUsageTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("mainWindow", u"Class", None));
        ___qtablewidgetitem2 = self.recentUsageTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("mainWindow", u"Worksheet", None));
        ___qtablewidgetitem3 = self.recentUsageTable.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("mainWindow", u"Time", None));
        self.groupBox_2.setTitle(QCoreApplication.translate("mainWindow", u"Recent New Upload Worksheets", None))
        ___qtablewidgetitem4 = self.recentUploadedTable.horizontalHeaderItem(0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("mainWindow", u"Name", None));
        ___qtablewidgetitem5 = self.recentUploadedTable.horizontalHeaderItem(1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("mainWindow", u"Subject", None));
        ___qtablewidgetitem6 = self.recentUploadedTable.horizontalHeaderItem(2)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("mainWindow", u"Form/Level", None));
        ___qtablewidgetitem7 = self.recentUploadedTable.horizontalHeaderItem(3)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("mainWindow", u"Upload Date", None));
        self.menuHelp.setTitle(QCoreApplication.translate("mainWindow", u"Help", None))
    # retranslateUi

