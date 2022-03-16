'''
TagTool - 2022
author: SappI
'''

import os
import pandas as pd
from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import pickle
import platform

# Import UI files
from ui.mainWindow import Ui_MainWindow
from ui.editor import Ui_editorWindow
from ui.diag import Ui_aboutWindow
from ui.newItem import Ui_newItemWindow
from ui.pageSelect import Ui_pageWindow

# Update this with each release
appName = "TagTool"
versionNumber = "1.5.0"
appPath = os.path.dirname(__file__)
platName = platform.system()
dataLoc = QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.DataLocation)[0] + f'/{appName}'

# Window classes
class mainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.setupUi(self)        
        self.act_quit.triggered.connect(quitApp)
        self.act_open.triggered.connect(openFile)
        self.act_clearTable.triggered.connect(clearTable)
        self.act_about.triggered.connect(showAbout)
        self.act_editor.triggered.connect(showEditor)
        self.btnSetColumn.clicked.connect(setCol)
        self.btnTagAll.clicked.connect(tagAll)
        self.btnTagEach.clicked.connect(tagEach)
        self.btn_save.clicked.connect(saveFile)
        self.menu_openFile.triggered.connect(openFile)
        self.menu_keywordEditor.triggered.connect(showEditor)
        self.menu_clearTable.triggered.connect(clearTable)

class editorWindow(QtWidgets.QMainWindow, Ui_editorWindow):
    def __init__(self):
        super(editorWindow, self).__init__()
        self.setupUi(self)
        
        self.act_close.triggered.connect(closeEditor)
        self.act_save.triggered.connect(saveDefault)
        self.btn_newEntry.clicked.connect(newEntry)
        self.btn_deleteEntry.clicked.connect(deleteEntry)
        self.btn_save.clicked.connect(saveAndClose)
        self.tblEdit.cellChanged.connect(cellTest)
        self.act_import.triggered.connect(importCSV)
        self.act_export.triggered.connect(exportCSV)
        self.btnImport.clicked.connect(importCSV)
        self.btnExport.clicked.connect(exportCSV)

class aboutWindow(QtWidgets.QMainWindow, Ui_aboutWindow):
    def __init__(self):
        super(aboutWindow, self).__init__()
        self.setupUi(self)
        self.btnOk.clicked.connect(closeAbout)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
        self.lblVersion.setText(f'Version {versionNumber}')

class newItem(QtWidgets.QMainWindow, Ui_newItemWindow):
    def __init__(self):
        super(newItem, self).__init__()
        self.setupUi(self)
        self.btnCreate.clicked.connect(createNewItem)
        self.btnCancel.clicked.connect(closeNewItem)

class pageSelect(QtWidgets.QMainWindow, Ui_pageWindow):
    def __init__(self):
        super(pageSelect, self).__init__()
        self.setupUi(self)
        self.btnForward.clicked.connect(lambda: changePage(False))
        self.btnBack.clicked.connect(lambda: changePage(True))
        self.btnOpen.clicked.connect(openPage)

# Globals
df = pd.DataFrame
dfEditor = pd.DataFrame
dfNew = pd.DataFrame
dfPage = pd.DataFrame
fileLoaded = False
activeColumn = 0
editorLoaded = False
pageNum = 0
numberOfPages = 0
excelFile = ''

# Data from res.dat will be stored in this dictionary
iconDict = {}

# Initialize the app
app = QtWidgets.QApplication([])

# Create a DF
def createDF(fName):
    if ".csv" in fName:
        df = pd.read_csv(fName)
        return df
    elif ".xlsx" in fName:
        df = pd.read_excel(fName)
        return df

def readDat(datFile):
    # Reads resource data packed in the res.dat file
    global iconDict
    f=open(datFile, 'rb')
    iconDict = pickle.load(f)
    f.close()

def showAbout():
    uiDiag.show()

# Show error message
def errorMessage(text, title):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText(text)
    msg.setWindowTitle(title)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    retval = msg.exec()

def showEditor():
    uiEditor.show()
    populateEditor()


def importCSV():
    try:
        filename = QtWidgets.QFileDialog.getOpenFileName(None, 'Select Dir', os.getcwd(), "CSV files(*.csv)")[0]
    except:
        print("No file found")
    if filename:
        global dfEditor
        #tempDF = pd.DataFrame
        tempDF = pd.read_csv(filename)
        tempDF.columns = tempDF.columns.str.lower()
        if 'category' in tempDF.columns and 'keywords' in tempDF.columns and 'blacklist' in tempDF.columns:
            print("SUCCESS")
            tempDF.drop(tempDF.columns.difference(['category', 'keywords','blacklist']), 1, inplace=True)
            tempDF.rename(columns={'category': 'Category', 'keywords': 'Keywords', 'blacklist': 'Blacklist'}, inplace=True)
            tempDF = tempDF[["Category", "Keywords", "Blacklist"]]
            dfEditor = tempDF
            write_dt_to_Editor(dfEditor, editorTable)
        else:
            errorMessage("Please make sure Category, Keywords, and Blacklist\nare all column names in the file and try again.", "Error reading CSV")

def exportCSV():
    global dfEditor
    try:
        filename = QtWidgets.QFileDialog.getSaveFileName(None, 'Save File', os.getcwd(), "CSV Files(*.csv)")[0]
        print(filename)
        dfEditor.to_csv(str(filename), index=False)
    except:
        pass

def showNewItem():
    uiNewItem.txtEntryName.clear()
    uiNewItem.show()

def closeNewItem():
    uiNewItem.close()

# Change the color of rows depending on column
# Needs RGB values passed
def colorRows(table, column, r, g, b):
    col = column
    for row in range(table.rowCount()):
        table.item(row, col).setBackground(QtGui.QColor(r,g,b))

def createNewItem():
    # Add new item to the DF and then update the editor table with updated DF
    global dfEditor
    categoryName = uiNewItem.txtEntryName.text()
    if len(categoryName.strip(' ')) < 1:
        errorMessage("Category cannot be empty", "Error")
        uiNewItem.txtEntryName.clear()
    else:
        newRow = {'Category':f'{categoryName}', 'Keywords':"", 'Blacklist':""}
        dfEditor = dfEditor.append(newRow, ignore_index=True)
        uiNewItem.close()
        write_dt_to_Editor(dfEditor, editorTable)

def saveAndClose():
    global dfEditor
    try:
        if platName == 'Darwin':
            dfEditor.to_json(f'{appPath}/default.json', orient='records')
        else:
            dfEditor.to_json('default.json', orient='records')
        uiEditor.close()
    except:
        errorMessage("Error saving default.json\nYou may not have sufficient write access to the default directory.")

def saveDefault():
    global df
    if platName == 'Darwin':
        dfEditor.to_json(f'{appPath}/default.json', orient='records')
    else:
        dfEditor.to_json('default.json', orient='records')
    setEditorStatus("Default config saved")

def setEditorStatus(text):
    editorStatusBar.showMessage(text)

def quitApp():
    sys.exit()

def selectPage(fName):
    global dfPage
    global pageTable
    global pageNum
    global numberOfPages
    global excelFile
    pageNum = 0
    uiPageSelect.show()
    # Store the excel filename as a global var
    excelFile = fName
    xls = pd.ExcelFile(excelFile)
    numberOfPages = len(xls.sheet_names)
    # Read in the excel file and get the sheet name based off
    # xls's index to pageNum
    dfPage = pd.read_excel(excelFile, sheet_name=xls.sheet_names[pageNum])
    write_dt_to_pageSelect(dfPage, pageTable)
    uiPageSelect.lblPageNum.setText(f"Page {pageNum + 1}")

def changePage(isBack = False):
    global pageNum
    global dfPage
    global numberOfPages
    global excelFile
    try:
        if isBack == False:
            if pageNum < numberOfPages - 1:
                pageNum = pageNum + 1
                # Have to create a new xls item here
                # so we can access page names.
                xls = pd.ExcelFile(excelFile)
                dfPage = pd.read_excel(excelFile, sheet_name=xls.sheet_names[pageNum])
                write_dt_to_pageSelect(dfPage, pageTable)
                uiPageSelect.lblPageNum.setText(f"Page {pageNum + 1}")
        else:
            if pageNum > 0:
                pageNum = pageNum - 1
                # Have to create a new xls item here
                # so we can access page names.
                xls = pd.ExcelFile(excelFile)
                dfPage = pd.read_excel(excelFile, sheet_name=xls.sheet_names[pageNum])
                write_dt_to_pageSelect(dfPage, pageTable)
                uiPageSelect.lblPageNum.setText(f"Page {pageNum + 1}")
    except:
        print("null value")

def openPage():
    global df
    global dfPage
    uiPageSelect.close()
    # Store the contents of dfPage into the primary
    # df object and write it to the table.
    df = dfPage
    write_dt_to_qTable(df, table)
    ui.btnSetColumn.setEnabled(True)

def openFile():
    global table
    global df
    global fileLoaded
    try:
        filename = QtWidgets.QFileDialog.getOpenFileName(None, 'Select Dir', os.getcwd(), "CSV or Excel files (*.csv *.xlsx)")[0]
    except:
        print("No file found")
    if filename:
        if ".csv" in filename:
            try:
                df = createDF(filename)
                write_dt_to_qTable(df, table)
                fileLoaded = True
                ui.btnSetColumn.setEnabled(True)
            except:
                errorMessage("Error opening file", "Error")
        if ".xlsx" in filename:
            xls = pd.ExcelFile(filename)
            # If the length of the excel file is 1 just
            # load that into the DF
            if len(xls.sheet_names) == 1:
                df = createDF(filename)
                write_dt_to_qTable(df, table)
                fileLoaded = True
                ui.btnSetColumn.setEnabled(True)
            # If there are more than 1 page in the excel file
            # we then run it through the select page screen
            elif len(xls.sheet_names) > 1:
                selectPage(filename)
            else:
                print("Empty Excel file")
    else:
        print("Empty filename")

def tagAll():
    global df
    global dfNew
    global activeColumn
    global progressBar

    saveButton.setEnabled(False)
    dfNew = df.copy()
    dfNew['Topic Categories'] = ''

    # Convert all data to string. Function crashes if its another datatype
    dfNew = dfNew.astype(str)

    if platName == 'Darwin':
        dfJson = pd.read_json(f'{appPath}/default.json')
    else:
        dfJson = pd.read_json("default.json")

    check = False
    commentList = []

    # Loop through each table item and add the text to the
    # commentList list
    for x in dfNew.index:
        commentList.append(dfNew.iloc[x,activeColumn])

    # Set progress bar to the length of the commentList
    progressBar.setMaximum(len(commentList))

    for stringIndex, item in enumerate(commentList):
        string = item
        check = False
        for index, row in dfJson.iterrows():
            blacklistWords = row['Blacklist'].split(",")
            keywords = row['Keywords'].split(",")
            category = row['Category']
            check = False

            # Loop through the blacklist and attempt to find a match.
            # If match, delete that word before we perform a search
            for word in blacklistWords:
                if len(word) > 0:
                    if word in string.lower():
                        string = string.replace(word, '')

            # Loop through the keywords and look for a match
            # if a match is found, we can enable the CHECK
            # variable which prevents it from counting the word
            # twice.
            for word in keywords:                
                if len(word) > 0:
                    if word in string.lower() and check == False:
                        if len(dfNew['Topic Categories'].iloc[stringIndex]) < 1:
                            dfNew['Topic Categories'].iloc[stringIndex] = category
                        else:
                            dfNew['Topic Categories'].iloc[stringIndex] = dfNew['Topic Categories'].iloc[stringIndex] + f', {category}'
                        check = True
        # Update the progress bar and process the changes
        # so the UI updates.
        progressBar.setValue(stringIndex)
        app.processEvents()
    progressBar.setValue(0)
    write_dt_to_qTable(dfNew, table)
    colorRows(table, activeColumn, 129, 189, 147)
    saveButton.setEnabled(True)

def tagEach():
    global df
    global dfNew
    global activeColumn
    global progressBar

    saveButton.setEnabled(False)
    dfNew = df.copy()

    dfNew = dfNew.astype(str)

    if platName == 'Darwin':
        dfJson = pd.read_json(f'{appPath}/default.json')
    else:
        dfJson = pd.read_json("default.json")
    check = False
    commentList = []
    
    for index, row in dfJson.iterrows():
        category = row['Category']
        dfNew[category] = ''

    for x in dfNew.index:
        commentList.append(dfNew.iloc[x,activeColumn])
    
    progressBar.setMaximum(len(commentList))
        
    for stringIndex, item in enumerate(commentList):
        string = item
        check = False
        for index, row in dfJson.iterrows():
            blacklistWords = row['Blacklist'].split(",")
            keywords = row['Keywords'].split(",")
            category = row['Category']           
            check = False
            for word in blacklistWords:
                if len(word) > 0:
                    if word in string.lower():
                        string = string.replace(word, '')

            for word in keywords:                
                if len(word) > 0:
                    if word in string.lower() and check == False:                     
                        dfNew[category].iloc[stringIndex] = 'Y'
                        check = True
        progressBar.setValue(stringIndex)
        app.processEvents()
    progressBar.setValue(0)
    write_dt_to_qTable(dfNew, table)
    saveButton.setEnabled(True)

def clearTable():
    global df
    global table
    global activeColumn
    saveButton.setEnabled(False)
    df = pd.DataFrame(None)
    write_dt_to_qTable(df, table)
    ui.btnTagAll.setEnabled(False)
    ui.btnTagEach.setEnabled(False)
    ui.btnSetColumn.setEnabled(False)
    ui.txtActiveStat.setText('No Active Column selected')
    activeColumn = 0

def setCol():
    global table
    global activeColumn
    colorRows(table, activeColumn, 255, 255, 255)
    activeColumn = table.currentColumn()
    colorRows(table, activeColumn, 129, 189, 147)
    table.clearSelection()
    ui.txtActiveStat.setText(f'The current active column is {activeColumn + 1}')
    ui.btnTagAll.setEnabled(True)
    ui.btnTagEach.setEnabled(True)
    print(activeColumn)

def closeEditor():
    uiEditor.close()

def populateEditor():
    global dfEditor
    global editorLoaded
    editorLoaded = False
    try:
        if platName == 'Darwin':
            dfEditor = pd.read_json(f'{appPath}/default.json')
        else:
            dfEditor = pd.read_json("default.json")

        write_dt_to_Editor(dfEditor, editorTable)
        editorLoaded = True
    except:
        errorMessage("default.json not found!", "Error")
        closeEditor()

def write_dt_to_qTable(df, table):
    headers = list(df)
    table.setRowCount(df.shape[0])
    table.setColumnCount(df.shape[1])
    table.setHorizontalHeaderLabels(headers)
    df_array = df.values
    for row in range(df.shape[0]):
        for col in range(df.shape[1]):
            table.setItem(row, col, QtWidgets.QTableWidgetItem(str(df_array[row,col])))

def write_dt_to_Editor(df, editorTable):
        global editorLoaded
        editorLoaded = False
        headers = list(df)
        editorTable.setRowCount(df.shape[0])
        editorTable.setColumnCount(df.shape[1])
        editorTable.setHorizontalHeaderLabels(headers)
        df_array = df.values
        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                editorTable.setItem(row, col, QtWidgets.QTableWidgetItem(str(df_array[row,col])))
        editorLoaded = True

def write_dt_to_pageSelect(df, pageTable):
    headers = list(df)
    pageTable.setRowCount(df.shape[0])
    pageTable.setColumnCount(df.shape[1])
    pageTable.setHorizontalHeaderLabels(headers)
    df_array = df.values
    for row in range(df.shape[0]):
        for col in range(df.shape[1]):
            pageTable.setItem(row, col, QtWidgets.QTableWidgetItem(str(df_array[row,col])))
    

def newEntry():
    showNewItem()

def deleteEntry():
    global dfEditor
    index = editorTable.currentRow()
    print(index)
    if index != -1:
        dfEditor = dfEditor.drop(index, axis=0)
        dfEditor.reset_index(drop=True, inplace=True)
        write_dt_to_Editor(dfEditor, editorTable)
    else:
        pass

def cellTest():
    global dfEditor
    global editorLoaded
    if editorLoaded:
        print("cell changed")
        col = uiEditor.tblEdit.currentColumn()
        row = uiEditor.tblEdit.currentRow()
        tableItem = uiEditor.tblEdit.item(row, col).text()
        print(tableItem)
        dfEditor.iloc[row, col] = tableItem.replace(', ', ',')
        write_dt_to_Editor(dfEditor, editorTable)
        editorStatusBar.showMessage(str(tableItem))

def saveFile():
    global dfNew
    try:
        filename = QtWidgets.QFileDialog.getSaveFileName(None, 'Save File', os.getcwd(), "CSV Files(*.csv)")[0]
        print(filename)
        dfNew.to_csv(str(filename), index=False)
    except:
        pass

def iconFromBase64(base64):
    pixmap = QtGui.QPixmap()
    pixmap.loadFromData(QtCore.QByteArray.fromBase64(base64))
    icon = QtGui.QIcon(pixmap)
    return icon

def imageFromBase64(base64):
    pixmap = QtGui.QPixmap()
    pixmap.loadFromData(QtCore.QByteArray.fromBase64(base64))
    return pixmap

def closeAbout():
    uiDiag.close()

def loadData():
    try:
        if platName == 'Darwin':
            readDat(f'{appPath}/res.dat')
        else:
            readDat('res.dat')
        
        app.setWindowIcon(iconFromBase64(bytes(iconDict['icon.png'], encoding='utf8')))
        ui.menu_openFile.setIcon(iconFromBase64(bytes(iconDict['folder.png'], encoding='utf8')))
        ui.menu_keywordEditor.setIcon(iconFromBase64(bytes(iconDict['keyword.png'], encoding='utf8')))
        ui.menu_clearTable.setIcon(iconFromBase64(bytes(iconDict['clear.png'], encoding='utf8')))
        uiDiag.pixLogo.setPixmap(imageFromBase64(bytes(iconDict['logo.png'], encoding='utf8')))
    except:
        errorMessage('Could not load res.dat\nApplication will still run without graphical icons and logos.', 'Error')
        uiDiag.pixLogo.setText("TagTool")

# Set up the window objects        
ui = mainWindow()
uiEditor = editorWindow()
uiDiag = aboutWindow()
uiNewItem = newItem()
uiPageSelect = pageSelect()

# Variables
table = ui.tableWidget
progressBar = ui.progressBar
saveButton = ui.btn_save
editorTable = uiEditor.tblEdit
pageTable = uiPageSelect.tblPage
editorStatusBar = uiEditor.statusbar

# Load in the image data from res.dat
loadData()

print(dataLoc)

# Show main window and exec the program
ui.show()
app.exec()