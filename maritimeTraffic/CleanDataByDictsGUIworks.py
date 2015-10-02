#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,subprocess,re,xlwt
from collections import OrderedDict
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        
        button1 = QPushButton("Browse")
        button2 = QPushButton("Browse")
        button3 = QPushButton("Browse")
        button4 = QPushButton("Browse")
        button5 = QPushButton("Save")
        buttonBoxOk = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBoxCanc = QDialogButtonBox(QDialogButtonBox.Cancel)
        
        self.label1 = QLabel("<font color=grey size=2>Select the raw data file</font>")
        self.label2 = QLabel("<font color=grey size=2>Select the boat type dictionary file</font>")
        self.label3 = QLabel("<font color=grey size=2>Select the boat routes dictionary file</font>")
        self.label4 = QLabel("<font color=grey size=2>Select the boat usage dictionary file</font>")
        self.label5 = QLabel("<font color=grey size=2>Select the clean file</font>")
        
        self.lineedit1 = QLineEdit()
        self.lineedit2 = QLineEdit()
        self.lineedit3 = QLineEdit()
        self.lineedit4 = QLineEdit()
        self.lineedit5 = QLineEdit()
        
        descr1 = QLabel("Input .csv file of raw data")
        descr2 = QLabel("Recall Dictionaries")
        descr3 = QLabel("Output .xls file of output clean data")
        
        grid = QGridLayout()
        grid.addWidget(descr1, 0, 0)
        grid.addWidget(self.label1, 1, 0)
        grid.addWidget(self.lineedit1,2,0)
        grid.addWidget(button1, 2, 1)
        grid.addWidget(descr2, 3, 0)
        grid.addWidget(self.label2, 4, 0)
        grid.addWidget(self.lineedit2,5,0)
        grid.addWidget(button2, 5, 1)
        grid.addWidget(self.label3, 6, 0)
        grid.addWidget(self.lineedit3,7,0)
        grid.addWidget(button3, 7, 1)
        grid.addWidget(self.label4, 8, 0)
        grid.addWidget(self.lineedit4,9,0)
        grid.addWidget(button4, 9, 1)
        grid.addWidget(descr3, 10, 0)
        grid.addWidget(self.label5, 11, 0)
        grid.addWidget(self.lineedit5,12,0)
        grid.addWidget(button5, 12, 1)
        grid.addWidget(buttonBoxCanc, 13, 0)
        grid.addWidget(buttonBoxOk, 13, 1)
        
        self.setLayout(grid)
        
        self.connect(button1, SIGNAL("clicked()"), self.clicked1)
        self.connect(button2, SIGNAL("clicked()"), self.clicked2)
        self.connect(button3, SIGNAL("clicked()"), self.clicked3)
        self.connect(button4, SIGNAL("clicked()"), self.clicked4)
        self.connect(button5, SIGNAL("clicked()"), self.clicked5)
        buttonBoxOk.accepted.connect(self.accept)
        buttonBoxCanc.rejected.connect(self.reject)

        self.setWindowTitle("Clean Data By Dictionaries")
        
    def setChooser(self):
		Adialog = chooser(self)
		Adialog.labRawUse1.setText("What is the version propre of: "+str(self.valore)+"? choose between..")
		Adialog.useComboBox.addItems(self.lista)
		result = Adialog.exec_()
		if result == 0:
			self.exVal = str(Adialog.useComboBox.currentText())
			self.nwVal = str(Adialog.useLineEdit.text())
			if self.exVal:
				self.ans = self.exVal
			else:
				self.ans = self.nwVal
		return self.ans
  
    def clicked1(self):      
        nomeFile=QFileDialog.getOpenFileNames(self,"Open Raw Data File")
        self.label1.setText(nomeFile.takeFirst())
        self.lineedit1.clear()
        doc = QTextDocument()
        doc.setHtml(self.label1.text())
        text = doc.toPlainText()
        self.lineedit1.insert( text )
        self.label1.setText("<font color=grey size=2>Select the raw data file</font>")
        self.dirty = text
    
    def clicked2(self):      
        nomeFile=QFileDialog.getOpenFileNames(self,"Open Type Dictionary File")
        self.label2.setText(nomeFile.takeFirst())
        self.lineedit2.clear()
        doc = QTextDocument()
        doc.setHtml(self.label2.text())
        text = doc.toPlainText()
        self.lineedit2.insert( text )
        self.label2.setText("<font color=grey size=2>Select the boat type dictionary file</font>")
        self.inDictType = text
                  
    def clicked3(self):      
        nomeFile=QFileDialog.getOpenFileNames(self,"Open Route Dictionary File")
        self.label3.setText(nomeFile.takeFirst())
        self.lineedit3.clear()
        doc = QTextDocument()
        doc.setHtml(self.label3.text())
        text = doc.toPlainText()
        self.lineedit3.insert( text )
        self.label3.setText("<font color=grey size=2>Select the boat routes dictionary file</font>")
        self.inDictRoute = text
   
    def clicked4(self):      
        nomeFile=QFileDialog.getOpenFileNames(self,"Open Usage Dictionary File")
        self.label4.setText(nomeFile.takeFirst())
        self.lineedit4.clear()
        doc = QTextDocument()
        doc.setHtml(self.label4.text())
        text = doc.toPlainText()
        self.lineedit4.insert( text )
        self.label4.setText("<font color=grey size=2>Select the boat usage dictionary file</font>")
        self.inDictUse = text
   
    def clicked5(self):      
        nomeFile=QFileDialog.getSaveFileName(self,"Save Output File")
        self.label5.setText(nomeFile)
        self.lineedit5.clear()
        doc = QTextDocument()
        doc.setHtml(self.label5.text())
        text = doc.toPlainText()
        self.lineedit5.insert( text )
        self.label5.setText("<font color=grey size=2>Select the clean file</font>")
        self.outfile = text
        
    def accept(self):
#		try:
			if self.dirty and self.inDictType and self.inDictRoute and self.inDictUse and self.outfile:
				print "Processing begins here"
				p=open(self.dirty,'r')
				r=p.readlines()
				semaf=[]
				for i in r:
					semaf.append(i.split(";"))
				semaf=semaf[2:]
				t=[]
				mname=['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Août','Septembre','Octobre','Novembre','Décembre']
				routesem=[]
				nom=[]
				typeraw=[]
				nr=[]
				mois=[]
				date=[]
				heure=[]
				matr=[]
				for i in semaf:
					routesem.append(re.split("> |- |vers |VERS |Vers |>",i[5]))
					nr=int(i[0].split('/')[1])
					mois.append(mname[nr-1])
					date.append(i[0])
					heure.append(i[1])
					nom.append(i[2])
					matr.append(i[3])
					typeraw.append(i[4])
				an=date[0].split('/')[2]
				routesema=[]
				t=[]
				for i in routesem:
					for g in i:
						r=((((((((g.replace("-","")).strip()).upper()).replace("AVANT","AV")).replace("SMA","ST MATHIEU")).replace("CQT","CONQUET")).replace("BTH","BERTHAUME")).replace("DZ","DOUARNENEZ")).replace("AVGOULET","AV GOULET")
						t.append(r)
					routesema.append(filter(None,t))
					t=[]
				#imports dictionaries-----------------------------------------------------------------------------------------------------------------
				#typesdict
				typesdict={}
				a=open(self.inDictType,'r')
				b=a.readlines()
				for i in b:
					key,val=i.split('¡')
					value=list(val.split('¿'))
					typesdict[key]=value
				a.close()	
				for i in typesdict.keys():
					ab=typesdict[i][-1];
					typesdict[i][-1]=ab.split('\n')[0]
				#routesdict
				routesdict={}
				c=open(self.inDictRoute,'r')
				d=c.readlines()
				d2=[]
				value=[]
				for i in d:
					d2.append(i.split('\n')[0])
				for i in d2:
					key,val=i.split('¡')
					routesdict[key]=list(val.split(';'))
					value=[]
				c.close()
				#usesdict
				usesdict={}
				e=open(self.inDictUse,'r')
				f=e.readlines()
				for i in f:
					key,val=i.split('¡')
					value=list(val.split('¿'))
					usesdict[key]=value
				e.close()	
				for i in usesdict.keys():
					ab=usesdict[i][-1];
					usesdict[i][-1]=ab.split('\n')[0]
				#create final lists from dictionary occurrences, enlarge dictionaries if necesary-----------------------------------------------------
				#typeslist
				finaltypes2=[]
				finaltypes={}
				n=0
				for i in typeraw:
					for simp,raw in typesdict.iteritems():
						if i in raw:
							t=simp
					finaltypes[n]=t
					n=n+1
				finaltypes2=finaltypes.values()
				#useslist
				oui=99999999
				n=0
				finalusages={}
				finalusages2=[]
				t=[]
				sdictk=usesdict.keys()
				sdictk.sort()
				s=0
				for i in nom:
					for simp,raw in usesdict.iteritems():
						if i in raw:
							oui=n
							finalusages[n]=simp
						elif i.replace(' ','') in raw:
							oui=n
							finalusages[n]=simp
					if oui==n:
						n=n+1
					else:
						#qui va aperto il dialog------------------------------
						self.valore = i
						self.lista = sdictk
						answer = self.setChooser()
#						print "What is the usage propre of "+str(i)+"? chose between: "
#						answer=raw_input('\n or '.join(self.sdictk)+" or, otherwise, type down the new key for the dictionary: ")
#						if answer=='':
#							print "Warning! you have assigned 'None' usage to the boat, type once again the usage choosing between: "
#							answer=raw_input('\n or '.join(self.sdictk)+" or, otherwise, type down the new key for the dictionary: ")
						if answer not in usesdict.keys():
							t.append(i)
							usesdict[answer]=t
							usesdict.update()
							t=[]
						else:						
							usesdict[answer].append(i)
							usesdict.update()
							finalusages[n]=answer
						n=n+1
						s=s+1
				finalusages2=finalusages.values()
				#routeslist
				oui=99999999
				n=0
				finalroutes={}
				for i in routesema:
					routecode=routesdict.keys()
					routecode.sort()
					for simp,raw in routesdict.iteritems():
						if i in raw:
							oui=n
							finalroutes[n]=simp
					if oui==n:
						n=n+1
					else:
						self.valore = i
						self.lista = routecode						
						answer = self.setChooser()
#						print "What is the route propre of "+str(i)+"? chose between: "
#						answer=raw_input('\n or '.join("%-40s %s"%(routecode[i],routecode[i+len(routecode)/2]) for i in range(len(routecode)/2))+" or, otherwise, write down the new route: ")
					#	answer=raw_input('\n or '.join(routecode)+" or, otherwise, write down the new route: ")
						if answer in routecode:
							routesdict[answer].append(i)
							routesdict.update()
							finalroutes[n]=answer
							n=n+1
						else:
							t=[]
							t.append(i)
							routesdict[answer]=t
							routesdict.update()
							finalroutes[n]=answer
							n=n+1
				finalroutes2=finalroutes.values()
				#update dictionary files------------------------------------------------------------------------------------------------------------
				#typesdict
				typesfile=open(self.inDictType,'w')
				for key, value in typesdict.iteritems():
					typesfile.writelines(key+"¡")
					typesfile.writelines('¿'.join([str(item) for item in value]))
					typesfile.writelines("\n")
				typesfile.close()
				#routesdict
				routesfile=open(self.inDictRoute,'w')
				for key, value in routesdict.iteritems():
					routesfile.writelines(key+"¡")
					routesfile.writelines(';'.join([str(item) for item in value]))
					routesfile.writelines("\n")
				routesfile.close()
				#usesdict
				usesfile=open(self.inDictUse,'w')
				for key, value in usesdict.iteritems():
					usesfile.writelines(key+"¡")
					usesfile.writelines('¿'.join([str(item) for item in value]))
					usesfile.writelines("\n")
				usesfile.close()
				print "Dictionaries updated and printed in text files"

				#write down the xcel file
				workbook = xlwt.Workbook('utf-8')
				sheet = workbook.add_sheet('Feuil1')
				listone=[]
				a=len(mois)
				#print lenght lists for debug
				for i in range(0,a):
					listone.append([mois[i],date[i],heure[i],nom[i],matr[i],finalusages2[i],finaltypes2[i],finalroutes2[i]])
				for i in range(0,a+2):
					if i==0:
						style = xlwt.easyxf('font: bold 1, color red;')
						sheet.write(0,0,"PECHE PLAISANCE AN "+an,style)
					elif i==1:
						style = xlwt.easyxf('font: bold 1, color blue;')
						sheet.write(1,0,"MOIS",style)
						sheet.write(1,1,"DATE",style)
						sheet.write(1,2,"HEURE",style)
						sheet.write(1,3,"NOM",style)
						sheet.write(1,4,"MATRICULE",style)
						sheet.write(1,5,"USAGE",style)
						sheet.write(1,6,"TYPO",style)
						sheet.write(1,7,"ROUTE",style)
					else:
						for index,value in enumerate(listone[i-2]):
							value=[value]
							sheet.write(i,index,value)
				workbook.save(self.outfile)
				QMessageBox.warning(self,"Warning", "Elaboration finished, clean xcel file created", unicode())
				sys.exit()
#		except AttributeError:
#			QMessageBox.warning(self,"Warning", "Please fill all the requested fields before starting processing", unicode())
    
    def __repr__(self):
		return repr([self.dirty,self.inDictType,self.inDictRoute,self.inDictUse,self.outfile])
 
class chooser(QDialog):
	def __init__(self,parent=Form):
		super(chooser,self).__init__(parent)

#		self.labRawUse1 = QLabel("What is the version propre of: "+str(self.valore)+"? choose between..")
		self.labRawUse1 = QLabel()
		labRawUse2 = QLabel("or, alternatively, type down the new record")
		self.useComboBox = QComboBox()
#		self.useComboBox.addItems(self.lista)
		self.useLineEdit = QLineEdit("Type new record here, if needed")
		okButton = QPushButton("Cancel")	#& é un acceleratore: OK puo' essere premuto con Alt+O senza bisogno di andarci col mouse o col Tab
		cancelButton = QPushButton("&OK")
		
		self.setWindowTitle("Choose right value")
		
		buttonLayout = QHBoxLayout()
		buttonLayout.addStretch()
		buttonLayout.addWidget(okButton)
		buttonLayout.addWidget(cancelButton)
		
		layout = QGridLayout()
		layout.addWidget(self.labRawUse1, 0, 0)
		layout.addWidget(self.useComboBox, 1, 0)
		layout.addWidget(labRawUse2, 2, 0)
		layout.addWidget(self.useLineEdit, 3, 0, 3, 1)
		layout.addLayout(buttonLayout,4, 0, 1, 3)
		
		self.setLayout(layout)
		
		self.connect(okButton, SIGNAL("clicked()"), self, SLOT("accept()"))
		self.connect(cancelButton, SIGNAL("clicked()"), self, SLOT("reject()"))
		
#		self.connect(self.useComboBox,SIGNAL("currentIndexChanged(int)"), self.recordExValue)
#		self.connect(self.useLineEdit,SIGNAL('returnPressed()'),self.recordNwValue)
		
#	def recordExValue(self):
#		self.exVal = unicode(self.useComboBox.currentText())
#		return exVal
	
#	def recordNwValue(self):
#		self.nwVal = unicode(self.useLineEdit.text())
#		return nwVal
        
def main():
	app = QApplication(sys.argv)
	form = Form()
	form.show()
	return app.exec_()

if __name__ == '__main__':
    main()
