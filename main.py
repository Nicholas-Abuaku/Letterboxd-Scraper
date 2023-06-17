import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog,QTableWidgetItem, QHeaderView
from PyQt6.QtCore import pyqtSlot, QFile, QTextStream, pyqtSignal, Qt
from SentiScraper import Ui_MainWindow
import resources
from webScraper import ReviewScraper
from sentimentAnalyser import sentimentAnalyser
import pandas as pd
res = {}
results_df = []
class MainWindow(QMainWindow):
    progressUpdate = pyqtSignal(int)
    def __init__(self):
        super(MainWindow,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.scraperMenuButton.setChecked(True)
        self.ui.beginScrapeButton.clicked.connect(self.startScraper)
        self.ui.openCSV.clicked.connect(self.browseFiles)
        self.ui.exportResultsButton.clicked.connect(self.exportResults)
        self.ui.analyzeButton.clicked.connect(self.runSentiment)
        self.ui.viewAllReviews.clicked.connect(self.viewComments)
        
    

    
    def on_stackedWidget_currentChanged(self,index):
        buttonList = self.ui.menuBar.findChildren(QPushButton)

        for btn in buttonList:
            if index in [0,1]:
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)
    
    def on_scraperMenuButton_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)
    
    def on_sentimentMenuButton_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    
    
    def startScraper(self):
        url = self.ui.lineEdit.text()
        scraper = ReviewScraper(url)
        maxComments = 500
        scraper.scrape_reviews(500)

    
    def viewComments(self):
        df = results_df
        self.ui.reviewTable.setColumnCount(df.shape[1])
        self.ui.reviewTable.setRowCount(df.shape[0])
        self.ui.reviewTable.setHorizontalHeaderLabels(df.columns)
        
        header = self.ui.reviewTable.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        column_width = 600
        for j in range(df.shape[1]):
            self.ui.reviewTable.setColumnWidth(j, column_width)

        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                item = QTableWidgetItem(str(df.iat[i,j]))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.ui.reviewTable.setItem(i, j, item)

    def browseFiles(self):
        fname = QFileDialog.getOpenFileName(self, 'Open File','C:\\Users','CSV Files (*.csv)')
        self.ui.pathToCSV.setText(fname[0])
    
    def runSentiment(self):
        global results_df
        sA = sentimentAnalyser(self.ui.pathToCSV.text())
        for i, row in sA.df.iterrows():
            try:
                text = row['Reviews']
                myid = row['ID']
                roberta_results = sA.polarity_scores_roberta(text)
                res[myid] = roberta_results
                
                results_df = pd.DataFrame(res).T
                results_df['ID'] = results_df.index
                results_df = results_df.merge(sA.df,how='left')  
            except RuntimeError:
                print("An error has occured")
    
    def exportResults(self):
        results_df.to_csv('results.csv',index=False)
        
        


    

    


if __name__=="__main__":
    app =  QApplication(sys.argv)
    window = MainWindow()
    window.show()


    sys.exit(app.exec())
