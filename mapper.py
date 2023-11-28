import dash_bio as dashbio
import dash
import pandas as pd

from dash import html

app = dash.Dash(__name__)

data = pd.read_excel('./output1.xlsx')
data = data.dropna()
data_list = []

for k in data.itertuples():
    data_list.append({"chr": f"{k[1]}", "start": int(k[2]), "stop": int(k[3])})

ch = []
for i in data_list:
    if (i['chr'] == '4') or (i['chr'] == '8') or (i['chr'] == '9') or (i['chr'] == '14') or (i['chr'] == '21') or (i['chr'] == 'Y'):
        if i['chr'] == '4':
            if i['start'] <= 190214555:
                ch.append(i)
            else:
                print(f"'chr':{i['chr']}, 'start':{i['start']}, 'stop': {i['start']}")
                # ch_out_of_bounds.append({'chr': i['chr'], 'start': i['start'], 'stop': i['stop']})
        if i['chr'] == '8':
            if i['start'] <= 145138636:
                ch.append(i)
            else:
                print(f"'chr':{i['chr']}, 'start':{i['start']}, 'stop': {i['start']}")
                # ch_out_of_bounds.append({"chr": i["chr"], "start": i['start'], "stop": i['stop']})
        if i['chr'] == '9':
            if i['start'] <= 138394717:
                ch.append(i)
            else:
                print(f"'chr':{i['chr']}, 'start':{i['start']}, 'stop': {i['start']}")
                # ch_out_of_bounds.append({"chr": i["chr"], "start": i['start'], "stop": i['stop']})
        if i['chr'] == '14':
            if i['start'] <= 107043718:
                ch.append(i)
            else:
                print(f"'chr':{i['chr']}, 'start':{i['start']}, 'stop': {i['start']}")
                # ch_out_of_bounds.append({"chr": i["chr"], "start": i['start'], "stop": i['stop']})
        if i['chr'] == '21':
            if i['start'] <= 46709983:
                ch.append(i)
            else:
                print(f"'chr':{i['chr']}, 'start':{i['start']}, 'stop': {i['start']}")
                # ch_out_of_bounds.append({"chr": i['chr'], "start": i['start'], "stop": i['stop']})
        if i['chr'] == 'Y':
            if i['start'] <= 57227415:
                ch.append(i)
            else:
                print(f"'chr':{i['chr']}, 'start':{i['start']}, 'stop': {i['start']}")
                # ch_out_of_bounds.append({"chr": i["chr"], "start": i['start'], "stop": i['stop']})
    else:    
        ch.append(i)


annots = [
{
"chr": "1",
"start": 79337872,
"stop": 79346600
},
{
"chr": "1",
"start": 80097404,
"stop": 80103638
},
{
"chr": "1",
"start": 85068775,
"stop": 85078397
},
{
"chr": "1",
"start": 92128008,
"stop": 92136304
},
{
"chr": "1",
"start": 112638945,
"stop": 112645195
},
{
"chr": "1",
"start": 118357956,
"stop": 118364632
},
{
"chr": "3",
"start": 22065421,
"stop": 22071833
},
{
"chr": "3",
"start": 36403312,
"stop": 36410924
},
{
"chr": "3",
"start": 37410049,
"stop": 37420469
},
{
"chr": "3",
"start": 86157064,
"stop": 86167045
},
{
"chr": "5",
"start": 80587671,
"stop": 80588293
},
{
"chr": "5",
"start": 100943040,
"stop": 100951127
},
{
"chr": "5",
"start": 118033370,
"stop": 118040152
},
{
"chr": "11",
"start": 106040657,
"stop": 106050454
},
{
"chr": "11",
"start": 118165941,
"stop": 118173118
},
{
"chr": "11",
"start": 130198757,
"stop": 130210960
},
{
"chr": "13",
"start": 53916842,
"stop": 53921124
},
{
"chr": "13",
"start": 62096909,
"stop": 62101216
},
{
"chr": "13",
"start": 82860096,
"stop": 82868882
},
{
"chr": "13",
"start": 83802486,
"stop": 83807276
},
{
"chr": "13",
"start": 87409519,
"stop": 87418176,
}
]

chrom = set(i['chr'] for i in ch)
# print(chrom)
app.layout = html.Div(style = {"textAlign": "center"}, children = [
    'Chromosome overlap viewer',
    
    dashbio.Ideogram(
        id = 'chromosome_mapper',
        orientation = 'horizontal',
        chrHeight = 1200,
        chrWidth = 25,
        rotatable = False,
        chromosomes = list(chrom),
        annotations = ch,
        showBandLabels = True,
        annotationsLayout = "tracks",
        annotationHeight = 5,
    ),
    html.Div(id='my-default-ideogram-rotated')
])

if __name__ == '__main__':
    app.run_server(debug=True)
