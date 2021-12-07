import matplotlib.pyplot as plt
import matplotlib as mat
import numpy as np
import pandas as pd
from collections import defaultdict

chroName = ['chr' + str(i) for i in range(1, 23)]
chroName.extend(['chrX', 'chrY'])

#Sorting the excel file by Begin Location
def SortData(dataFrame_p, ascending_p = True):
    print('Sorting data...')

    sorted_frame = dataFrame_p.sort_values(by = 'Begin Location', ascending = ascending_p)
    
    print('Done.\n')
    return sorted_frame

def setLimitsSame(chrom_dict1, chrom_dict2):


    chrom_dict1_para = chrom_dict1
    chrom_dict2_para = chrom_dict2

    diff = 0
    for i in chroName:
        if (i in chrom_dict1 and i in chrom_dict2):
            chro1 = chrom_dict1[i]
            chro2 = chrom_dict2[i]
        
            if (len(chro1) > len(chro2)):
                diff = len(chro1) - len(chro2)
                chro2.extend([0 for i in range(diff)])
                chrom_dict2_para.update({i:chro2})
        
            else:
                diff = len(chro2) - len(chro1)
                chro1.extend([0 for i in range(diff)])
                chrom_dict1_para.update({i:chro1})

    return chrom_dict1_para, chrom_dict2_para

def storeData(file_dict):
#creating dictonary to store the location and their respective chromosomes
    chromlist = defaultdict(list)
    print("Processing...")

#store the location and chromosomes in the excel file
    file_loc_b = file_dict['Begin Location']
    file_loc_e = file_dict['End Location']
    file_chro = file_dict['Chromosome']
    
    for chro, bloc, eloc in zip(file_chro, file_loc_b, file_loc_e):
        if (pd.isna(eloc) and pd.isna(bloc)):
            continue
        elif (pd.isna(bloc)):
            chromlist[chro].append(list(map(int,[eloc, eloc])))
        elif (pd.isna(eloc)):
            chromlist[chro].append(list(map(int,[bloc, bloc])))
        else:
            chromlist[chro].append(list(map(int,[bloc, eloc])))
    
    return chromlist


def findOverlap(chromlist1, chromlist2):

    def overlaps(L1, start_p, end_p):
        for i in iter(L1):
            start = max(i[0], start_p)
            stop = min(i[1], end_p)

            if (start > stop):
                continue
            else:
                yield [start, stop]

  
    overlap_dict = defaultdict(list)

    for i in chroName:
        if (i in chromlist1 and i in chromlist2):
            chro1 = chromlist1[i]
            chro2 = chromlist2[i]
            
            chro1.sort()
            chro2.sort()

            if (len(chro1) != 0 and chro2 != 0):
                if (len(chro1) > len(chro2)):   
                    for j in chro2:
                        start_stop = overlaps(chro1, j[0], j[1])
                        for overlap_loc in start_stop:
                            overlap_dict[i].append(overlap_loc)
   
    return overlap_dict

#Plotting the values returned by the findCommon function
def PlotGraph(commonChro_p, file_name1, file_name2):
    #Data:
    chro_label = ['chr' + str(i) for i in range(1, 23)]
    # chro_label_num = [i for i in range(1, 25)]
    loc = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    loc1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    #Assigning common locations founds as per their chromosomes
    ind = 0
    for key in commonChro_p:
            for row in commonChro_p[key]:
                for col in range(len(row)):
                    if (ind == 0):
                        index1 = int(row[col].split('r')[1]) - 1
                        loc[index1] = key
                    else:
                        index2 = int(row[col].split('r')[1]) - 1
                        loc1[index2] = key
                ind += 1
            ind = 0

    barWidth = 0.45

    #creating the bar plot
    fig, ax = plt.subplots(figsize = (16,9))

    #setting the x axis limits
    ax.set_xlim([50, 2_050_084_860])

    #creating an array of the number of labels present
    y = np.arange(len(chro_label))

    #plotting the bar plot
    rect1 = ax.barh(y + barWidth/2, loc, barWidth, color = 'r', edgecolor = 'grey',
            label = file_name1)
    rect2 = ax.barh(y - barWidth/2, loc1, barWidth, color = 'b', edgecolor = 'grey',
            label = file_name2)

    #setting limits for x-axis ticks and their rotation
    plt.xticks(np.arange(min(loc), 2_050_084_860, 50_000_000), rotation = 75)

    #formatting how the values are displayed
    ax.xaxis.set_major_formatter(mat.ticker.StrMethodFormatter('{x: .0f}'))

    #removing the boundary lines in graph
    sPine = ['top', 'right']
    remove_spine = [ax.spines[i].set_visible(False) for i in sPine]

    #setting the tick values for y axis
    ax.set_yticks(y)
    ax.set_yticklabels(chro_label)

    #add padding to the labels
    ax.xaxis.set_tick_params(pad = 8)
    ax.yaxis.set_tick_params(pad = 10)

    #creating grid lines
    plt.grid(linestyle = '--', linewidth = 0.5)

    ax.set_title('Common Chromosomes and their locations')
    ax.set_xlabel('Locations')
    ax.set_ylabel('Chromosomes')

    ax.legend()

    #Adding annotations to the bar plots
    ax.bar_label(rect1, fmt = '%.0f', padding = 3, label_type = 'edge')
    ax.bar_label(rect2, fmt = '%.0f', padding = 3, label_type = 'edge')

    plt.show()

#Displaying the common locations found along with the chromosome found in both files           
def displayOverlap(final_dict):
    if (len(final_dict) == 0):
        print("No overlaps found!")
    else:
        print('Displaying...\n')
        for chro,loc in final_dict.items():
            if (loc != None):
                print(f'{chro} -> {loc}\n')

#DRIVER CODE
path1 = input("Enter path for file 1: ")
path2 = input("Enter path for file 2: ")

print("Reading Data...")

colNames_toread = ['Chromosome', 'Begin Location', 'End Location']
df1 = pd.read_excel(r"{0}".format(path1))[colNames_toread]
df2 = pd.read_excel(r"{0}".format(path2))[colNames_toread]

display_path1 = path1.split('\\')[-1]
display_path2 = path2.split('\\')[-1]

#displaying max no. of rows
print(f"Total number of rows/entries in {display_path1[:-5]}: {df1.shape[0]}")
print(f"Total number of rows/entries in {display_path2[:-5]}: {df2.shape[0]}")

sorted_ask = input("Do you want to sort the data/values to compare ?(Y/n) ")
if (sorted_ask.lower() == 'y'):
    df1 = SortData(df1)
    df2 = SortData(df2)

df1_toDict1 = df1.to_dict('list')
df2_toDict2 = df2.to_dict('list')

chromoList1 = storeData(df1_toDict1)
chromoList2 = storeData(df2_toDict2)

overlaps = findOverlap(chromoList1, chromoList2)
# # equal_val_chromL1, equal_val_chromL2 = setLimitsSame(chromoList1, chromoList2)

displayOverlap(overlaps)

# PlotGraph(commonChro, display_path1[:-5], display_path2[:-5])