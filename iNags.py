from Tkinter import *
import tkMessageBox
from tkFileDialog import *
from os import listdir
import os
from os.path import isfile,join
import glob

def browse_button():
   #Allow user to select a directory and store in a global var
   #Called folder_path

   global folder_path
   filename=askdirectory()
   folder_path.set(filename)           #filename has the path of the main directory
   listFileDir=listdir(filename)
   FolderPathEntry.delete(0, END)      #deletes the current value
   FolderPathEntry.insert(0, filename) #inserts new value assigned by 2nd parameter

def addtoList():
   global numLbox
   numLbox=numLbox+1
   SearchKeyEntryString = SearchKeyEntry.get()
   counts=Lbox.get(0,END).count(SearchKeyEntryString)
   if counts==0:
     Lbox.insert(numLbox, SearchKeyEntryString) 
   else:
     tkMessageBox.showinfo("Error", "Keyword already exists in the List !")

def deletefromList():
   global numLbox
   numLbox=numLbox-1
   value=str((Lbox.get(ACTIVE)))
   if value:
     idx = Lbox.get(0,END).index(value)
     Lbox.delete(idx)

def mainMethod():
    directoryPath=FolderPathEntry.get()
    outfile= open(directoryPath+"/outfile.txt","w+")
    folderSuffix=SuffixEntry.get()
    listTuple=Lbox.get(0,END)
    fileExtension=directoryPath+"/*"+folderSuffix
    listfiledirs=listdir(directoryPath)
    matchedFolders=glob.glob(fileExtension)
    for folder in matchedFolders:
        logFilePath=glob.glob(folder+"/xrun.log")[0]
        outfile.write("\n"+logFilePath+"\n")
        file = open(logFilePath, 'r') 
        for eachline in file: 
          for pattern in listTuple:
            patternRegex = re.compile(pattern) 
            matched = patternRegex.search(eachline) 
            if matched:
                 outfile.write(eachline) 
        outfile.write("\n--------------------------------------------------------------------------------------------------------\n") 
    outfile.write("\n--------------------------------------------------------------------------------------------------------\n") 
    outfile.close() 
    file.close() 
    os.system("gedit outfile.txt")











#######################################################GUI-CODE############################################################################

#MainCode::Begins

root=Tk()
folder_path=StringVar()
root.title("iNags")


mainframe=Frame(root,bd=5) 
mainframe.pack()

BrowseButton=Button(mainframe,text="Browse", width=5,command=browse_button,bg="white",font="Times 10 bold",bd=4)
BrowseButton.grid(row=0, column=2) 

FolderpathLabel=Label(mainframe,width=15, text='Main Folder',font="Times 10 bold")
FolderpathLabel.grid(row=0) 
SuffixLabel=Label(mainframe,width=15, text='Folder Suffix',font="Times 10 bold")
SuffixLabel.grid(row=1) 
SearchLabel=Label(mainframe,width=15, text='Search String',font="Times 10 bold")
SearchLabel.grid(row=2) 
SearchKeyWordsLabel=Label(mainframe,width=15, text='Search KeyWords',font="Times 10 bold")
SearchKeyWordsLabel.grid(row=3) 

FolderPathEntry = Entry(mainframe,width=40) 
FolderPathEntry.grid(row=0, column=1) 
SuffixEntry = Entry(mainframe,width=40) 
SuffixEntry.grid(row=1, column=1) 
SearchKeyEntry = Entry(mainframe,width=40) 
SearchKeyEntry.grid(row=2, column=1) 

addButton=Button(mainframe,text="Add", width=5,command=addtoList,bg="white",font="Times 10 bold",bd=4)
addButton.grid(row=2, column=2) 
deleteButton=Button(mainframe,text="Delete", width=5,command=deletefromList,bg="white",font="Times 10 bold",bd=4)
deleteButton.grid(row=3, column=2) 

numLbox=0  
Lbox = Listbox(mainframe,width=40,height=10) 
Lbox.grid(row=3, column=1) 


frame = Frame(mainframe,highlightcolor="white",bd=10) 
frame.grid(row=4, column=1)

ApplyButton=Button(frame,text="Apply", width=5,command=mainMethod,bg="PeachPuff",font="Times 10 bold",relief=GROOVE,bd=4)
ApplyButton.pack(side = LEFT) 
CancelButton=Button(frame,text="Cancel", width=5,command=root.destroy,bg="Moccasin",font="Times 10 bold",relief=GROOVE,bd=4)
CancelButton.pack(side = LEFT) 

root.mainloop() 

#MainCode::Ends








