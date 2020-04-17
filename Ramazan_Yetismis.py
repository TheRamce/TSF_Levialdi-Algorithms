import csv
from random import randint
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from PIL import Image
import numpy as np
import tkinter as tk
from tkinter.filedialog import *
from PIL import Image, ImageTk
'''NCC is for Levialdi's connected components.NCC_TSH is for TSF connected components.flag is for Leviald's termination condition.
Flag2 is for TSF termination condition'''
NCC= 0;NCC_TSF = 0;flag = 0 ;Flag2=True


#image operations
openedImage=None;binaryImage=None;binaryImage3=None;framedImage=None;img1=None
pixelMapAsString="";Number_Lev="";name="created_object"
number_of_iterations=0#iteration for LEvialdi
number_of_iterations1=0#iteration for TSF
#Functions asks user to choose İmage and then converts it to binary form and shows on The GUİ
def openImage():
    openFileFormats = (("all files", "*.*"), ("png files", "*.png"))  # File formats for easy search
    path = askopenfilename(parent=root, filetypes=openFileFormats)  # Basic file pick gui
    fp = open(path, "rb")  # Read file as a byte map
    global openedImage, binaryImage, framedImage,binaryImage2,name
    st = fp.name.split('/')
    name = st[len(st) - 1]

   #converting Image to binary
    openedImage = Image.open(fp)
    grayArray = PIL2np(openedImage)
    grayframedarr = frame(grayArray)
    framedImage = np2PIL(grayframedarr)
    binaryArray = gray2Bin(grayArray)
    binaryImage = frame(binaryArray)#For levialdi
    binaryImage2=frame(binaryArray)#for TSF

    global img1#takes the parameter img1

#adds image to the GUI
    defImg = ImageTk.PhotoImage(openedImage)
    img1.config(image=defImg)
    img1.image = defImg
    img1.update()
    global binaryImage3,binaryCanvas3 #this canvas
    binarr=pixel(binaryImage)#writes the binary formed image
    binaryCanvas3.create_text(0, 0, text=binarr,font=("Ariel", 3, "bold"), tag="lvTag1", anchor=NW)
    binaryCanvas3.update()
    NCC_lev()#writes the number of connected component for levialdi
    TSF_NCC()#writes the number of connected component for TSF
    writeLev(binaryImage)#writes the img as binary form at each iterations
    writeTSH(binaryImage)#writes the img as binary form at each iterations
#add frames '0's' to the given arry
def frame(arr):
    nrows=len(arr[0])
    ncols=len(arr[1])
    temp = np.zeros(shape=(nrows+2, ncols+2))
    for i in range(0, nrows):

        for j in range(0, ncols):
            temp[i + 1][j + 1] = arr[i][j]

    return temp
#takes arr and returns img
def np2PIL(im):
    print("size of arr: ",im.shape)
    img = Image.fromarray(np.uint8(im))
    return img
#takes img and returns np_Array
def PIL2np(img):
    global nrows
    global ncols
    nrows = img.size[0]
    ncols = img.size[1]
    print("nrows, ncols : ", nrows,ncols)
    imgarray = np.array(img.convert("1"))
    return imgarray
def gray2Bin(newarr):
    nrows = len(newarr[0])
    ncols = len(newarr[1])
    array=np.zeros(shape=(nrows, ncols))
    for i in range(nrows):
        for j in range(ncols):
            if newarr[i][j]==True:
                array[i][j] = 1
            else:
                array[i][j] = 0
    return array
#The levialdi algorithms 1 iteration
def iterForLevialdi (arr):
    global NCC#number of connected components
    global flag#flag for change
    nrows = len(arr[0])#lenght of nrows and ncols
    ncols = len(arr[1])
    counter = 0
    temp=arr.__copy__()
    #this loops helps me to scan the array from upper right part to lower left
    for i in range(1,nrows - 1):
        for j in range(ncols - 2,0,-1):
            if arr[i][j]==0:#augmented condition
                counter = counter + 1
                if (counter == (nrows - 2)*(ncols - 2)):
                    flag = 1
                if (arr[i+1][j]==1 and arr[i][j-1]==1):
                    temp[i][j] = 1
            else:#deletion conditions
                if arr[i][j+1]==0 and arr[i][j-1]==0 and arr[i+1][j]==0 and arr[i-1][j]==0 and arr[i+1][j+1]==0 and arr[i+1][j-1]==0 and arr[i-1][j+1]==0 and arr[i-1][j-1]==0:
                    NCC = NCC + 1
                    temp[i][j] = 0
                elif arr[i+1][j]==0 and arr[i][j-1]==0 and arr[i+1][j-1]==0:
                    temp[i][j]=0
    return temp
#by the help of the pass by referance I don need to use temp array.This fucntion counts the number of iteraiton
def Levialdi():
    global binaryImage,NCC,number_of_iterations
    arr=binaryImage#binary iamge which we opned

    while(True):
        arr = iterForLevialdi(arr)
        writeLev(arr)#writes the GUI the updated arr
        NCC_lev()#writes the gui the updated NCC adn iteraitons
        if flag == 1:#termination condition is ensure
            break
        number_of_iterations = number_of_iterations + 1

    print("__FOR-LEV__iteration =",number_of_iterations,"NCC =",NCC)

    return number_of_iterations
#finds the number ones which are 8 connected
def Bp(arr,i,j):
    counter=0
    if arr[i][j+1]==1:
        counter=counter+1
    if arr[i][j-1]==1:
        counter = counter + 1
    if arr[i+1][j] == 1:
        counter = counter + 1
    if arr[i+1][j +1] == 1:
        counter = counter + 1

    if arr[i+1][j -1] == 1:
        counter = counter + 1
    if arr[i-1][j] == 1:
        counter = counter + 1
    if arr[i-1][j +1] == 1:
        counter = counter + 1
    if arr[i-1][j -1] == 1:
        counter = counter + 1
    return counter
#finds the 8 connected componenents aorund the specified index
def Cp(arr,i,j):
    counter=0
    ones=0
    # defines 8 lenght array and add the neigbors to the array
    temp = np.array([0, 0, 0, 0, 0, 0, 0, 0])
    temp[0] = arr[i][j - 1]
    temp[1] = arr[i - 1][j-1]
    temp[2] = arr[i - 1][j ]
    temp[3] = arr[i-1][j + 1]
    temp[4] = arr[i][j + 1]
    temp[5] = arr[i +1][j+1]
    temp[6] = arr[i + 1][j ]
    temp[7] = arr[i+1][j - 1]
    #if there is Connceted components it replaces the correct zeros with 1
    for i in range(0,7,2):
        if temp[i]==1 and temp[(i+2)%8]==1:
            temp[i+1]=1

    for i in range(0, 8):#This part is almost same with Tp()
        if temp[i] == 0 and temp[(i + 1) % 8] == 1:

            counter = counter + 1
        if temp[i] == 1:
            ones = ones + 1
    if ones==8:#if all of them are 1 that means the CP() is 1
        return 1
    else:
        return counter
#finds the 0 to 1 transition
def Tp(arr,i,j):
    counter=0
    # defines 8 lenght array and add the neigbors to the array
    temp=np.array([0,0,0,0,0,0,0,0])
    temp[0]=arr[i-1][j-1]
    temp[1]=arr[i-1][j]
    temp[2]=arr[i-1][j+1]
    temp[3]=arr[i][j+1]
    temp[4]=arr[i + 1][j + 1]
    temp[5]=arr[i+1][j]
    temp[6]=arr[i+1][j-1]
    temp[7]=arr[i][j-1]
    #searches if there is any 0 1 transititon
    for i in range(0,8):
        if temp[i]==0 and temp[(i+1)%8]==1:
            counter=counter+1


    return counter
#finds the 3 or grater lenght zeros which are 4 connected
def Zp(arr,i,j):
    counter = 0
    temp = np.array([0, 0, 0, 0, 0, 0, 0, 0])
    #defines 8 lenght array and add the neigbors to the array
    temp[0] = arr[i - 1][j - 1]
    temp[1] = arr[i - 1][j]
    temp[2] = arr[i - 1][j + 1]
    temp[3] = arr[i][j + 1]
    temp[4] = arr[i + 1][j + 1]
    temp[5] = arr[i + 1][j]
    temp[6] = arr[i + 1][j - 1]
    temp[7] = arr[i][j - 1]
    for i in range(0,8):#searches if there is 3 or more zeros
        if temp[i]==0 and temp[(i+1)%8]==0 and temp[(i+2)%8]==0:
            counter=counter+1
    return counter
#Just one iteraiton for TSF
def iterForTSF(arr):
    global NCC_TSF#connected components
    global Flag2#termination flag
    nrows = len(arr[0])
    ncols = len(arr[1])
    counter=0
    # THE 1. SUBFİELD
    #if i is odd j is 1 else j is 2 we devide the array by yhe help of this algorithm
    for i in range(1, nrows-1):
        j = 2
        if i % 2 == 1:
            j = 1
        while j < ncols-1:

            cp=Cp(arr,i,j)#calls the Cp()

            if arr[i][j]==0:#if index is 0 then
                counter+=1#looks if there is any change

                if (cp==1) and ((arr[i][j-1]==1 and arr[i-1][j]==1) or(arr[i][j-1]==1 and arr[i+1][j]==1)):#this is the deletion condition
                    arr[i][j]=1

            else:#this part we look for the aougmented condition because index is 1
                bp=Bp(arr,i,j)#calls for bp()
                zp=Zp(arr,i,j)#calls the Zp()


                if bp==0:#means isolated point
                    NCC_TSF+=1
                    arr[i][j]=0
                if bp==1 :#this is  nested if statement

                    if cp==1 and zp>0 and(arr[i-1][j-1]==0 and arr[i+1][j-1]==0 ):#if bp is 1 then these 3 have to be TRUE
                        arr[i][j] = 0
                else:#if it is different tham 1 then these 2 have to be TRUE
                    if cp == 1 and zp > 0:
                        arr[i][j] = 0

            j = j + 2#increment J with 2
    #THE 2. SUBFİELD
    for i in range(1, nrows-1):

        j = 1
        if i % 2 == 1:
            j = 2
        while j < ncols-1:
            cp = Cp(arr, i, j)

            if arr[i][j] == 0:
                counter+=1
                if (counter == (nrows - 2) * (ncols - 2)):
                    Flag2=False
               # print('for index2=0')
               # print('i=',i,'j=',j,'cp=',cp)
                if (cp == 1) and ((arr[i][j - 1] == 1 and arr[i - 1][j] == 1) or (arr[i][j - 1] == 1 and arr[i + 1][j] == 1)):
                    arr[i][j] = 1
                    #print('index2=1')
            else:
               # print('for index2=1')
                bp = Bp(arr, i, j)
                zp = Zp(arr, i, j)
               #print('bp', bp, 'zp', zp, 'cp', cp)
                if bp == 0:
                    NCC_TSF+=1
                    arr[i][j] = 0
                if bp==1 :
                    if cp==1 and zp>0 and(arr[i-1][j-1]==0 and arr[i+1][j-1]==0 ):
                        arr[i][j] = 0

                else:
                    if cp == 1 and zp > 0:
                        arr[i][j] = 0


            j = j + 2
    return arr
#counts the iteration for TSF
def TSH():
    global Flag2,number_of_iterations1
    global NCC_TSF

    global  binaryImage2
    arr=binaryImage2
    while True:
        arr=iterForTSF(arr)
        TSF_NCC()
        writeTSH(arr)

        if Flag2==False:
            break
        number_of_iterations1 += 1
        print('__FOR-TSH__iteration =', number_of_iterations1,' NCC =', NCC_TSF)
def save():
    global name, NCC, NCC_TSF, number_of_iterations, number_of_iterations1,binaryImage#Takes the gloabl variables
    row=len(binaryImage);col=len(binaryImage[1])
    size=str(row*col)#finds the size of the file

    saveFileFormats = (("csv files", "*.csv"), ("all files", "*.*"))#ask user to take the path
    output = asksaveasfile(filetypes=saveFileFormats, title='Export File',
                           defaultextension='.csv')
    with open(output.name, "w") as csv_file:#opens the csv file and adds the file name
        fieldnames = ['Algorithm', 'File Name', 'Iteration', 'NCC', 'Size']#opnes array
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        #writes the first and second rows
        writer.writerow({'Algorithm': 'Levialdi', 'File Name': name, 'Iteration':str(number_of_iterations) , 'NCC': str(NCC), 'Size': size})
        writer.writerow({'Algorithm': 'TSF', 'File Name': name, 'Iteration': str(number_of_iterations1), 'NCC': str(NCC_TSF), 'Size': size})




root = tk.Tk()
xSize,ySize = 1600,1000
size = str(xSize)+"x"+str(ySize)
root.geometry(size)
root.title("Programing Studio")
root.configure(bg='white')

#designs the label
Label(root, bg='white', text="test").grid(row=1, column=0, padx=xSize/6.7, pady=ySize/5.3)
Label(root, bg='white', text="test").grid(row=1, column=1, padx=xSize/6.7, pady=ySize/5.3)
Label(root, bg='white', text="test").grid(row=1, column=2, padx=xSize/6.7, pady=ySize/5.3)
Label(root, bg='white', text="test").grid(row=2, column=0, padx=xSize/6.7, pady=ySize/5.3)
Label(root, bg='white', text="test").grid(row=2, column=1, padx=xSize/6.7, pady=ySize/5.3)
Label(root, bg='white', text="test").grid(row=2, column=2, padx=xSize/6.7, pady=ySize/5.3)



#converst binary array to pixel string
def pixel(imgArr):
    pixelAsString=""
    nRow=len(imgArr[0])
    nCol=len(imgArr[1])
    for r in range(nRow):
        for c in range(nCol):
            pixelAsString +=str(imgArr[r][c])
        pixelAsString += "\n"


    return pixelAsString
#writs TSF_NCC to the screen
def TSF_NCC():
    global NCC_TSF,textC1,number_of_iterations1
    fontSize = 20
    tsf_Ncc='NCC='+str(NCC_TSF)
    it=str(number_of_iterations1)
    textC1.select_clear()
    textC1.delete("lvTag1")
    textC1.create_text(50,50, text='TSF ALGORITHM\n'+tsf_Ncc+'\nITERATIONS='+it, font=("Ariel", fontSize, "bold"), tag="lvTag1", anchor=NW)
    textC1.update()
#writs Levialdi_NCC to the screen
def NCC_lev():
    global NCC,textC,number_of_iterations
    fontSize = 20
    tsf_Ncc='NCC='+str(NCC)
    it=str(number_of_iterations)
    textC.select_clear()
    textC.delete("lvTag")
    textC.create_text(50,50, text='LEVIALDI ALGORITHM\n'+tsf_Ncc+'\nITERATIONS='+it, font=("Ariel", fontSize, "bold"), tag="lvTag", anchor=NW)
    textC.update()
#writes the bianry array to the screen after each iteration for levialdi
def writeLev(imgArr):
    global binaryCanvas
    global pixelMapAsString
    fontSize =3
    pixelMapAsString=pixel(imgArr)
    Number_Lev=str(NCC)
    binaryCanvas.select_clear()
    binaryCanvas.delete("lvTag")
    binaryCanvas.create_text(0, -20, text=pixelMapAsString, font=("Ariel", fontSize, "bold"), tag="lvTag", anchor=NW)
    binaryCanvas.update()
#writes the bianry array to the screen after each iteration for tsf
def writeTSH(imgArr):
    global binaryCanvas2
    global pixelMapAsString
    fontSize = 3
    pixelMapAsString=pixel(imgArr)
    binaryCanvas2.select_clear()
    binaryCanvas2.delete("lvTag")
    binaryCanvas2.create_text(0, -20, text=pixelMapAsString, font=("Ariel", fontSize, "bold"), tag="lvTag", anchor=NW)
    # anchor North West is used to position the image to top left corner
    # 0,0 gives relative position to anchor

    # for remove text from canvas use tag
    #binaryCanvas.select_clear()
    #binaryCanvas.delete("lvTag")

    #for update you can remove and write text for every iteration
    binaryCanvas2.update()
# writes the bianry array to the screen after each iteration
def binary_image(nrow,ncol,Value):
    x, y = np.indices((nrow, ncol))
    mask_lines = np.zeros(shape=(nrow,ncol))
    a=randint(0,nrow-10)
    b=randint(0,ncol-10)
    c= randint(0,nrow-10)
    d = randint(0,ncol-10)
    x0, y0, r0 = a, b, 10
    x1, y1, r1 = c, d, 10
    x2, y2, r2 = c, d, 10

    for i in range(50, 80):
        mask_lines[i][i + 1] = 1
        mask_lines[i][i + 2] = 1
        mask_lines[i][i + 10] = 1
        mask_lines[i][i + 20] = 1

    mask_circle1 = np.abs((x - x0) ** 2 + (y - y0) ** 2 - r0 ** 2 ) <= 5
    mask_square1 = np.fmax(np.absolute( x - x1), np.absolute( y - y1)) <= r1
    mask_square2 = np.fmax(np.absolute( x - x2), np.absolute( y - y2)) <= r2

    #imge = np.logical_or ( np.logical_or(mask_lines, mask_circle1), mask_square1) * Value
    imge = np.logical_or(mask_lines, mask_square1) * Value

    return imge
#creates image
def createImage():
    global binaryImage, framedImage, binaryImage2,binaryImage3
    ONE = 150
    bim = binary_image(100,100,ONE)
    new_img = np2PIL(bim)
    array=PIL2np(new_img)
    framedarray=frame(array)
    binaryImage=gray2Bin(framedarray)
    binaryImage2=gray2Bin(framedarray)


    defImg = ImageTk.PhotoImage(new_img)
    img1.config(image=defImg)
    img1.image = defImg
    img1.update()

    binarr=pixel(binaryImage)
    binaryCanvas3.create_text(-20, 0, text=binarr,font=("Ariel", 3, "bold"), tag="lvTag1", anchor=NW)
    binaryCanvas3.update()
    NCC_lev()
    TSF_NCC()
    writeLev(binaryImage)
    writeTSH(binaryImage)

menubar = Menu(root)

# create a pulldown menu, and add it to the menu bar
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=openImage)
filemenu.add_command(label="Create",command=createImage)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

# create more pulldown menus
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Levialdi", command=Levialdi)
editmenu.add_command(label="TSF", command=TSH)
editmenu.add_command(label="Save", command=save)
menubar.add_cascade(label="Edit", menu=editmenu)

root.config(menu=menubar)




# You should use canvas to edit text in label
binaryCanvas = Canvas(root, borderwidth=2, bg="white", bd=3, relief="groove")
binaryCanvas.grid(row=1, column=1, sticky=W + E + N + S)
binaryCanvas2 = Canvas(root, borderwidth=2, bg="white", bd=3, relief="groove")
binaryCanvas2.grid(row=2, column=1, sticky=W + E + N + S)


binaryCanvas3 = Canvas(root, borderwidth=2, bg="white", bd=3, relief="groove")
binaryCanvas3.grid(row=2, column=0, sticky=W + E + N + S)

textC1 = Canvas(root, borderwidth=2, bg="white", bd=3, relief="groove")
textC1.grid(row=2, column=2, sticky=W + E + N + S)
textC = Canvas(root, borderwidth=2, bg="white", bd=3, relief="groove")
textC.grid(row=1, column=2, sticky=W + E + N + S)


img1 = Label(root, borderwidth=2, bg="white", fg="black", bd=3, relief="groove")
img1.grid(row=1, column=0, sticky=W + E + N + S)

root.mainloop()