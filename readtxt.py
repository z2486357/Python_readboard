fh = open( "test.txt","r",encoding="utf-8-sig" );
content=[]
output=[]
for line in fh.readlines():
    y = [value for value in line.split()]
    content.append( y )
fh.close()
output=[]
print(int(content[0][0]))