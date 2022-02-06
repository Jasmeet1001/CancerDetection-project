import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from collections import defaultdict
import json
import turtle

chroName = ['chr' + str(i) for i in range(1, 23)]
chroName.extend(['chrX', 'chrY'])

chromosome_lengths = {'chr1': {'bL': '0', 'eL': '250_000_000'}, 'chr2': {'bL': '0', 'eL': '243_000_000'}, 'chr3': {'bL': '0', 'eL': '200_000_000'}, 'chr4': {'bL': '0', 'eL': '192_000_000'}, 
'chr5': {'bL': '0', 'eL': '181_000_000'}, 'chr6': {'bL': '0', 'eL': '171_000_000'}, 'chr7': {'bL': '0', 'eL': '159_000_000'}, 'chr8': {'bL': '0', 'eL': '147_000_000'}, 'chr9': {'bL': '0', 'eL': '141_000_000'}, 
'chr10': {'bL': '0', 'eL': '136_000_000'}, 'chr11': {'bL': '0', 'eL': '135_000_000'}, 'chr12': {'bL': '0', 'eL': '133_000_000'}, 'chr13': {'bL': '0', 'eL': '115_000_000'}, 
'chr14': {'bL': '0', 'eL': '107_000_000'}, 'chr15': {'bL': '0', 'eL': '101_000_000'}, 'chr16': {'bL': '0', 'eL': '89_000_000'}, 'chr17': {'bL': '0', 'eL': '79_000_000'}, 
'chr18': {'bL': '0', 'eL': '77_000_000'}, 'chr19': {'bL': '0', 'eL': '64_000_000'}, 'chr20': {'bL': '0', 'eL': '63_000_000'}, 'chr21': {'bL': '0', 'eL': '47_000_000'}, 
'chr22': {'bL': '0', 'eL': '50_000_000'}, 'chrX': {'bL': '0', 'eL': '155_000_000'}, 'chrY': {'bL': '0', 'eL': '58_000_000'}}

def chromDraw(norm_overlaps, chrom_toShow):
    rect = turtle.Turtle()
    turtle.setup(1920, 1080)
##rect.hideturtle()
    rect.penup()

    x = -700
    y = 30
    new_y = y - 4

    length_disp = 0
    spacing_limit = 50
    zoom_list_single = []
    zoom_list_double = []

    zoom_list_single_norm = []
    zoom_list_double_norm = []

    diffB, diffE, diffBO = 0, 0, 0
    diffBB, diffBE, diffEE, diffEB, diffBOB, diffBOE = 0, 0, 0, 0, 0, 0

    first = True

    def zoom():
        rect.speed(1)
        rect.color('black')
        rect.penup()
        rect.setposition(x, new_y)

        zoom_list_single_noDup = list(dict.fromkeys(zoom_list_single))
        zoom_list_single_norm_noDup = list(dict.fromkeys(zoom_list_single_norm))

        zoom_list_double_noDup = list(sorted(set(tuple(inner) for inner in zoom_list_double)))
        zoom_list_double_norm_noDup = list(dict.fromkeys(zoom_list_double_norm))
        rect.forward(zoom_list_single_norm_noDup[len(zoom_list_single_norm_noDup)//2])
        rect.right(90)
        rect.penup()
        rect.forward(72)
        rect.pendown()
        rect.right(45)
        rect.forward(250)
        rect.penup()
        rect.backward(250)
        rect.left(90)
        rect.pendown()
        rect.forward(250)
        rect.penup()
        rect.left(45)
        rect.forward(120)
        rect.right(90)
        rect.forward(30)
        rect.right(90)

        rect.begin_fill()
        for i in range(2):
            rect.forward(600)
            rect.left(90)
            rect.forward(60)
            rect.left(90)
        rect.end_fill()
    ##  rect.color('')
        rect.forward(600)
        rect.right(180)

    with open(r'E:\CancerDetection-project-1\normalized_overlap_Files\overlaps_normalized_HBV_VIS.json') as json_file1, open(r'E:\CancerDetection-project-1\OverlapsFound_in_DataSets\overlapsFound_HBV_VIS.json') as json_file2:

        over = json.load(json_file1)
        over_ori = json.load(json_file2)

        for i in over.keys():

            rect.speed(6)

            rect.setposition(0, 130)
            rect.pendown()
            rect.color('black')
            rect.write(f"Chromosome {i.split('r')[1]}", font=("Verdana", 15, "normal"), align = 'center')
            rect.penup()
            rect.setposition(x,y)
            rect.pendown()

            rect.speed(0)

            rect.begin_fill()
            for r in range(2):
                if (length_disp == 0):
                    rect.write(f"{chromosome_lengths[i]['bL']}", font=("Verdana", 10, "normal"), align = 'center')
                    length_disp += 1

                rect.forward(1400)

                if (length_disp == 1):
                    rect.write(f"{chromosome_lengths[i]['eL']}", font=("Verdana", 10, "normal"), align = 'center')
                    length_disp += 1

                rect.right(90)
                rect.forward(60)
                rect.right(90)
            rect.end_fill()

            length_disp = 0

            rect.penup()
            rect.right(90)
            rect.forward(100)
            rect.left(90)

            for j in range(len(over[i])):
                if (len(over[i][j]) == 1):
                    rect.setposition(x,new_y)
                    rect.color('#0000ff')
                    rect.penup()
                    rect.forward(over[i][j]['bL'])
                    rect.right(90)
                    rect.pendown()
                    rect.forward(52)

    ##                rect.penup()
    ##                rect.forward(20)
    ##                rect.pendown()
    ##                rect.write(f"{over_ori[i][j]['bL']}", font=("Verdana", 8, "normal"), align = 'right')
    ##                rect.penup()
    ##                rect.backward(20)

                    rect.left(90)

                    if (not first):
                        if (len(over[i][j - 1]) == 2):
                            diffB = over[i][j]['bL'] - over[i][j - 1]['bL']
                            diffE = over[i][j]['bL'] - over[i][j - 1]['eL']
                            if (diffB < 0):
                                diffB = -(diffB)
                            if (diffE < 0):
                                diffE = -(diffE)

                            if ((j != (len(over[i]) - 1)) and ((diffB <= spacing_limit) or (diffE <= spacing_limit))):
                                zoom_list_single.append(over_ori[i][j]['bL'])
                                zoom_list_single_norm.append(over[i][j]['bL'])

                                zoom_list_double.append([over_ori[i][j - 1]['bL'], over_ori[i][j - 1]['eL']])
                                zoom_list_double_norm.append(over[i][j - 1]['bL'])

                            else:
                                if ((j == (len(over[i]) - 1)) or ((len(zoom_list_single) > 1 or len(zoom_list_double) > 1))):
                                    zoom()
    ##                              for i in zoom_list_single_noDup:


                        elif (len(over[i][j - 1]) == 1):
                            diffBO = over[i][j]['bL'] - over[i][j - 1]['bL']

                            if (diffBO < 0):
                                diffBO = -(diffBO)

                            if ((j != (len(over[i]) - 1)) and diffBO <= spacing_limit):
                                zoom_list_single.extend([over_ori[i][j - 1]['bL'], over_ori[i][j]['bL']])

                                zoom_list_single_norm.extend([over[i][j - 1]['bL'], over[i][j]['bL']])
                            else:
                                if ((j == (len(over[i]) - 1)) or ((len(zoom_list_single) > 1 or len(zoom_list_double) > 1))):
                                    zoom()
                    else:
                        first = False

                    print(f'{i}, B-> {diffB}, E-> {diffE}, BO-> {diffBO}, len 1')

                    rect.penup()

                elif (len(over[i][j]) == 2):
                    rect.setposition(x,new_y)
                    rect.color('red')
                    rect.penup()
                    rect.forward(over[i][j]['bL'])
                    rect.right(90)
                    rect.pendown()

                    rect.begin_fill()
                    rect.forward(52)
    ##                rect.penup()
    ##                rect.forward(20)
    ##                rect.pendown()
    ##                rect.write(f"{over_ori[i][j]['bL']}", font=("Verdana", 8, "normal"), align = 'right')
    ##                rect.penup()
    ##                rect.backward(20)
    ##                rect.pendown()

                    rect.left(90)
                    rect.forward(over[i][j]['eL'] - over[i][j]['bL'])

    ##                rect.penup()
    ##                rect.right(90)
    ##                rect.forward(20)
    ##                rect.pendown()
    ##                rect.write(f"  {over_ori[i][j]['eL']}", font=("Verdana", 8, "normal"), align = 'left')
    ##                rect.penup()
    ##                rect.backward(20)
    ##                rect.pendown()
    ##                rect.left(90)

                    rect.left(90)
                    rect.forward(52)
                    rect.left(90)
                    rect.forward(over[i][j]['eL'] - over[i][j]['bL'])
                    rect.end_fill()
                    rect.right(180)
                    rect.penup()

                    if (not first):
                        if (len(over[i][j - 1]) == 2):
                            diffBB = over[i][j]['bL'] - over[i][j - 1]['bL']
                            diffBE = over[i][j]['bL'] - over[i][j - 1]['eL']
                            diffEE = over[i][j]['eL'] - over[i][j - 1]['eL']
                            diffEB = over[i][j]['eL'] - over[i][j - 1]['bL']

                            if (diffBB < 0):
                                diffBB = -(diffBB)
                            if (diffEE < 0):
                                diffEE = -(diffEE)
                            if (diffBE < 0):
                                diffBE = -(diffBE)
                            if (diffEB < 0):
                                diffEB = -(diffEB)

                            if ((j != (len(over[i]) - 1)) and ((diffBB <= spacing_limit) or (diffEE <= spacing_limit) or (diffBE <= spacing_limit) or (diffBE <= spacing_limit))):
                                zoom_list_double_norm.append(over[i][j - 1]['bL'])
                                zoom_list_double.append([over_ori[i][j - 1]['bL'],over_ori[i][j - 1]['eL']])

                                zoom_list_double_norm.append(over[i][j]['bL'])
                                zoom_list_double.append([over_ori[i][j]['bL'], over_ori[i][j]['eL']])
                            else:
                                if ((j == (len(over[i]) - 1)) or ((len(zoom_list_single) > 1 or len(zoom_list_double) > 1))):
                                    zoom()

                        elif (len(over[i][j - 1]) == 1):
                            diffBOB = over[i][j]['bL'] - over[i][j - 1]['bL']
                            diffBOE = over[i][j]['eL'] - over[i][j - 1]['bL']

                            if (diffBOB < 0):
                                diffBOB = -(diffBOB)
                            if (diffBOE < 0):
                                diffBOE = -(diffBOE)

                            if ((j != (len(over[i]) - 1)) and ((diffBOB <= spacing_limit) or (diffBOE <= spacing_limit))):
                                zoom_list_single_norm.append(over[i][j - 1]['bL'])
                                zoom_list_single.append(over_ori[i][j - 1]['bL'])

                                zoom_list_double_norm.append(over[i][j]['bL'])
                                zoom_list_double.append([over_ori[i][j]['bL'], over_ori[i][j]['eL']])
                            else:
                                if ((j == (len(over[i]) - 1)) or ((len(zoom_list_single) > 1 or len(zoom_list_double) > 1))):
                                    zoom()
                    else:
                        first = False

                    print(f'{i}, B-> {diffB}, BB-> {diffBB}, BE-> {diffBE}, E-> {diffE}, EE-> {diffEE}, EB-> {diffEB} , BO-> {diffBO}, BOB-> {diffBOB}, BOE-> {diffBOE}, len 2')


            if (i == 'chr1'):
                turtle.exitonclick()

            rect.penup()
            rect.speed(1)
            rect.forward(1000)
            rect.clear()
            first = True
            diffB, diffE, diffBO = 0, 0, 0
            diffBB, diffBE, diffEE, diffEB, diffBOB, diffBOE = 0, 0, 0, 0, 0, 0
            zoom_list_single.clear()
            zoom_list_single.clear()


        rect.speed(6)
        rect.color('black')
        rect.setposition(0,0)
        rect.write("End of overlaps", font = ("Verdana", 40, "normal"), align = 'center')
        turtle.done()


def to_json(original_overlaps, normalized_overlaps, file_name, file_name_normalized):
    with open(f"{file_name}.json", 'w') as ori_overlaps:
        json.dump(original_overlaps, ori_overlaps, indent = 0)
    
    with open(f"{file_name_normalized}.json", 'w') as norm_overlaps:
        json.dump(normalized_overlaps, norm_overlaps, indent = 0)


def storeData(file_dict):
#creating dictonary to store the location and their respective chromosomes
    chromlist = defaultdict(list)
    print("Processing...", end = '')

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
        y = []
        for i in iter(L1):
            start = max(i[0], start_p)
            stop = min(i[1], end_p)
            
            if (start > stop):
                continue
            else:
                x.append([start,stop])
                y.extend(list(range(start, stop + 1)))

        return x, y
  
    overlap_dict = defaultdict(list)
    overlap_dict_plot = defaultdict(list)

    for i in chroName:
        if (i in chromlist1 and i in chromlist2):
            chro1 = chromlist1[i]
            chro2 = chromlist2[i]
            
            chro1.sort()
            chro2.sort()

            if (len(chro1) != 0 and chro2 != 0):
                if (len(chro1) > len(chro2)):   
                    for j in chro2:
                        start_stop_x, start_stop_y = overlaps(chro1, j[0], j[1])
                        overlap_dict[i].extend(start_stop_x)
                        overlap_dict_plot[i].extend(start_stop_y)
                else:
                    for j in chro1:
                        start_stop_x, start_stop_y = overlaps(chro2, j[0], j[1])
                        overlap_dict[i].extend(start_stop_x)
                        overlap_dict_plot[i].extend(start_stop_y)
            else:
                continue
        else:
            continue

        overlaps_noDup = list(sorted(set(tuple(inner) for inner in overlap_dict[i])))
        
        overlap_dict[i].clear()

        for val in overlaps_noDup:
            overlap_dict[i].append({'bL': val[0], 'eL': val[1]})

    return overlap_dict, overlap_dict_plot

def normalize(overlaps_file):
    normalized_overlaps = defaultdict(list)

    for i in chroName:
        for ori in overlaps_file[i]:
            temp_scaled_val_bL = ((ori['bL'] - int(chromosome_lengths[f'{i}']['bL']))/(int(chromosome_lengths[f'{i}']['eL']) - int(chromosome_lengths[f'{i}']['bL']))) * (int(chromosome_lengths[f'{i}']['eL'].split('_')[0]) - int(chromosome_lengths[f'{i}']['bL'])) + int(chromosome_lengths[f'{i}']['bL'])
            if (ori['bL'] == ori['eL']):
                normalized_overlaps[i].append({'bL': temp_scaled_val_bL})
            else:
                temp_scaled_val_eL = ((ori['eL'] - int(chromosome_lengths[f'{i}']['bL']))/(int(chromosome_lengths[f'{i}']['eL']) - int(chromosome_lengths[f'{i}']['bL']))) * (int(chromosome_lengths[f'{i}']['eL'].split('_')[0]) - int(chromosome_lengths[f'{i}']['bL'])) + int(chromosome_lengths[f'{i}']['bL'])
                normalized_overlaps[i].append({'bL': temp_scaled_val_bL, 'eL': temp_scaled_val_eL})

    return normalized_overlaps


def plot_grph(overlap_dict, chrNum):

    fig,ax = plt.subplots(nrows=2, ncols=1)
    fig.suptitle(f"Overlapping Locations(Chromosome {chrNum})")

    norm_overlap_dict = []
    overlaps_count = {}
    
    for val in overlap_dict:
        temp_norm = ((val - int(chromosome_lengths[f'chr{chrNum}']['bL']))/(int(chromosome_lengths[f'chr{chrNum}']['eL']) - int(chromosome_lengths[f'chr{chrNum}']['bL']))) * (int(chromosome_lengths[f'chr{chrNum}']['eL'].split('_')[0]) - int(chromosome_lengths[f'chr{chrNum}']['bL'])) + int(chromosome_lengths[f'chr{chrNum}']['bL'])
        norm_overlap_dict.append(temp_norm)
    
    overlapdict_listval_noDup = list(dict.fromkeys(norm_overlap_dict))
    for dup in overlapdict_listval_noDup:
        overlaps_count[dup] = norm_overlap_dict.count(dup)

    #linePlot with locations
    line = sns.lineplot(ax = ax[0], x = overlapdict_listval_noDup, y = overlapdict_listval_noDup, marker = 'o')
    for x,m in zip(overlapdict_listval_noDup, overlapdict_listval_noDup): 
        line.text(x = x, y = x, s = f'{m:.6f}')
    line.set_xlim(int(chromosome_lengths[f'chr{chrNum}']['bL']), int(chromosome_lengths[f'chr{chrNum}']['eL'].split('_')[0]))
    line.set_ylim(int(chromosome_lengths[f'chr{chrNum}']['bL']), int(chromosome_lengths[f'chr{chrNum}']['eL'].split('_')[0]))
    line.set_xlabel("VIS-HBV")
    line.set_ylabel("Mutations")

    #lineplot with duplicate values
    line_count = sns.lineplot(ax = ax[1], x = overlaps_count.keys(), y = overlaps_count.values(),  marker = 'o')
    for x,m in zip(overlaps_count.keys(), overlaps_count.values()):
        line_count.text(x = x, y = m, s = f'{m:.0f}')

    line_count.set_xlim(int(chromosome_lengths[f'chr{chrNum}']['bL']), int(chromosome_lengths[f'chr{chrNum}']['eL'].split('_')[0]))
    line_count.set_ylim(0, max(overlaps_count.values()) + 1)
    line_count.set_xlabel("Overlaps")
    line_count.set_ylabel("Number of occurences")
    
    plt.show()

def chromosomeDraw(norm_values, chro_num):
    fig, ax = plt.subplots()

    single_mutation = 'blue'
    ranged_mutation = 'red'

    ax.add_patch(plt.Rectangle((0, 45), int(chromosome_lengths['chr' + chro_num]['eL'].split('_')[0]), 10, fc = 'black'))
    
    for plot in norm_values:
        
        if (len(plot) == 1):
            ax.plot([plot['bL'], plot['bL']], [45.5, 54.5], color = single_mutation)
        
        elif (len(plot) == 2):
            ax.plot([plot['bL'], plot['bL']], [45.5, 54.5], color = ranged_mutation)
            ax.plot([plot['eL'], plot['eL']], [46, 54], color = ranged_mutation)

            ax.plot([plot['bL'], plot['eL']], [54.5, 54.5], color = ranged_mutation)
            ax.plot([plot['bL'], plot['eL']], [45.5, 45.5], color = ranged_mutation)
            
    plt.yticks([])
    plt.xlim(-10, int(chromosome_lengths['chr' + chro_num]['eL'].split('_')[0]) + 10)
    plt.ylim(-10, 100)
    plt.show()

#Displaying the common locations found along with the chromosome found in both files           
def displayOverlap(final_overlap_list, chrNum):
    values_noDup = list(dict.fromkeys(final_overlap_list))
    if (len(final_overlap_list) == 0):
        return "No overlaps found!"
    else:
        print('Displaying...\n')
        return f"Chromosome {chrNum} -> {values_noDup}"


#DRIVER CODE

path1 = input("Enter path for file 1: ")
path2 = input("Enter path for file 2: ")

print("Reading Data...")

colNames_toread = ['Chromosome', 'Begin Location', 'End Location']

if (path1[-4:] == 'xlsx' and path2[-4:] == 'xlsx'):
    df1 = pd.read_excel(r"{0}".format(path1))[colNames_toread]
    df2 = pd.read_excel(r"{0}".format(path2))[colNames_toread]

elif (path1[-4:] == 'json' and path2[-4:] == 'json'):
    df1 = pd.read_json(r"{0}".format(path1))[colNames_toread]
    df2 = pd.read_json(r"{0}".format(path2))[colNames_toread]


print("Done")

display_path1 = path1.split('\\')[-1]
display_path2 = path2.split('\\')[-1]

#displaying max no. of rows
print(f"Total number of rows/entries in {display_path1[:-5]}: {df1.shape[0]}")
print(f"Total number of rows/entries in {display_path2[:-5]}: {df2.shape[0]}")

df1_toDict1 = df1.to_dict('list')
df2_toDict2 = df2.to_dict('list')

chromoList1 = storeData(df1_toDict1)
chromoList2 = storeData(df2_toDict2)

overlaps, overlaps_std_wth_Dup = findOverlap(chromoList1, chromoList2)
overlaps_normalized = normalize(overlaps)

# to_json(overlaps, overlaps_normalized, f"{display_path1[:-5]}_{display_path2[:-5]}Overlaps", f"{display_path1[:-5]}_{display_path2[:-5]}_NormalizedOverlaps")

print("Show overlaps for:\n")
for num, name in enumerate(chroName, 1):
    print(f"{num}. Chromosome {name.split('r')[1]}\n")

while(True):

    chr_to_show = input("Enter chromosome name: ")
    disp_noDup = displayOverlap(overlaps_std_wth_Dup[('chr' + chr_to_show)], chr_to_show)

    if (disp_noDup != "No overlaps found!"):
        print(disp_noDup)
        plot_grph(overlaps_std_wth_Dup[('chr' + chr_to_show)], chr_to_show)
        chromosomeDraw(overlaps_normalized[('chr' + chr_to_show)], chr_to_show)
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