#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,subprocess,re,xlwt,datetime
from collections import OrderedDict
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        
        button1 = QPushButton("Browse")
        button5 = QPushButton("Save")
        buttonBoxOk = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBoxCanc = QDialogButtonBox(QDialogButtonBox.Cancel)
        
        self.label1 = QLabel("<font color=grey size=2>Select the data file missing time infromation</font>")
        self.label5 = QLabel("<font color=grey size=2>Select a name for the output file</font>")
        
        self.lineedit1 = QLineEdit()
        self.lineedit5 = QLineEdit()
        
        descr1 = QLabel("Input .csv file of missing time infromation data")
        descr3 = QLabel("Output .csv file of temporal data")
        
        grid = QGridLayout()
        grid.addWidget(descr1, 0, 0)
        grid.addWidget(self.label1, 1, 0)
        grid.addWidget(self.lineedit1,2,0)
        grid.addWidget(button1, 2, 1)
        grid.addWidget(descr3, 3, 0)
        grid.addWidget(self.label5, 4, 0)
        grid.addWidget(self.lineedit5,5,0)
        grid.addWidget(button5, 5, 1)
        grid.addWidget(buttonBoxCanc, 6, 0)
        grid.addWidget(buttonBoxOk, 6, 1)
        
#        grid.addWidget(self.label5, 3, 0)
#        grid.addWidget(self.lineedit5,4,0)
#        grid.addWidget(button5, 4, 1)
#        grid.addWidget(buttonBoxCanc, 5, 0)
#        grid.addWidget(buttonBoxOk, 5, 1)
        
        self.setLayout(grid)
        
        self.connect(button1, SIGNAL("clicked()"), self.clicked1)
        self.connect(button5, SIGNAL("clicked()"), self.clicked5)
        buttonBoxOk.accepted.connect(self.accept)
        buttonBoxCanc.rejected.connect(self.reject)

        self.setWindowTitle("Add duration tool")
        
    def clicked1(self):      
        nomeFile=QFileDialog.getOpenFileNames(self,"Select Input File")
        self.label1.setText(nomeFile.takeFirst())
        self.lineedit1.clear()
        doc = QTextDocument()
        doc.setHtml(self.label1.text())
        text = doc.toPlainText()
        self.lineedit1.insert( text )
        self.label1.setText("<font color=grey size=2>Select the missing time infromation data</font>")
        self.inputFile = text
   
    def clicked5(self):      
        nomeFile=QFileDialog.getSaveFileName(self,"Select Output File")
        self.label5.setText(nomeFile)
        self.lineedit5.clear()
        doc = QTextDocument()
        doc.setHtml(self.label5.text())
        text = doc.toPlainText()
        self.lineedit5.insert( text )
        self.label5.setText("<font color=grey size=2>Save the temporal file</font>")
        self.outputFile = text
        
    def accept(self):
		try:
			if self.inputFile and self.outputFile:
				r=open(self.inputFile,'r')
				d=r.readlines()
				e=d[2:]
				o=open(self.outputFile,'w')
				o.writelines(d[0].split('\n')[0]+";;")
				o.writelines("\n")
				o.writelines(d[1].split('\n')[0]+";START;END")
				o.writelines("\n")
				for i in e:
					if i.split(';')[5] == 'transport passagers':
						dur=1
					elif i.split(';')[5] == 'pêche professionnelle':
						dur=6
					elif i.split(';')[5] == 'course/régate':
						dur=8
					elif i.split(';')[5] == 'transport fret':
						dur=1
					elif i.split(';')[5] == 'activité scientifique':
						dur=8
					elif i.split(';')[5] == 'plongée':
						dur=4
					elif i.split(';')[5] == 'pêche plaisance':
						dur=4
					elif i.split(';')[5] == 'voilier école':
						dur=3
					elif i.split(';')[5] == 'sauvetage en mer':
						dur=2
					elif i.split(';')[5] == 'plaisance':
						dur=4
					elif i.split(';')[5] == 'indéterminé':
						dur=1
					elif i.split(';')[5] == 'surveillance côtière':
						dur=1
					elif i.split(';')[5] == 'travaux maritimes':
						dur=8
					elif i.split(';')[5] == 'croisière':
						dur=1
					elif i.split(';')[5] == 'militaire':
						dur=1
					elif i.split(';')[5] == 'SAMU':
						dur=1
					ye=i.split(';')[1].split('/')[2]
					if len(i.split(';')[1].split('/')[1]) == 1:
						mo='0'+i.split(';')[1].split('/')[1]
					else: mo=i.split(';')[1].split('/')[1]
					if len(i.split(';')[1].split('/')[0]) == 1:
						da='0'+i.split(';')[1].split('/')[0]
					else: da=i.split(';')[1].split('/')[0]
					if len(i.split(';')[2].split(':')[0]) == 1:
						ho='0'+i.split(';')[2].split(':')[0]
					else: ho=i.split(';')[2].split(':')[0]
					try:
						if len(i.split(';')[2].split(':')[1]) == 1:
							mi='0'+i.split(';')[2].split(':')[1]
					#here I decided to prune each missing temporal information record
					except IndexError:
						continue
					else: mi=i.split(';')[2].split(':')[1]
					if len((i.split(';')[2].split(':')[2]).split(' ')[0]) == 1:
						se='0'+(i.split(';')[2].split(':')[2]).split(' ')[0]
					else: se=(i.split(';')[2].split(':')[2]).split(' ')[0]
					if (i.split(';')[2].split(':')[2]).split(' ')[1] == 'PM':
						ho=str(int(ho)+12)
					if ho == '24': ho='00'	
					start=ye+'-'+mo+'-'+da+' '+ho+':'+mi+':'+se
					#add duration
					mytime = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
					mytime += datetime.timedelta(hours=dur)
					end=mytime.strftime("%Y-%m-%d %H:%M:%S")
					o.writelines(i.split('\n')[0]+";"+start+";"+end)
					o.writelines("\n")
				o.close()
				QMessageBox.warning(self,"Warning", "Elaboration finished", unicode())
				sys.exit()
		except AttributeError:
			QMessageBox.warning(self,"Warning", "Please fill all the requested fields before starting processing", unicode())

    
        
def main():
	app = QApplication(sys.argv)
	form = Form()
	form.show()
	return app.exec_()

if __name__ == '__main__':
    main()
