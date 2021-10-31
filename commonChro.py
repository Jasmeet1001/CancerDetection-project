from openpyxl import load_workbook
import pandas as pd
from collections import defaultdict

def SortData(path1p, path2p, ascending_p = True):
    print('Sorting data...this might take some time')
    df1 = pd.read_excel(r"{0}".format(path1p))
    df2 = pd.read_excel(r"{0}".format(path2p))

    sorted1 = df1.sort_values(by = 'Begin Location', ascending = ascending_p)
    sorted2 = df2.sort_values(by = 'Begin Location', ascending = ascending_p)

    dataframe = pd.DataFrame(sorted1)
    dataframe.to_excel(r"{0}".format(path1p), index = False)    

    dataframe = pd.DataFrame(sorted2)
    dataframe.to_excel(r"{0}".format(path2p), index = False)
    print('Done.\n')

#creating lists to store chromosomes and their location
def storeData(sheetName1, sheetName2):

    chromlist1 = defaultdict(list)
    chromlist2 = defaultdict(list)

    colName1 = {}
    colName2 = {}
    colNum = 0
    
    #displaying max no. of rows
    print(f"Total number of rows/entries in {display_path1[:-5]}: {sheetName1.max_row}")
    print(f"Total number of rows/entries in {display_path2[:-5]}: {sheetName2.max_row}")
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
            chromlist1[int(str(row1[colName2['begin location'] - colName1['chromosome']]).split("_")[0])].append(row1[0])
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
            chromlist2[int(str(row2[colName2['begin location'] - colName1['chromosome']]).split("_")[0])].append(row2[0])
            #chromloc2.append()

    workbook1.close()
    workbook2.close()

    return chromlist1, chromlist2

#Finding common chromosome and their location
def findCommon(chromList1, chromList2, loc = [], chro = []):
    print("Finding common...")

    def greater():
        return len(chromList1) > len(chromList2)

    if (greater()):   
        for key1 in chromList1:
            for key2 in chromList2:
                if (key1 == key2):
                    chro.append([chromList1[key1], chromList2[key2]])
                    loc.append(key2)
    else:
        for key1 in chromList2:
            for key2 in chromList1:
                if (key2 == key1):
                    chro.append([chromList1[key1], chromList2[key2]])
                    loc.append(key1)

    return chro, loc

#Displaying the common locations found                
def display():
    print('Displaying...')
    if (len(commonLoc) != 0 and len(commonChro) != 0):
        for i in range(len(commonLoc)):
            print(f"Common chromosome found in: \n{display_path1[:-5]}: {commonChro[i][0]}\n{display_path2[:-5]}: {commonChro[i][1]}\npresent at location {commonLoc[i]}")
    else:
        return ("No common locations found!")


#DRIVER CODE
path1 = input("Enter path for file 1: ")
path2 = input("Enter path for file 2: ")

display_path1 = path1.split('\\')[-1]
display_path2 = path2.split('\\')[-1]

sorted_ask = input("Is the data/values to compare sorted?(Y/n) ")

if (sorted_ask.lower() != 'y'):
    SortData(path1,path2)

workbook1 = load_workbook(filename = r"{0}".format(path1), read_only = True)
workbook2 = load_workbook(filename = r"{0}".format(path2), read_only = True)

#assigning the active sheet in excel file to a variable
sheet1 = workbook1.active
sheet2 = workbook2.active

chromoList1, chromoList2 = storeData(sheet1, sheet2)
commonChro, commonLoc = findCommon(chromoList1, chromoList2)

display()





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
