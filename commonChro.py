import matplotlib.pyplot as plt
import matplotlib as mat
import numpy as np
import pandas as pd
from collections import defaultdict

#Sorting the excel file by Begin Location
def SortData(dataFrame_p, ascending_p = True):
    print('Sorting data...')

    dataFrame_p.sort_values(by = 'Begin Location', ascending = ascending_p, inplace = True)
    
    print('Done.\n')
    return dataFrame_p

#Storing data in a dictionary and returning it
def storeData(file_dict):
    #creating dictonary to store the location and their respective chromosomes
    chromlist = defaultdict(list)

    print("Processing...")
    
    #store the location and chromosomes in the excel file
    file_loc = file_dict['Begin Location']
    file_chro = file_dict['Chromosome']

    for loc, chro in zip(file_loc, file_chro):
        chromlist[loc].append(chro)

    return chromlist

#Finding common location and their respective chromosome
def findCommon(chromList1, chromList2, chro = {}):
    print("Finding common...")

    #Function to check and return which dataSet has more entries/values
    def greater():
        return len(chromList1) > len(chromList2)

    #accessing keys from the the dictonary and finding common ones
    if (greater()):
        for key1 in chromList1.keys():
            if (key1 in chromList2.keys()):
                chro[key1] = [chromList1[key1], chromList2[key1]]
    else:
        for key1 in chromList2.keys():
            if (key1 in chromList1.keys()):
                chro[key1] = [chromList1[key1], chromList2[key1]]

    return chro

#Plotting the values returned by the findCommon function
def PlotGraph(commonChro_p, file_name1, file_name2):
    #Data:
    chro_label = ['chr' + str(i) for i in range(1, 25)]
    chro_label_num = [i for i in range(1, 25)]
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
def display():
    print('Displaying...')
    if (len(commonChro) != 0):
        for key in commonChro.keys():
            print(f"Common chromosome found in: \n{display_path1[:-5]}: {commonChro[key][0]}\n{display_path2[:-5]}: {commonChro[key][1]}\npresent at location {key}")
    else:
        return ("No common locations found!")


#DRIVER CODE
path1 = input("Enter path for file 1: ")
path2 = input("Enter path for file 2: ")

print("Reading Data...")

colNames_toread = ['Chromosome', 'Begin Location']
df1 = pd.read_excel(r"{0}".format(path1))[colNames_toread]
df2 = pd.read_excel(r"{0}".format(path2))[colNames_toread]

display_path1 = path1.split('\\')[-1]
display_path2 = path2.split('\\')[-1]

sorted_ask = input("Do you want to sort the data/values to compare ?(Y/n) ")

if (sorted_ask.lower() == 'y'):
    df1 = SortData(df1)
    df2 = SortData(df2)

#displaying max no. of rows
print(f"Total number of rows/entries in {display_path1[:-5]}: {df1.shape[0]}")
print(f"Total number of rows/entries in {display_path2[:-5]}: {df2.shape[0]}")

df_dict_1 = df1.to_dict('list')
df_dict_2 = df2.to_dict('list')

chromoList1 = storeData(df_dict_1)
chromoList2 = storeData(df_dict_2)

commonChro = findCommon(chromoList1, chromoList2)

display()

PlotGraph(commonChro, display_path1[:-5], display_path2[:-5])