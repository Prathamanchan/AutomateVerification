
procedure(MainForm()
  let(((xwidth 330) (ydelta 30) (prompt 126) TabField1
       PlaceButton RouteButton)

                                               

/*  TabField1   */  
  Reference=hiCreateFileSelectorField(
                       ?name 'Reference
                       ?mode 'directory
                       ?prompt "Choose Directory" )

 DefValue=list( "TIME" "INFO" "ERROR" "FINE" "WARNING" "NOTIME")               
 Suffix=hiCreateStringField( ?name 'Suffix ?prompt "Folder Suffix" ?defValue "")    
 SearchString=hiCreateStringField( ?name 'SearchString ?prompt "Search String" ?defValue "")                          
 addButton=hiCreateButton(?name 'addButton ?buttonText "Add" ?callback "addToList(hiGetCurrentForm())")  
 Delete=hiCreateButton(?name 'Delete ?buttonText "Delete" ?callback "DeletefromList(hiGetCurrentForm())") 
 ListBField = hiCreateListBoxField(?name    'ListBField
                                  ?prompt    "Key Words"
                                  ?choices  DefValue  
                                  ?numRows    3
                                  ?multipleSelect nil
                                  ?keepHistory t)
 
                                                  
 TabField1=list(
           list(Reference 10:1*ydelta xwidth+8:ydelta prompt)
           list(Suffix 10:2*ydelta xwidth-20:ydelta prompt)
           list(SearchString 10:3*ydelta xwidth-20:ydelta prompt)
           list(addButton 320:3*ydelta 80:ydelta prompt)
           list(Delete 320:4*ydelta 80:ydelta prompt)
           list(ListBField 10:4*(ydelta+3) xwidth-20:100 prompt)
           )                           
                            
     
  tabField=hiCreateTabField(
              ?name 'tabField
              ?notebookStyle nil
              ?pageScroller nil
              ?tabPlacement 'top
              ?tabs list("iNags")
              ?fields list(TabField1)
              ?value 1)

  
              
  hiCreateAppForm(
              ?name 'tabForm
              ?fields list(list(tabField 0:0 xwidth+80:8*ydelta+40 0))
              ?formTitle "Boring Stuff"
              ?buttonLayout 'OKCancel  
              ?callback    'MainTask
              ?initialSize list(xwidth+80 9*ydelta+20))
              
  hiDisplayForm(tabForm))
  )
 
 


       
procedure(MainTask(form)
     let((ElemfromList)
  DirectoryPath=tabForm->tabField->page1->Reference->value         
  DirectoryFilesnFolders=getDirFiles(DirectoryPath)
  MatchedFilesnFolders=pcreMatchList(tabForm->tabField->page1->Suffix->value  DirectoryFilesnFolders) 
  ListValues=tabForm->tabField->page1->ListBField->choices
  myPort = outfile(strcat(DirectoryPath "/runSimulation"))
 ; MatchedFolders=setof(match MatchedFilesnFolders fileLength(strcat(DirectoryPath "/" match))==4096)
 
  foreach(match MatchedFilesnFolders
      fullpath=strcat(DirectoryPath "/" match "/xrun.log")
      fpFile = infile(fullpath)
      fprintf(myPort "\n =+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+ %s =+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+ \n" fullpath)
      while(gets(line fpFile)
      foreach(key ListValues
      when(pcreMatchp(key line)  println(line)   
      fprintf(myPort "%s" line)
       )
       )
       )

         );foreach  
   edit(strcat(DirectoryPath "/runSimulation"))       
   close(myPort)           
)
)

procedure(addToList(form)
     let((ElemfromList)
  ElemfromList=tabForm->tabField->page1->SearchString->value  
  DefValue=cons(ElemfromList DefValue)
  tabForm->tabField->page1->ListBField->choices=DefValue
            
)
)

procedure(DeletefromList(form)
     let((ElemfromList)
  ElemfromList=tabForm->tabField->page1->ListBField->value
  DefValue=remove(car(ElemfromList) DefValue)
  tabForm->tabField->page1->ListBField->choices=DefValue                   
            
            
)
)



MainForm()
