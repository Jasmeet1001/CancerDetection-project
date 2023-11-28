import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import json
import turtle
import dash_bio as dashbio
import dash
import plotly.express as px

from dash.dependencies import Input, Output
from dash import html, dcc
from collections import defaultdict
from pathlib import Path

CHRO_NAME = ['chr' + str(i) for i in range(1, 23)]
CHRO_NAME.extend(['chrX', 'chrY'])

CHROMOSOME_LENGTHS = {
    'chr1': {'bL': '0', 'eL': '250_000_000'}, 'chr2': {'bL': '0', 'eL': '243_000_000'}, 'chr3': {'bL': '0', 'eL': '200_000_000'}, 'chr4': {'bL': '0', 'eL': '192_000_000'},
    'chr5': {'bL': '0', 'eL': '181_000_000'}, 'chr6': {'bL': '0', 'eL': '171_000_000'}, 'chr7': {'bL': '0', 'eL': '159_000_000'}, 'chr8': {'bL': '0', 'eL': '147_000_000'},
    'chr9': {'bL': '0', 'eL': '141_000_000'},'chr10': {'bL': '0', 'eL': '136_000_000'}, 'chr11': {'bL': '0', 'eL': '135_000_000'}, 'chr12': {'bL': '0', 'eL': '133_000_000'},
    'chr13': {'bL': '0', 'eL': '115_000_000'},'chr14': {'bL': '0', 'eL': '107_000_000'}, 'chr15': {'bL': '0', 'eL': '101_000_000'}, 'chr16': {'bL': '0', 'eL': '89_000_000'},
    'chr17': {'bL': '0', 'eL': '79_000_000'},'chr18': {'bL': '0', 'eL': '77_000_000'}, 'chr19': {'bL': '0', 'eL': '64_000_000'}, 'chr20': {'bL': '0', 'eL': '63_000_000'},
    'chr21': {'bL': '0', 'eL': '47_000_000'},'chr22': {'bL': '0', 'eL': '50_000_000'}, 'chrX': {'bL': '0', 'eL': '155_000_000'}, 'chrY': {'bL': '0', 'eL': '58_000_000'}
    }


def chromosome_mapper(annotations_p, vr_name):
    app = dash.Dash(__name__)

    chrom = set(i['chr'] for i in annotations_p)
    
    app.layout = html.Div(style = {"textAlign": "center"}, children = [
    f'Chromosome overlap viewer {vr_name}',
    
    dashbio.Ideogram(
        id = 'chromosome_mapper',
        orientation = 'horizontal',
        chrHeight = 1200,
        chrWidth = 25,
        rotatable = False,
        chromosomes = list(chrom),
        annotations = annotations_p,
        showBandLabels = True,
        annotationsLayout = "tracks",
        annotationHeight = 5,
    ),
    html.Div(id='my-default-ideogram-rotated')
    ])

    app.run_server()


def read_file(file_path: str):
    '''
    Reads the given excel or json file and converts it into an ordered dictionary to be processed further. Takes in
    the path of the file as an argument.
    '''
    print("Reading Data...")

    colNames_toread = ['Chromosome', 'Begin Location', 'End Location']
    
    match (Path(file_path).suffix):
        case '.xlsx':
            df = pd.read_excel(r"{0}".format(file_path))[colNames_toread]
        case '.json':
            df = pd.read_json(r"{0}".format(file_path))[colNames_toread]
        case _:
            print("Invalid file paths.\nRetry")
            exit()

    print("Done")

    #displaying max no. of rows
    print(f"Total number of rows/entries in {Path(file_path).stem}: {df.shape[0]}")
    
    return df.to_dict('list')

def chrom_draw(norm_overlaps: str, chrom_toShow: str):
    '''
    Incomplete and Deprecated, draws a chromosome and its respective locations in 'turtle'. Provides a zoomed-in view for values too 
    close to be differentiated at default view. Takes in the normalized overlap dictionary returned by normalize(deprecated) 
    function and name of the chromosome to display the drawing for as arguments.
    '''
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

    diff_B, diff_E, diff_BO = 0, 0, 0
    diff_BB, diff_BE, diff_EE, diff_EB, diff_BOB, diff_BOE = 0, 0, 0, 0, 0, 0

    first = True

    def zoom():
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
                    rect.write(f"{CHROMOSOME_LENGTHS[i]['bL']}", font=("Verdana", 10, "normal"), align = 'center')
                    length_disp += 1

                rect.forward(1400)

                if (length_disp == 1):
                    rect.write(f"{CHROMOSOME_LENGTHS[i]['eL']}", font=("Verdana", 10, "normal"), align = 'center')
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

                    rect.left(90)

                    if (not first):
                        if (len(over[i][j - 1]) == 2):
                            diff_B = over[i][j]['bL'] - over[i][j - 1]['bL']
                            diff_E = over[i][j]['bL'] - over[i][j - 1]['eL']
                            if (diffB < 0):
                                diffB = -(diffB)
                            if (diffE < 0):
                                diffE = -(diffE)

                            if ((j != (len(over[i]) - 1)) and ((diff_B <= spacing_limit) or (diff_E <= spacing_limit))):
                                zoom_list_single.append(over_ori[i][j]['bL'])
                                zoom_list_single_norm.append(over[i][j]['bL'])

                                zoom_list_double.append([over_ori[i][j - 1]['bL'], over_ori[i][j - 1]['eL']])
                                zoom_list_double_norm.append(over[i][j - 1]['bL'])

                            else:
                                if ((j == (len(over[i]) - 1)) or ((len(zoom_list_single) > 1 or len(zoom_list_double) > 1))):
                                    zoom()


                        elif (len(over[i][j - 1]) == 1):
                            diff_BO = over[i][j]['bL'] - over[i][j - 1]['bL']

                            if (diff_BO < 0):
                                diff_BO = -(diff_BO)

                            if ((j != (len(over[i]) - 1)) and diff_BO <= spacing_limit):
                                zoom_list_single.extend([over_ori[i][j - 1]['bL'], over_ori[i][j]['bL']])

                                zoom_list_single_norm.extend([over[i][j - 1]['bL'], over[i][j]['bL']])
                            else:
                                if ((j == (len(over[i]) - 1)) or ((len(zoom_list_single) > 1 or len(zoom_list_double) > 1))):
                                    zoom()
                    else:
                        first = False

                    print(f'{i}, B-> {diff_B}, E-> {diff_E}, BO-> {diff_BO}, len 1')

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

                    rect.left(90)
                    rect.forward(over[i][j]['eL'] - over[i][j]['bL'])

                    rect.left(90)
                    rect.forward(52)
                    rect.left(90)
                    rect.forward(over[i][j]['eL'] - over[i][j]['bL'])
                    rect.end_fill()
                    rect.right(180)
                    rect.penup()

                    if (not first):
                        if (len(over[i][j - 1]) == 2):
                            diff_BB = over[i][j]['bL'] - over[i][j - 1]['bL']
                            diff_BE = over[i][j]['bL'] - over[i][j - 1]['eL']
                            diff_EE = over[i][j]['eL'] - over[i][j - 1]['eL']
                            diff_EB = over[i][j]['eL'] - over[i][j - 1]['bL']

                            if (diff_BB < 0):
                                diff_BB = -(diff_BB)
                            if (diff_EE < 0):
                                diff_EE = -(diff_EE)
                            if (diff_BE < 0):
                                diff_BE = -(diff_BE)
                            if (diff_EB < 0):
                                diff_EB = -(diff_EB)

                            if ((j != (len(over[i]) - 1)) and ((diff_BB <= spacing_limit) or (diff_EE <= spacing_limit) or (diff_BE <= spacing_limit) or (diff_BE <= spacing_limit))):
                                zoom_list_double_norm.append(over[i][j - 1]['bL'])
                                zoom_list_double.append([over_ori[i][j - 1]['bL'],over_ori[i][j - 1]['eL']])

                                zoom_list_double_norm.append(over[i][j]['bL'])
                                zoom_list_double.append([over_ori[i][j]['bL'], over_ori[i][j]['eL']])
                            else:
                                if ((j == (len(over[i]) - 1)) or ((len(zoom_list_single) > 1 or len(zoom_list_double) > 1))):
                                    zoom()

                        elif (len(over[i][j - 1]) == 1):
                            diff_BOB = over[i][j]['bL'] - over[i][j - 1]['bL']
                            diff_BOE = over[i][j]['eL'] - over[i][j - 1]['bL']

                            if (diff_BOB < 0):
                                diff_BOB = -(diff_BOB)
                            if (diff_BOE < 0):
                                diff_BOE = -(diff_BOE)

                            if ((j != (len(over[i]) - 1)) and ((diff_BOB <= spacing_limit) or (diff_BOE <= spacing_limit))):
                                zoom_list_single_norm.append(over[i][j - 1]['bL'])
                                zoom_list_single.append(over_ori[i][j - 1]['bL'])

                                zoom_list_double_norm.append(over[i][j]['bL'])
                                zoom_list_double.append([over_ori[i][j]['bL'], over_ori[i][j]['eL']])
                            else:
                                if ((j == (len(over[i]) - 1)) or ((len(zoom_list_single) > 1 or len(zoom_list_double) > 1))):
                                    zoom()
                    else:
                        first = False

                    print(f'{i}, B-> {diff_B}, BB-> {diff_BB}, BE-> {diff_BE}, E-> {diff_E}, EE-> {diff_EE}, EB-> {diff_EB} , BO-> {diff_BO}, BOB-> {diff_BOB}, BOE-> {diff_BOE}, len 2')


            if (i == 'chr1'):
                turtle.exitonclick()

            rect.penup()
            rect.speed(1)
            rect.forward(1000)
            rect.clear()
            first = True
            diff_B, diff_E, diff_BO = 0, 0, 0
            diff_BB, diff_BE, diff_EE, diff_EB, diff_BOB, diff_BOE = 0, 0, 0, 0, 0, 0
            zoom_list_single.clear()
            zoom_list_single.clear()


        rect.speed(6)
        rect.color('black')
        rect.setposition(0,0)
        rect.write("End of overlaps", font = ("Verdana", 40, "normal"), align = 'center')
        turtle.done()

def to_json(original_overlaps: dict, file_name: str):
    '''
    Convert the overlaps found into a json file format. Takes in the overlap dictionary and the name of the file to
    be created as arguments.
    '''
    with open(f"{file_name}.json", 'w') as ori_overlaps:
        json.dump(original_overlaps, ori_overlaps, indent = 0)
    
    # with open(f"{file_name_normalized}.json", 'w') as norm_overlaps:
    #     json.dump(normalized_overlaps, norm_overlaps, indent = 0)

def convert_excel(overlap_file: dict, file_name: str):
    '''
    Convert the overlaps found into an excel file format. Takes in the overlap dictionary and the name of the file
    to be created as arguments.
    '''
    df_first = pd.DataFrame(columns = ['Chromosome', 'Begin Location', 'End Location'])

    for chro in overlap_file:
            df1 = pd.DataFrame({'Chromosome': [chro['chr']], 'Begin Location': [chro['start']], 'End Location': [chro['stop']]}, columns = ['Chromosome', 'Begin Location', 'End Location'])
            df_first = pd.concat([df_first, df1])

    df_first.to_excel(f'{file_name}.xlsx', sheet_name = 'Sheet1', index = False)

def store_data(file_dict: dict):
    '''
    Takes in a dictionary in {'column_name': [row_value]} format as argument and outputs a dictionary sorted 
    by "Chromosomes".
    '''
    #creating dictonary to store the location and their respective chromosomes
    chrom_list = defaultdict(list)
    print("Processing...", end = '')

    #store the location and chromosomes in the excel file
    file_loc_b = file_dict['Begin Location']
    file_loc_e = file_dict['End Location']
    file_chro = file_dict['Chromosome']
    
    for chro, bloc, eloc in zip(file_chro, file_loc_b, file_loc_e):
        if (pd.isna(eloc) and pd.isna(bloc)):
            continue
        elif (pd.isna(bloc)):
            chrom_list[chro].append(list(map(int,[eloc, eloc])))
        elif (pd.isna(eloc)):
            chrom_list[chro].append(list(map(int,[bloc, bloc])))
        else:
            if (bloc > eloc):
                bloc, eloc = eloc, bloc
            chrom_list[chro].append(list(map(int,[bloc, eloc])))
    
    print("Done")

    return chrom_list

def find_overlap(chrom_list1: dict, chrom_list2: dict):
    '''
    Finds overlap between the two dictionaries returned by the store_data function as arguments and returns two dictionaries
    one with closed range values the other with range values opened.
    '''
    print("Finding Overlaps...")

    def overlaps(L1: list, start_p: int, end_p: int):
        closed_range = []
        open_range = []
        mid = (0 + ((len(L1)-1)-0)) // 2

        for i, j in zip(L1[:mid], L1[mid:]):
            start_left = max(i[0], start_p)
            stop_left = min(i[1], end_p)

            start_right = max(j[0], start_p)
            stop_right = min(j[1], end_p)
            
            if ((start_left > stop_left) and (start_right > stop_right)):
                continue
            elif (start_right > stop_right):
                closed_range.append([start_left, stop_left])
                open_range.extend(list(range(start_left, stop_left + 1)))
            elif (start_left > stop_left):
                closed_range.append([start_right, stop_right])
                open_range.extend(list(range(start_right, stop_right + 1)))
            else:
                closed_range.append([start_left, stop_left])
                open_range.extend(list(range(start_left, stop_left + 1)))

                closed_range.append([start_right, stop_right])
                open_range.extend(list(range(start_right, stop_right + 1)))

                
        return closed_range, open_range
  
    overlap_dict_closed_range = defaultdict(list)
    overlap_dict_open_range = defaultdict(list)
    final_closed_range_list = []

    for i in CHRO_NAME:
        if (i in chrom_list1 and i in chrom_list2):
            chro1 = chrom_list1[i]
            chro2 = chrom_list2[i]
            
            chro1.sort()
            chro2.sort()

            if (len(chro1) != 0 and len(chro2) != 0):
                if (len(chro1) > len(chro2)):   
                    
                    for j in chro2:
                        start_stop_closed, start_stop_open = overlaps(chro1, j[0], j[1])
                        
                        overlap_dict_closed_range[i].extend(start_stop_closed)
                        overlap_dict_open_range[i].extend(start_stop_open)
                else:
                    
                    for j in chro1:
                        start_stop_closed, start_stop_open = overlaps(chro2, j[0], j[1])
                        
                        overlap_dict_closed_range[i].extend(start_stop_closed)
                        overlap_dict_open_range[i].extend(start_stop_open)

        overlaps_noDup = list(sorted(set(tuple(inner) for inner in overlap_dict_closed_range[i])))
        overlap_dict_open_range[i] = list(dict.fromkeys(overlap_dict_open_range[i]))

        for val in overlaps_noDup:
            final_closed_range_list.append({"chr": i.split("r")[1], "start": val[0], "stop": val[1]})

    return final_closed_range_list, overlap_dict_open_range

def normalize(overlaps_file: dict):
    '''
    Deprecated, used with chom_draw function to scale down the values by a factor of 1,000,000 to fit them in the 
    canvas. Takes in the overlap dictionary returned by find_overlaps as an argument.
    '''
    normalized_overlaps = defaultdict(list)

    for i in CHRO_NAME:
        for ori in overlaps_file[i]:
            temp_scaled_val_bL = ((ori['bL'] - int(CHROMOSOME_LENGTHS[f'{i}']['bL']))/(int(CHROMOSOME_LENGTHS[f'{i}']['eL']) - int(CHROMOSOME_LENGTHS[f'{i}']['bL']))) * (int(CHROMOSOME_LENGTHS[f'{i}']['eL'].split('_')[0]) - int(CHROMOSOME_LENGTHS[f'{i}']['bL'])) + int(CHROMOSOME_LENGTHS[f'{i}']['bL'])
            if (ori['bL'] == ori['eL']):
                normalized_overlaps[i].append({'bL': temp_scaled_val_bL})
            else:
                temp_scaled_val_eL = ((ori['eL'] - int(CHROMOSOME_LENGTHS[f'{i}']['bL']))/(int(CHROMOSOME_LENGTHS[f'{i}']['eL']) - int(CHROMOSOME_LENGTHS[f'{i}']['bL']))) * (int(CHROMOSOME_LENGTHS[f'{i}']['eL'].split('_')[0]) - int(CHROMOSOME_LENGTHS[f'{i}']['bL'])) + int(CHROMOSOME_LENGTHS[f'{i}']['bL'])
                normalized_overlaps[i].append({'bL': temp_scaled_val_bL, 'eL': temp_scaled_val_eL})

    return normalized_overlaps

def plot_grph(overlap_dict: list, chr_num: str, virus_name_p: str):
    '''
    Takes in the list of individual chromosome overlap values found (eg: overlap_dictionary['chr1']), chromosome 
    number and the name of the virus as arguments and plots a scatter plot.
    '''
    fig,ax = plt.subplots()
    fig.suptitle(f'Overlapping Locations(Chromosome {chr_num}) {virus_name_p}')
    
    #linePlot with locations
    line = sns.scatterplot(x = overlap_dict, y = overlap_dict, marker = 'o')
    
    line.set_xlim(int(CHROMOSOME_LENGTHS[f'chr{chr_num}']['bL']), int(CHROMOSOME_LENGTHS[f'chr{chr_num}']['eL']))
    line.set_ylim(int(CHROMOSOME_LENGTHS[f'chr{chr_num}']['bL']), int(CHROMOSOME_LENGTHS[f'chr{chr_num}']['eL']))
    
    line.set_xlabel('VIS')
    line.set_ylabel('Mutations')
    
    plt.show()

def chromosome_draw(annot: list, chro_num: str, virus_name_p: str, is_HERVS: bool):
    '''
    Takes in the list of individual chromosome overlap values found (eg: overlap_dictionary['chr1']), chromosome 
    number and the name of the virus as arguments and returns a graphical representation of the chromosome with the 
    locations relative to the length of the chromosome.
    '''
    fig, ax = plt.subplots()

    color_select = ['#fe6507', '#042db3', '#57bf3c', '#f8cc16', '#6c2778']

    single_mutation = 'blue'
    ranged_mutation = 'red'

    ax.add_patch(plt.Rectangle((0, 45), int(CHROMOSOME_LENGTHS[f'chr{chro_num}']['eL']), 1, fc = '#414141'))
    
    starting_loc = int(CHROMOSOME_LENGTHS[f'chr{chro_num}']['bL'])
    ending_loc = int(CHROMOSOME_LENGTHS[f'chr{chro_num}']['eL'])

    ax.text(x = 0, y = 47, s = f'{starting_loc:.0f}', color = 'black', horizontalalignment = 'center')
    ax.text(x = ending_loc, y = 47, s = f'{ending_loc:.0f}', horizontalalignment = 'center')
    ax.text(x = int(CHROMOSOME_LENGTHS[f'chr{chro_num}']['eL'])/2, y = 55, s = f'Chromosome{chro_num}({virus_name_p})', horizontalalignment = 'center')
    
    if (not is_HERVS):
        count = 0
        for plot in annot:
            colors = color_select[count]
            if (count == len(color_select) - 1):
                count = 0
            else:
                count += 1

            if (len(plot) == 1):
                ax.plot([plot['bL'], plot['bL']], [43, 48], color = colors)
        
            elif (len(plot) == 2):
                ax.plot([plot['bL'], plot['bL']], [43, 48], color = ranged_mutation)
                ax.plot([plot['eL'], plot['eL']], [43, 48], color = ranged_mutation)

                ax.plot([plot['bL'], plot['eL']], [48, 48], color = ranged_mutation)
                ax.plot([plot['bL'], plot['eL']], [43, 43], color = ranged_mutation)

    else:
        for plots in annot:
            if (len(plots) == 1):
                ax.plot(plots['bL'], 48, "|r")
                ax.plot(plots['bL'], 43, "_g")
        
            elif (len(plots) == 2):
                ax.plot([plots['bL'], plots['bL']], [53, 48], color = ranged_mutation)
                ax.plot([plots['eL'], plots['eL']], [53, 48], color = ranged_mutation)

                ax.plot([plots['bL'], plots['eL']], [48, 48], color = ranged_mutation)
                ax.plot([plots['bL'], plots['eL']], [53, 53], color = ranged_mutation)

                ax.plot([plots['bL'], plots['eL']], [43, 43], color = "green")
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    plt.xlim(-10, int(CHROMOSOME_LENGTHS[f'chr{chro_num}']['eL']))
    plt.yticks([])    
    plt.ylim(-10, 100)

    ax.set_xlabel('Chromosome Length(BP)')

    plt.show()

#Displaying the common locations found along with the chromosome found in both files           
def display_overlap(final_overlap_list: list, chr_num: str):
    '''
    Takes in the list of individual chromosome overlap values found(eg: overlap_dictionary['chr1']), chromosome
    number as arguments and displays all the overlaps found.
    '''
    if (len(final_overlap_list) == 0):
        return 'No overlaps found!'
    else:
        print('\nDisplaying...')
        return f'Chromosome {chr_num} -> {final_overlap_list}'

def disp_inter(overlaps_p, overlaps_ranged_p, virus_name_p):
    '''
    Displays a command-line interface to view the found overlaps between the two given files. Takes in the non-ranged
    overlap dictionary, the ranged overlap dictionary, and the name of the virus as arguments.
    '''
    # print("Show overlaps for:")
    # for num, name in enumerate(CHRO_NAME, 1):
        # print(f"{num}. Chromosome {name.split('r')[1]}")

    # while (True):

    chr_to_show = input("Enter chromosome name: ")
    disp_nodup = display_overlap(overlaps_ranged_p[f'chr{chr_to_show}'], chr_to_show)

    if (disp_nodup != "No overlaps found!"):
        
        print(disp_nodup)
            # plot_grph(overlaps_ranged_p[f'chr{chr_to_show}'], chr_to_show, virus_name_p)
        chromosome_mapper(overlaps_p, virus_name_p)
            # chromosome_draw(overlaps_p[f'chr{chr_to_show}'],chr_to_show, virus_name_p, True)
        
        print('Exit(y/n): ')    
        ext = input()
        if (ext == 'y'):
            print('Quitting...')
            exit()    
    else:
        print(disp_nodup)

def run(file_path1: str, file_path2: str,  virus_name: str):
    '''
    The "No hassle" function, automatically does all the needed work and displays the command line interface. 
    Takes in the path of files to be compared and the name of the virus as arguments.
    '''
    overlaps_closed_ranged, overlaps_open_ranged = find_overlap(store_data(read_file(file_path1)), store_data(read_file(file_path2)))
    
    convert_json = input('Create json file of output: ')
    if (convert_json.lower() == 'y'):
        to_json(overlaps_closed_ranged, f"Overlaps_{Path(file_path1).stem}_{Path(file_path2).stem}")

    convert_ex = input('Create excel file of the output: ')
    if (convert_ex.lower() == 'y'):
        convert_excel(overlaps_closed_ranged, f"overlaps_{Path(file_path1).stem}_{Path(file_path2).stem}")

    disp_inter(overlaps_closed_ranged, overlaps_open_ranged, virus_name)

#DRIVER CODE
if (__name__ == '__main__'):
    
    path1 = input("Enter path for file 1: ")
    path2 = input("Enter path for file 2: ")
    vir_name = input("Enter name of Virus: ")
    
    df1 = read_file(path1)
    df2 = read_file(path2)

    stored_chrom1 = store_data(df1)
    stored_chrom2 = store_data(df2)

    closed_range_val, open_range_val = find_overlap(stored_chrom1, stored_chrom2)
    
    # to_json(closed_range_val, f"overlaps_{Path(path1).stem}_{Path(path2).stem}")
    # convert_excel(closed_range_val, f"overlaps_{Path(path1).stem}_{Path(path2).stem}")

    disp_inter(closed_range_val, open_range_val, vir_name)
