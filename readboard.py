from PIL import Image
import numpy as np
import xlsxwriter
I = Image.open('test.png') 
"""I.show()"""  
"""I.save('./save.png')"""
global I_array
I_array= np.array(I)
"""print (I_array[519][663])"""
"""print(len(I_array))
print(len(I_array[0]))"""
total=0
global record
record=[]
for i in range(0,100):
    record.append([])
recordnum=0
lastlinedot=False
havedot=False
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
"""
output wuth the mark on center
I_array= np.array(I)
for i in range(0,len(center)):
    I_array[center[i][0]][center[i][1]][0]=0
    I_array[center[i][0]][center[i][1]][1]=0
    I_array[center[i][0]][center[i][1]][2]=0
I_array=I_array[:,:,0:3]
matplotlib.image.imsave('xxx.png', I_array)
"""
fh = open( "test.txt","r",encoding="utf-8-sig" );
content=[]
output=[]
for line in fh.readlines():
    y = [value for value in line.split()]
    content.append( y )
fh.close()
output=[]

for i in range(0,len(center)):
    for j in range(0,len(content)):
        if center[i][0]==int(content[j][0]) and center[i][1]==int(content[j][1]):
            output.append([content[j][0],content[j][1],content[j][2],content[j][3],content[j][4]])


workbook = xlsxwriter.Workbook('test.xlsx')
worksheet = workbook.add_worksheet()
for i in range(0,len(output)):
    worksheet.write_row(i,0,output[i])
workbook.close()
