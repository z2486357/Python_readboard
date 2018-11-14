import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication,QDialog,QFileDialog,QMessageBox
from PyQt5.uic import loadUi
from PIL import Image
import numpy as np
import xlsxwriter
import matplotlib.pyplot


"""open userinterface"""
class userinterface (QDialog):
    def __init__(self):
        super(userinterface,self).__init__()
        loadUi('userinterface.ui',self)
        self.setWindowTitle('userinterface GUI')

    @pyqtSlot()
    def on_pngfile_clicked(self):
        global pngfileName
        pngfileName, _ = QFileDialog.getOpenFileName(self,"Open File","",".png Files (*.png);;All Files (*)", options=QFileDialog.Options())
        self.pnglabel.setText(str(pngfileName))
        self.xlsxlabel.setText(""+str(pngfileName[:-4])+".xlsx")
    
    @pyqtSlot()
    def on_txtfile_clicked(self):
        txtfileName, _ = QFileDialog.getOpenFileName(self,"Open File","",".txt Files (*.txt);;All Files (*)", options=QFileDialog.Options())
        self.txtlabel.setText(""+txtfileName)
        
    @pyqtSlot()
    def on_GO_clicked(self):
        try:
            if (self.pnglabel.text()==self.unvisible.text() or self.txtlabel.text()==self.unvisible.text()):
                QMessageBox.information(self,' ',"go to choose file")
            else:       
                I = Image.open(self.pnglabel.text()) 
                global I_array
                I_array= np.array(I)
                global record
                record=[]
                for i in range(0,100):
                    record.append([])
                recordnum=0
                def findaround(i,j,recordnum):
                    global record
                    global I_array
                    record[recordnum].append([i,j])
                    I_array[i][j][0]=0
                    I_array[i][j][1]=0
                    I_array[i][j][2]=0
                    if I_array[i][j+1][0]>128 and I_array[i][j+1][1]>128 and I_array[i][j+1][2]>128:
                        findaround(i,j+1,recordnum)
                    if I_array[i][j-1][0]>128 and I_array[i][j-1][1]>128 and I_array[i][j-1][2]>128:
                        findaround(i,j-1,recordnum)
                    if I_array[i+1][j][0]>128 and I_array[i+1][j][1]>128 and I_array[i+1][j][2]>128:
                        findaround(i+1,j,recordnum)
                        
                for i in range(0,len(I_array)):
                    for j in range(0,len(I_array[0])):
                        if I_array[i][j][0]>128 and I_array[i][j][1]>128 and I_array[i][j][2]>128:
                            findaround(i,j,recordnum)
                            recordnum+=1
                
                center=[]
                for i in range(0,len(record)):
                    totali=0
                    totalj=0
                    for j in range(0,len(record[i])):
                        totali+=record[i][j][0]
                        totalj+=record[i][j][1]
                    totali=int(totali/len(record[i]))
                    totalj=int(totalj/len(record[i]))
                    center.append([totali,totalj])
                
                """output wuth the mark on center"""
                I_array= np.array(I)
                for i in range(0,len(center)):
                    I_array[center[i][0]][center[i][1]][0]=0
                    I_array[center[i][0]][center[i][1]][1]=0
                    I_array[center[i][0]][center[i][1]][2]=0
                I_array=I_array[:,:,0:3]
                global pngfileName
                matplotlib.image.imsave(pngfileName[:-4]+"_withpoint.png", I_array)
                

                fh = open( self.txtlabel.text(),"r",encoding="utf-8-sig" );
                content=[]
                output=[]
                for line in fh.readlines():
                    y = [value for value in line.split()]
                    content.append( y )
                fh.close()
                output=[]
                
                def canbetransfertofloat(input):
                    try:
                        float(input)
                        return True
                    except:
                        return False
                    
                for i in range(0,len(center)):
                    for j in range(0,len(content)):
                        if center[i][0]==int(content[j][0]) and center[i][1]==int(content[j][1]):
                            if (canbetransfertofloat(content[j][2])):
                                output.append([content[j][0],content[j][1],"-->",content[j][0],content[j][1],content[j][2],content[j][3],content[j][4]])
                            else:
                                plus=j
                                minus=j
                                while(canbetransfertofloat(content[plus][2])==False and plus<len(content)-1):
                                    plus+=1
                                while(canbetransfertofloat(content[minus][2])==False and minus>0):
                                    minus-=1
                                up=0
                                while(canbetransfertofloat(content[j-1920*up][2])==False and j-1920*up>1920):
                                    up+=1
                                down=0
                                while(canbetransfertofloat(content[j+1920*down][2])==False and j+1920*down<len(content)-1):
                                    down+=1
                                if plus-j>j-minus:
                                    plus=0
                                else:
                                    minus=0
                                if up>abs(j-plus+minus) or down>abs(plus+minus):
                                    if up<down:
                                        output.append([content[j][0],content[j][1],"-->",content[j-1920*up][0],content[j-1920*up][1],
                                                  content[j-1920*up][2],content[j-1920*up][3],content[j-1920*up][4]])
                                    else:
                                        output.append([content[j][0],content[j][1],"-->",content[j+1920*down][0],content[j+1920*down][1],
                                                  content[j+1920*down][2],content[j+1920*down][3],content[j+1920*down][4]])                                        
                                else:
                                    output.append([content[j][0],content[j][1],"-->",content[plus+minus][0],content[plus+minus][1],
                                                  content[plus+minus][2],content[plus+minus][3],content[plus+minus][4]])
                
                
                workbook = xlsxwriter.Workbook(self.xlsxlabel.text())
                worksheet = workbook.add_worksheet()
                for i in range(0,len(output)):
                    worksheet.write_row(i,0,output[i])
                workbook.close()
                QMessageBox.information(self,' ',"Finish")
        except:
            QMessageBox.information(self,' ',"Something wrong. Close and try again")
            
                
app=QApplication(sys.argv)
widget=userinterface()
widget.show()
sys.exit(app.exec_())
    




