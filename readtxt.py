fh = open( "test.txt","r",encoding="utf-8-sig" );
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

print(canbetransfertofloat(content[0][3]))