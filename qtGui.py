# Created by Oceanlight 

from PyQt5 import QtCore, QtGui, QtWidgets

from SQLquery import *
from SQLupdate import *
from qtEdit import Ui_EditMenu
# subprocess -> cpy, bash exec, webbrowser -> open links
import subprocess, webbrowser



class Ui_Dashboard(object):
	def openEditWindow(self, subjectID: int):
		self.window = QtWidgets.QMainWindow()
		self.subjectID = subjectID
		self.ui = Ui_EditMenu(self.subjectID)
		self.ui.setupUi(self.window)
		self.window.show()

	def makeOpenEditWindowLambda(self, subjectID: int):
		return lambda: self.openEditWindow(subjectID)


	def openUrls(self, subjectID: int):
		print(f"openUrls id: {subjectID}")
		for url in getSubjectURLs(subjectID):
			webbrowser.open(url, new=1)

	def makeOpenUrlsLambda(self, subjectID: int):
		return lambda: self.openUrls(subjectID)


	def openZoom(self, subjectID: int):
		print(f"openZoom id: {subjectID}")
		if (zoomURL := getSubjectZoomURL(subjectID)) != "":
			# open link in zoom
			bashCommand = "open -a zoom.us " + zoomURL
			subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
		else: 
			return
		if (zoomPass := getSubjectZoomPasscode(subjectID)) != "":
			# TODO: automate password entry
			# yank zoom password to clipboard (yeah I use vim haha)
			subprocess.run("pbcopy", universal_newlines=True, input=zoomPass)

	def makeOpenZoomLambda(self, subjectID: int):
		return lambda: self.openZoom(subjectID)

	# open new window with options to edit

	def addSubject(self):
		newSubjectID = addSubject("")
		self.openEditWindow(newSubjectID)
		# TODO: reload window?
		# update dashboard when changes are made to subject/name changed



	def setupUi(self, Dashboard):
		Dashboard.setObjectName("Subject Dashboard")
		Dashboard.resize(647, 406)
		Dashboard.setAutoFillBackground(False)
		Dashboard.setStyleSheet("")

		self.centralwidget = QtWidgets.QWidget(Dashboard)
		self.centralwidget.setObjectName("centralwidget")
		self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
		self.tableWidget.setGeometry(QtCore.QRect(10, 10, 630, 351))
		self.tableWidget.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
		# hide column && row numbers
		self.tableWidget.verticalHeader().setVisible(False)
		self.tableWidget.horizontalHeader().setVisible(False)
		

		# no. of subjects
		# self.tableWidget.setRowCount(len(getAllSubjectIDs()))
		self.tableWidget.setRowCount(0)
		self.tableWidget.setColumnCount(4)
		self.tableWidget.setObjectName("tableWidget")
		# append each subject
		# FOR each subject, add 1) name 2) open URLs (button) 3) open zoom (button) 4) edit
		for subjectID in getAllSubjectIDs():
			# add row
			rowPosition = self.tableWidget.rowCount()
			self.tableWidget.insertRow(rowPosition)
			
			# name
			name = QtWidgets.QTableWidgetItem(getSubjectName(subjectID))
			name.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  # make cell not editable
			self.tableWidget.setItem(rowPosition, 0, name)


			# open urls button
			openUrlBtn = QtWidgets.QPushButton(self.tableWidget)
			openUrlBtn.setText('Open URLs')
			# disable button if subject has no urls
			# note that empty of invalid urls will still pass
			if getSubjectURLs(subjectID) == []:
				openUrlBtn.setEnabled(False)
			else:
				openUrlBtn.clicked.connect(self.makeOpenUrlsLambda(subjectID))
			self.tableWidget.setCellWidget(rowPosition, 1, openUrlBtn)
			

			# open zoom button
			openZoomBtn = QtWidgets.QPushButton(self.tableWidget)
			openZoomBtn.setText('Open meeting')
			# disable button if subject has no zoom link
			zoomUrl = getSubjectZoomURL(subjectID)
			if zoomUrl == "" or zoomUrl == None:
				openZoomBtn.setEnabled(False)
			else:
				openZoomBtn.clicked.connect(self.makeOpenZoomLambda(subjectID))
			self.tableWidget.setCellWidget(rowPosition, 2, openZoomBtn)

			# edit subject
			editSubjectBtn = QtWidgets.QPushButton(self.tableWidget)
			editSubjectBtn.setText('Edit...')
			editSubjectBtn.clicked.connect(self.makeOpenEditWindowLambda(subjectID))
			self.tableWidget.setCellWidget(rowPosition, 3, editSubjectBtn)
			
			header = self.tableWidget.horizontalHeader()       
			header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
			header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
			header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

		# add subject
		rowPosition = self.tableWidget.rowCount()
		self.tableWidget.insertRow(rowPosition)
		addSubjectBtn = QtWidgets.QPushButton(self.tableWidget)
		addSubjectBtn.setText("Add Subject")
		addSubjectBtn.clicked.connect(lambda: self.addSubject())
		self.tableWidget.setCellWidget(rowPosition, 0, addSubjectBtn)


		Dashboard.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(Dashboard)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 647, 22))
		self.menubar.setObjectName("menubar")

		self.menuEdit_s_this = QtWidgets.QMenu(self.menubar)
		self.menuEdit_s_this.setObjectName("menuEdit_s_this")
		self.menuFile = QtWidgets.QMenu(self.menubar)
		self.menuFile.setObjectName("menuFile")
		self.menuRun = QtWidgets.QMenu(self.menubar)
		self.menuRun.setObjectName("menuRun")
		self.menuHelp = QtWidgets.QMenu(self.menubar)
		self.menuHelp.setObjectName("menuHelp")

		Dashboard.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(Dashboard)
		self.statusbar.setObjectName("statusbar")
		Dashboard.setStatusBar(self.statusbar)
		self.actionNew_subject = QtWidgets.QAction(Dashboard)
		self.actionNew_subject.setObjectName("actionNew_subject")
		self.actionEdit_subject = QtWidgets.QAction(Dashboard)
		self.actionEdit_subject.setObjectName("actionEdit_subject")
		self.actionOpen_zoom = QtWidgets.QAction(Dashboard)
		self.actionOpen_zoom.setObjectName("actionOpen_zoom")
		self.actionOpen_urls = QtWidgets.QAction(Dashboard)
		self.actionOpen_urls.setObjectName("actionOpen_urls")
		self.actionDelete_subject = QtWidgets.QAction(Dashboard)
		self.actionDelete_subject.setObjectName("actionDelete_subject")
		self.menuEdit_s_this.addSeparator()
		self.menuEdit_s_this.addAction(self.actionNew_subject)
		self.menuEdit_s_this.addAction(self.actionDelete_subject)
		self.menuFile.addSeparator()
		self.menuFile.addAction(self.actionEdit_subject)
		self.menuRun.addAction(self.actionOpen_zoom)
		self.menuRun.addAction(self.actionOpen_urls)
		self.menubar.addAction(self.menuEdit_s_this.menuAction())
		self.menubar.addAction(self.menuFile.menuAction())
		self.menubar.addAction(self.menuRun.menuAction())
		self.menubar.addAction(self.menuHelp.menuAction())

		self.retranslateUi(Dashboard)
		QtCore.QMetaObject.connectSlotsByName(Dashboard)

	def retranslateUi(self, Dashboard):
		_translate = QtCore.QCoreApplication.translate
		Dashboard.setWindowTitle(_translate("Dashboard", "Dashboard"))
		self.menuEdit_s_this.setTitle(_translate("Dashboard", "File"))
		self.menuFile.setTitle(_translate("Dashboard", "Edit"))
		self.menuRun.setTitle(_translate("Dashboard", "Run"))
		self.menuHelp.setTitle(_translate("Dashboard", "Help"))
		self.actionNew_subject.setText(_translate("Dashboard", "New subject..."))
		self.actionNew_subject.setStatusTip(_translate("Dashboard", "Create a new subject"))
		self.actionNew_subject.setShortcut(_translate("Dashboard", "Ctrl+N"))
		self.actionEdit_subject.setText(_translate("Dashboard", "Edit subject..."))
		self.actionOpen_zoom.setText(_translate("Dashboard", "Open zoom..."))
		self.actionOpen_urls.setText(_translate("Dashboard", "Open urls..."))
		self.actionDelete_subject.setText(_translate("Dashboard", "Delete subject..."))



if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	Dashboard = QtWidgets.QMainWindow()
	ui = Ui_Dashboard()
	ui.setupUi(Dashboard)
	Dashboard.show()
	sys.exit(app.exec_())
