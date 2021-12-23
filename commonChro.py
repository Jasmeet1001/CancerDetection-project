import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from collections import defaultdict

chroName = ['chr' + str(i) for i in range(1, 23)]
chroName.extend(['chrX', 'chrY'])

#Sorting the excel file by Begin Location
def SortData(dataFrame_p, ascending_p = True):
    print('Sorting data...')

    sorted_frame = dataFrame_p.sort_values(by = 'Begin Location', ascending = ascending_p)
    
    print('Done.\n')
    return sorted_frame

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
    
    print("Done")

    return chromlist


def findOverlap(chromlist1, chromlist2):
    print("Finding Overlaps...")

    def overlaps(L1, start_p, end_p):
        x = []
        for i in iter(L1):
            start = max(i[0], start_p)
            stop = min(i[1], end_p)

            if (start > stop):
                continue
            else:
                x.extend(list(range(start, stop + 1)))
        return x
  
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
                        overlap_dict[i].extend(start_stop)
                else:
                    for j in chro1:
                        start_stop = overlaps(chro2, j[0], j[1])
                        overlap_dict[i].extend(start_stop)
   
    return overlap_dict

def plot_grph(overlap_dict, chrNum):
    fig,axes = plt.subplots(1, 2, figsize = (16,9))
    fig.suptitle(f"Overlapping Locations(Chromosome {chrNum})")

    overlap_dict_noDup = list(dict.fromkeys(overlap_dict))

    #linePlot
    line = sns.lineplot(ax = axes[0], x = overlap_dict_noDup, y = overlap_dict_noDup, marker = 'o')
    for x,m in zip(overlap_dict_noDup, overlap_dict_noDup): 
        line.text(x = x, y = x, s = f'{m:.0f}')

    line.set_xlabel("VIS-HBV")
    line.set_ylabel("Mutations")

    #HistPlot(Shrink = 0.75)
    hist_p = sns.histplot(ax = axes[1], x = overlap_dict, y = overlap_dict, color="#4CB391", cbar=True, cbar_kws = dict(shrink = .75), stat='count')
    hist_p.set_xlabel("VIS-HBV")
    hist_p.set_ylabel("Mutations")
    
    plt.show()

#Displaying the common locations found along with the chromosome found in both files           
def displayOverlap(final_dict, chrNum):
    if (len(final_dict) == 0):
        # not(('chr' + chrNum) in final_dict) or 
        return "No overlaps found!"
    else:
        print('Displaying...\n')
        return f"Chromosome {chrNum} -> {final_dict}"


#DRIVER CODE
path1 = input("Enter path for file 1: ")
path2 = input("Enter path for file 2: ")

print("Reading Data...")

colNames_toread = ['Chromosome', 'Begin Location', 'End Location']
df1 = pd.read_excel(r"{0}".format(path1))[colNames_toread]
df2 = pd.read_excel(r"{0}".format(path2))[colNames_toread]

print("Done")

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

print("Show overlaps for:\n")
for num, name in enumerate(chroName, 1):
    print(f"{num}. Chromosome {name.split('r')[1]}\n")

while(True):

    chr_to_show = input("Enter chromosome name: ")
    disp_noDup = displayOverlap(list(dict.fromkeys(overlaps[('chr' + chr_to_show)])), chr_to_show)

    if (disp_noDup != "No overlaps found!"):
        print(disp_noDup)
        plot_grph(overlaps[('chr' + chr_to_show)], chr_to_show)
        print('Exit(y/n): ')
        ext = input()
        if (ext == 'y'):
            print('Quitting...')
            break
        else:
            continue
    else:
        print(disp_noDup)
        continue