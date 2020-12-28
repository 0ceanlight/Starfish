# Created by Oceanlight

from PyQt5 import QtCore, QtGui, QtWidgets

import sys 
import time 

from SQLquery import *
from SQLupdate import *
from SQLdelete import *

# 1) name - edit, do not accept ""?
# 2) urls - edit, remove, add
# 3) zoom info - edit, accept ""
# note: adding, removing, and editing does nothing without saving

class Ui_EditMenu(object):
	subjectID = None
	def __init__(self, Ui_Dashboard, subjectID):
		super().__init__()
		self.subjectID = subjectID
		self.Ui_Dashboard = Ui_Dashboard
		# print("success")

	def save(self):
		print("saving...")
		#  Save subject name
		print(self.textEdit.text())	
		setSubjectName(self.subjectID, self.textEdit.text())

		# Save Zoom Info
		widgetItem = self.zoomTableWidget.item(0, 0)
		if widgetItem and widgetItem.text:
				zoomUrl = widgetItem.text()
				print("zoom Url" + zoomUrl)
		widgetItem = self.zoomTableWidget.item(1, 0)
		if widgetItem and widgetItem.text:
				zoomPass = widgetItem.text()
				print("zoom Pass" + zoomPass)

		setSubjectZoomInfo(self.subjectID, zoomUrl, zoomPass)

		# Save URLs
		# delete all existing
		deleteAllURLs(self.subjectID)
		# - 1 for the 'add url' row
		rowCount = self.urlTableWidget.rowCount() - 1
		for row in range(rowCount):
			widgetItem = self.urlTableWidget.item(row, 0)
			if widgetItem and widgetItem.text:
				print(widgetItem.text())
				addSubjectUrl(self.subjectID, widgetItem.text())

		# TODO: reload dashboard
		self.Ui_Dashboard.refresh()
		

	def delete(self):
		deleteSubject(self.subjectID)
		# TODO close window properly
		exit()

	def addUrl(self):
		print("adding Url...")
		# add an empty url above the 'add url' row
		rowPosition = self.urlTableWidget.rowCount() - 1
		self.urlTableWidget.insertRow(rowPosition)
		newUrl = QtWidgets.QTableWidgetItem("")
		self.urlTableWidget.setItem(rowPosition, 0, newUrl)
		# add remove url button to the new row
		rmUrlBtn = QtWidgets.QPushButton(self.urlTableWidget)
		rmUrlBtn.setText('-')
		rmUrlBtn.clicked.connect(self.makeDeleteUrlLambda(rowPosition))
		self.urlTableWidget.setCellWidget(rowPosition, 1, rmUrlBtn)

	def deleteUrl(self, row: int):
		print("deleting Url...")
		self.urlTableWidget.removeRow(row)


	def makeDeleteUrlLambda(self, row: int):
		return lambda: self.deleteUrl(row)

	def setupUi(self, EditMenu):
		EditMenu.setObjectName("EditMenu")
		EditMenu.resize(648, 435)
		

		# MARK: - URLs
		self.centralwidget = QtWidgets.QWidget(EditMenu)
		self.centralwidget.setObjectName("centralwidget")
		self.urlTableWidget = QtWidgets.QTableWidget(self.centralwidget)
		self.urlTableWidget.setGeometry(QtCore.QRect(20, 60, 331, 231))
		self.urlTableWidget.setObjectName("urlTableWidget")
		self.urlTableWidget.setColumnCount(2)
		self.urlTableWidget.setRowCount(0)

		def loadUrlTableWidget():
			for url in getSubjectURLs(self.subjectID):
				# add row
				rowPosition = self.urlTableWidget.rowCount()
				self.urlTableWidget.insertRow(rowPosition)
				# link - url name
				link = QtWidgets.QTableWidgetItem(url)
				self.urlTableWidget.setItem(rowPosition, 0, link)
				# remove url button
				rmUrlBtn = QtWidgets.QPushButton(self.urlTableWidget)
				rmUrlBtn.setText('-')
				rmUrlBtn.clicked.connect(self.makeDeleteUrlLambda(rowPosition))
				self.urlTableWidget.setCellWidget(rowPosition, 1, rmUrlBtn)

			# add url button
			rowPosition = self.urlTableWidget.rowCount()
			self.urlTableWidget.insertRow(rowPosition)
			addUrlBtn = QtWidgets.QPushButton(self.urlTableWidget)
			addUrlBtn.setText('+')
			addUrlBtn.clicked.connect(lambda: self.addUrl())
			self.urlTableWidget.setCellWidget(rowPosition, 1, addUrlBtn)
			# create non editable field next to add button
			empty = QtWidgets.QTableWidgetItem("")
			empty.setFlags(QtCore.Qt.ItemIsEnabled)
			self.urlTableWidget.setItem(rowPosition, 0, empty)

			header = self.urlTableWidget.horizontalHeader()       
			header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

			item = QtWidgets.QTableWidgetItem()
			self.urlTableWidget.setVerticalHeaderItem(0, item)
			item = QtWidgets.QTableWidgetItem()
			self.urlTableWidget.setHorizontalHeaderItem(0, item)
			item = QtWidgets.QTableWidgetItem()
			self.urlTableWidget.setHorizontalHeaderItem(1, item)

		loadUrlTableWidget()

		# 'URLs'
		self.urlLabel = QtWidgets.QLabel(self.centralwidget)
		self.urlLabel.setGeometry(QtCore.QRect(150, 40, 58, 16))
		self.urlLabel.setAlignment(QtCore.Qt.AlignCenter)
		self.urlLabel.setObjectName("urlLabel")
		


		# MARK: - Zoom ----------------------------------------------------
		self.zoomTableWidget = QtWidgets.QTableWidget(self.centralwidget)
		self.zoomTableWidget.setGeometry(QtCore.QRect(370, 60, 256, 81))
		self.zoomTableWidget.setBaseSize(QtCore.QSize(0, 0))
		self.zoomTableWidget.setObjectName("zoomTableWidget")
		self.zoomTableWidget.setColumnCount(1)
		self.zoomTableWidget.setRowCount(2)

		zoomUrl = QtWidgets.QTableWidgetItem(getSubjectZoomURL(self.subjectID))
		self.zoomTableWidget.setItem(0, 0, zoomUrl)

		zoomPass = QtWidgets.QTableWidgetItem(getSubjectZoomPasscode(self.subjectID))
		self.zoomTableWidget.setItem(1, 0, zoomPass) 
		
		header = self.zoomTableWidget.horizontalHeader()
		header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
		item = QtWidgets.QTableWidgetItem()
		self.zoomTableWidget.setVerticalHeaderItem(0, item)
		item = QtWidgets.QTableWidgetItem()
		self.zoomTableWidget.setVerticalHeaderItem(1, item)
		item = QtWidgets.QTableWidgetItem()
		self.zoomTableWidget.setHorizontalHeaderItem(0, item)

		# 'Zoom Info'
		self.zoomLabel = QtWidgets.QLabel(self.centralwidget)
		self.zoomLabel.setGeometry(QtCore.QRect(470, 40, 71, 16))
		self.zoomLabel.setAlignment(QtCore.Qt.AlignCenter)
		self.zoomLabel.setObjectName("zoomLabel")
		



		# subject name editor
		self.textEdit = QtWidgets.QLineEdit(self.centralwidget)
		self.textEdit.setGeometry(QtCore.QRect(250, 10, 141, 31))
		self.textEdit.setObjectName("textEdit")
		
		
		
		# lonely buttons
		self.saveButton = QtWidgets.QPushButton(self.centralwidget)
		self.saveButton.setGeometry(QtCore.QRect(260, 320, 131, 32))
		self.saveButton.setObjectName("saveButton")
		self.saveButton.clicked.connect(lambda: self.save())
		
		self.deleteButton = QtWidgets.QPushButton(self.centralwidget)
		self.deleteButton.setGeometry(QtCore.QRect(261, 350, 131, 32))
		self.deleteButton.setObjectName("deleteButton")
		self.deleteButton.clicked.connect(lambda: self.delete())


		EditMenu.setCentralWidget(self.centralwidget)

		self.menubar = QtWidgets.QMenuBar(EditMenu)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 648, 22))
		self.menubar.setObjectName("menubar")
		self.menuFile = QtWidgets.QMenu(self.menubar)
		self.menuFile.setObjectName("menuFile")
		self.menuEdit = QtWidgets.QMenu(self.menubar)
		self.menuEdit.setObjectName("menuEdit")
		self.menuHelp = QtWidgets.QMenu(self.menubar)
		self.menuHelp.setObjectName("menuHelp")
		EditMenu.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(EditMenu)
		self.statusbar.setObjectName("statusbar")
		EditMenu.setStatusBar(self.statusbar)
		self.actionSave = QtWidgets.QAction(EditMenu)
		self.actionSave.setObjectName("actionSave")
		self.actionClose = QtWidgets.QAction(EditMenu)
		self.actionClose.setObjectName("actionClose")
		self.actionAdd_URL = QtWidgets.QAction(EditMenu)
		self.actionAdd_URL.setObjectName("actionAdd_URL")
		self.actionAdd_URL_2 = QtWidgets.QAction(EditMenu)
		self.actionAdd_URL_2.setObjectName("actionAdd_URL_2")
		self.actionDelete = QtWidgets.QAction(EditMenu)
		self.actionDelete.setObjectName("actionDelete")
		self.actionEdit_name = QtWidgets.QAction(EditMenu)
		self.actionEdit_name.setObjectName("actionEdit_name")
		self.actionClear_zoom_info = QtWidgets.QAction(EditMenu)
		self.actionClear_zoom_info.setObjectName("actionClear_zoom_info")
		self.actionClose_without_saving = QtWidgets.QAction(EditMenu)
		self.actionClose_without_saving.setObjectName("actionClose_without_saving")
		self.menuFile.addAction(self.actionSave)
		self.menuFile.addAction(self.actionClose)
		self.menuFile.addAction(self.actionClose_without_saving)
		self.menuEdit.addAction(self.actionAdd_URL)
		self.menuEdit.addAction(self.actionAdd_URL_2)
		self.menuEdit.addSeparator()
		self.menuEdit.addAction(self.actionEdit_name)
		self.menuEdit.addAction(self.actionClear_zoom_info)
		self.menuEdit.addSeparator()
		self.menuEdit.addAction(self.actionDelete)
		self.menubar.addAction(self.menuFile.menuAction())
		self.menubar.addAction(self.menuEdit.menuAction())
		self.menubar.addAction(self.menuHelp.menuAction())

		self.retranslateUi(EditMenu)
		QtCore.QMetaObject.connectSlotsByName(EditMenu)

	def retranslateUi(self, EditMenu):
		_translate = QtCore.QCoreApplication.translate
		EditMenu.setWindowTitle(_translate("EditMenu", "Edit Menu"))

		# TODO: make this situation a bit more stylish
		# EditMenu.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		# EditMenu.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		# EditMenu.setStyleSheet("background-color: rgba(30, 30, 30, .7)")

		item = self.urlTableWidget.horizontalHeaderItem(0)
		item.setText(_translate("EditMenu", "URL"))
		item = self.zoomTableWidget.verticalHeaderItem(0)
		item.setText(_translate("EditMenu", "Zoom link"))
		item = self.zoomTableWidget.verticalHeaderItem(1)
		item.setText(_translate("EditMenu", "Passcode (optional)"))

		self.textEdit.setText(_translate("EditMenu", getSubjectName(self.subjectID)))
		self.textEdit.setPlaceholderText(_translate("EditMenu", "Subject name"))
		self.urlLabel.setText(_translate("EditMenu", "URLs"))
		self.zoomLabel.setText(_translate("EditMenu", "Zoom Info"))
		self.saveButton.setText(_translate("EditMenu", "Save"))
		self.deleteButton.setText(_translate("EditMenu", "Delete subject"))
		self.menuFile.setTitle(_translate("EditMenu", "File"))
		self.menuEdit.setTitle(_translate("EditMenu", "Edit"))
		self.menuHelp.setTitle(_translate("EditMenu", "Help"))
		self.actionSave.setText(_translate("EditMenu", "Save"))
		self.actionSave.setShortcut(_translate("EditMenu", "Ctrl+S"))
		self.actionClose.setText(_translate("EditMenu", "Close"))
		self.actionClose.setShortcut(_translate("EditMenu", "Ctrl+W"))
		self.actionAdd_URL.setText(_translate("EditMenu", "Add Subject"))
		self.actionAdd_URL.setShortcut(_translate("EditMenu", "Ctrl+N"))
		self.actionAdd_URL_2.setText(_translate("EditMenu", "Add URL"))
		self.actionAdd_URL_2.setShortcut(_translate("EditMenu", "Ctrl+U"))
		self.actionDelete.setText(_translate("EditMenu", "Delete subject..."))
		self.actionDelete.setShortcut(_translate("EditMenu", "Ctrl+Backspace"))
		self.actionEdit_name.setText(_translate("EditMenu", "Edit name..."))
		self.actionClear_zoom_info.setText(_translate("EditMenu", "Clear zoom info"))
		self.actionClose_without_saving.setText(_translate("EditMenu", "Quit"))
		self.actionClose_without_saving.setShortcut(_translate("EditMenu", "Ctrl+E"))


# quick testing - hardcoded subject ID
# subID = 1
# if __name__ == "__main__":
# 	 import sys
# 	 app = QtWidgets.QApplication(sys.argv)
# 	 EditMenu = QtWidgets.QMainWindow()
# 	 ui = Ui_EditMenu(subID)
# 	 ui.setupUi(EditMenu)
# 	 EditMenu.show()
# 	 sys.exit(app.exec_())
