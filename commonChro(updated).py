from openpyxl import load_workbook

#creating lists to store chromosomes and their location
def storeData(sheetName1, sheetName2, chromlist1 = [], chromlist2 = []):
    colName1 = {}
    colName2 = {}
    colNum = 0
    #displaying max no. of rows
    print(f"Total number of rows/entries in {path1}: {sheetName1.max_row}")
    print(f"Total number of rows/entries in {path2}: {sheetName2.max_row}")
    print("Processing...")
    
    for cols1 in sheetName1.iter_rows(min_row = 1, max_row = 1, min_col = 1, max_col = sheetName1.max_column, values_only = True):
        for i in range(sheetName1.max_column):
            if (cols1[i].lower() == "chromosome"):
                colName1[cols1[i].lower()] = colNum
            elif (cols1[i].lower() == "begin location"):
                colName2[cols1[i].lower()] = colNum
            
            colNum += 1
    
    #Adding chromosomes and locations from excel file in lists present above respectively
    for row1 in sheetName1.iter_rows(min_row = 2, min_col = colName1['chromosome'] + 1, max_col = colName2['begin location'] + 1, values_only = True):
        if (row1[0] != None and row1[colName2['begin location'] - colName1['chromosome']] != None):
            chromlist1.append([row1[0], int(str(row1[colName2['begin location'] - colName1['chromosome']]).split("_")[0])])
            #chromloc1.append()


    colName1.clear()
    colName2.clear()
    colNum = 0
    for cols2 in sheetName2.iter_rows(min_row = 1, max_row = 1, min_col = 1, max_col = sheetName2.max_column, values_only = True):
        for i in range(sheetName2.max_column):
            if (cols2[i].lower() == "chromosome"):
                colName1[cols2[i].lower()] = colNum
            elif (cols2[i].lower() == "begin location"):
                colName2[cols2[i].lower()] = colNum
            
            colNum += 1

    for row2 in sheetName2.iter_rows(min_row = 2, min_col = colName1['chromosome'] + 1, max_col = colName2['begin location'] + 1, values_only = True):
        if (row2[0] != None and row2[colName2['begin location'] - colName1['chromosome']] != None):
            chromlist2.append([row2[0], int(str(row2[colName2['begin location'] - colName1['chromosome']]).split("_")[0])])
            #chromloc2.append()

    return chromlist1, chromlist2

#Finding common chromosome and their location
def findCommon(chromList1, chromList2, loc = [], chro = []):
    print("Finding common...")
    def greater():
        return len(chromList1) > len(chromList2)

    if (greater()):   
        for i in range(len(chromList1)):
            for j in range(len(chromList2)):
                if (chromList1[i][1] == chromList2[j][1]):
                    chro.append([chromList1[i][0], chromList2[j][0]])
                    loc.append(chromList2[j][1])
                # if (chromoList1[i] == chromoList2[j]):
                #     commonChro.append(chromoList1[i])
                #     commonLoc.append(locList1[i])
                # else:
    else:
        for i in range(len(chromList2)):
            for j in range(len(chromList1)):
                if (chromList2[i][1] == chromList1[j][1]):
                    chro.append([chromList1[j][0], chromList2[i][0]])
                    loc.append(chromList1[j][1])

    return chro, loc

#Displaying the common locations found                
def display():
    if (len(commonLoc) != 0 and len(commonChro) != 0):
        for i in range(len(commonLoc)):
            print(f"common chro: {commonChro[i]} at {commonLoc[i]} location")
    else:
        return ("No common locations found!")


#DRIVER CODE
path1 = input("Enter path for file 1: ")
path2 = input("Enter path for file 2: ")

workbook1 = load_workbook(filename = r"{0}".format(path1), read_only = True)
workbook2 = load_workbook(filename = r"{0}".format(path2), read_only = True)

#assigning the active sheet in excel file to a variable
sheet1 = workbook1.active
sheet2 = workbook2.active

chromoList1, chromoList2 = storeData(sheet1, sheet2)
commonChro, commonLoc = findCommon(chromoList1, chromoList2)

#display()

workbook1.close()
workbook2.close()





##########################################################################################################################################################################
#Tests (possible alternatives)

##chromoList1 = defaultdict(list)
##chromoList2 = defaultdict(list)

##for row2 in sheet2.iter_rows(min_row = 2, min_col = 12, max_col = 13, values_only = True):
##    if (row2[1] != None and row2[0] != None and row1[1] != None and row1[4] != None):
##        chromoList2.append(row2[1])
##        locList2.append(row2[0])
##    if (row1[1] != None and row1[4] != None):
##        chromoList1.append(row1[1])
##        locList1.append(row1[4])
##        chromoList1[row1[1]].append(row1[4])

##        chromoList2[row2[1]].append(row2[0])

##    for keys1, values1 in chromoList1.items():
##        for keys2, values2 in chromoList2.items():
##            if (values1 == values2 and values1 != None and values2 != None):
##                if (keys1 == keys2 and keys1 != None and keys2 != None):
##    commonChro.append(keys1)
                    
##    print(commonChro, "\nif")
        
##else:
##    for keys1, values1 in chromoList2.items():
##        for keys2, values2 in chromoList1.items():
##            if (values1 == values2 and values1 != None and values2 != None):
##                if (keys1 == keys2 and keys1 != None and keys2 != None):
##                    commonChro.append(keys1)
##                    
##    print(commonChro, "\nif")

# print("Values are....\n", chromoList1[0])
# print(chromoList2[0])
