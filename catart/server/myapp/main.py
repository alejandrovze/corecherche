# myapp.py

from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, CustomJS, Slider, Div, Button, Paragraph, PointDrawTool, Select, FreehandDrawTool
from bokeh.plotting import figure, output_file, show, curdoc
from bokeh import events
from bokeh.themes import built_in_themes, Theme
from bokeh.io import curdoc
from pydub import AudioSegment
from pydub.playback import play
from pydub.silence import split_on_silence
import librosa
import numpy as np
import math
import sys
from aubio import source, pitch
import pandas as pd
import base64
import io
from bokeh.models.widgets import FileInput
import os
import time
from sklearn import preprocessing
import random
# PLAY WITH A NEW SONG 
splitNewSong = True
######################

number_of_colors = 20
random_color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(number_of_colors)]

output_file("contrast.html")
#curdoc().theme = 'contrast'
curdoc().theme = Theme(filename="myapp/theme.yaml")
audioAdress = 'myapp/static/data/'
win_s = 4096
hop_s = 512
tolerance = 0.8

feature_table = [np.array(['Filename', 'Spectral Centroid', 'Root Mean Square'])]

class SplitWavAudioMubin():
    def __init__(self, folder, filename, finalFolder):
        self.folder = folder
        self.filename = filename
        self.filepath = folder + filename
        self.finalFolder = finalFolder
        self.audio = AudioSegment.from_wav(self.filepath)
        self.arrayName = []
    
    def get_duration(self):
        return self.audio.duration_seconds
    
    def single_split(self, from_min, to_min, split_filename, diviseur):
        t1 = from_min  * 1000 // diviseur
        t2 = to_min  * 1000 // diviseur
        split_audio = self.audio[t1:t2]
        #os.remove(self.finalFolder + file_changment + split_filename)
        split_audio.export(self.finalFolder +split_filename, format="wav")
        
    def single_split_milli(self, split_filename, split_start):

        split_audio = self.audio[split_start:]
        #os.remove(self.finalFolder + file_changment + split_filename)
        split_audio.export(self.finalFolder +split_filename, format="wav")
        
    def multiple_split(self, sec_per_split, diviseur):
        total_mins = math.ceil(self.get_duration())
        for i in range(0, total_mins, sec_per_split):
            split_fn = str(i) + '_' + self.filename
            self.arrayName.append(split_fn)
            self.single_split(i, i+sec_per_split, split_fn, diviseur)
            print(str(i) + ' Done')
            if i == total_mins - sec_per_split:
                print('All splited successfully')  
                
    def multiple_split_milli(self, milli_time):
        total_mins = math.ceil(self.get_duration()) * 1000
        for i in range(0, total_mins, milli_time):
            split_fn = str(i) + '_' + self.filename
            self.arrayName.append(split_fn)
            self.single_split_milli (split_fn, i)
        print('Split Done')

                
if splitNewSong:
    audioAdress = 'myapp/static/split/'
    split_wav = SplitWavAudioMubin('myapp/static/', 'drum_sega1.wav', audioAdress)
    split_wav.multiple_split_milli(milli_time=200)
    twodtable = [np.array(['Filename', 'Spectral Centroid', 'Root Mean Square'])]
    for segSound in split_wav.arrayName:  
        y, sr = librosa.load(audioAdress + segSound)
        cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        meanCentroid = np.mean(cent)
        
        rms = librosa.feature.rms(y=y)
        meanRMS = np.mean(rms)
   
        
        twodtable.append(np.array([segSound, meanCentroid, meanRMS]))
    np.savetxt(audioAdress + 'scores_combined.txt', np.array(twodtable),fmt='%s', delimiter = "\t")
        
def set_carto(adresse):
    split_wav = SplitWavAudioMubin(audioAdress, adresse, audioAdress)
    split_wav.multiple_split_milli(milli_time=700)
    twodtable = []
    
    all_meanCentroid = []
    all_meanRMS = []
    
    for segSound in split_wav.arrayName:  
        y, sr = librosa.load(audioAdress + segSound)
        cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        meanCentroid = np.mean(cent)
        rms = librosa.feature.rms(y=y)
        meanRMS = np.mean(rms)
        
        all_meanCentroid.append(meanCentroid)
        all_meanRMS.append(meanRMS)
        
        #twodtable.append(np.array([segSound, meanCentroid, meanRMS]))

    all_meanCentroid = preprocessing.normalize([all_meanCentroid])[0]
    all_meanRMS = preprocessing.normalize([all_meanRMS])[0]
    
    for i in range(len(all_meanCentroid)):
        twodtable.append(np.array([split_wav.arrayName[i], all_meanCentroid[i], all_meanRMS[i]]))
    
    np.savetxt(audioAdress + 'scores_combined.txt', np.array(twodtable),fmt='%s', delimiter = "\t")
    return twodtable[:-1]

    
file_input = FileInput(accept="audio")    
dataFile = pd.read_csv(audioAdress + 'scores_combined.txt', sep="\t")
nameSound = dataFile.to_numpy()[:, 0]
x = dataFile.to_numpy()[:, 1]
y = dataFile.to_numpy()[:, 2]
state = ["False"]*len(x)
color= ["red"]*len(x)
fillalpha= [0.8]*len(x)

nameSound = []
x = []
y = []
state = []
color= []
fillalpha = []

def upload_song(attr,old,new):
    mytime = time.time()
    decoded = base64.b64decode(new)
    #os.remove(audioAdress+ 'temp.wav')
    wav_file = open(audioAdress + str(mytime) +'temp.wav', "wb")
    wav_file.write(decoded)
    
    set_carto(str(mytime)+'temp.wav')
    
    dataFile = pd.read_csv(audioAdress + 'scores_combined.txt', sep="\t")
    nameSound = dataFile.to_numpy()[:, 0]
    x = dataFile.to_numpy()[:, 1]
    y = dataFile.to_numpy()[:, 2]
    state = ["False"]*len(x)
    color= ["red"]*len(x)
    fillalpha = [0.8]*len(x)
    source2.data = {'x':[], 'y':[], 'color':[], 'state':[], 'nameSound':[], 'fillalpha':[]}
    source2.data = {'x':x, 'y':y, 'color':color, 'state':state, 'nameSound':nameSound, 'fillalpha':fillalpha}  
    
def upload_song_add(attr,old,new):
    mytime = time.time()
    decoded = base64.b64decode(new)
    #os.remove(audioAdress+ 'temp.wav')
    wav_file = open(audioAdress + str(mytime) +'temp.wav', "wb")
    wav_file.write(decoded)
    
    global feature_table
    feature_table = np.concatenate((feature_table,set_carto(str(mytime)+'temp.wav')))
    
    dataFile = pd.read_csv(audioAdress + 'scores_combined.txt', sep="\t", header=None)
    dataFile= dataFile[:-1]
    nameSound = dataFile.to_numpy()[:, 0]
    x = dataFile.to_numpy()[:, 1]
    y = dataFile.to_numpy()[:, 2]
    #remove last element often empty
    state = ["False"]*len(x)
    my_color= [random.choice(random_color)]*len(x)
    fillalpha=[0.8]*len(x)
    source2.data['x'] = np.concatenate((source2.data['x'], x))
    source2.data['y'] = np.concatenate((source2.data['y'], y))
    source2.data['color'] = np.concatenate((source2.data['color'], my_color))
    source2.data['state'] = np.concatenate((source2.data['state'], state))
    source2.data['nameSound'] = np.concatenate((source2.data['nameSound'], nameSound))
    source2.data['fillalpha'] = np.concatenate((source2.data['fillalpha'], fillalpha))
    

    
file_input = FileInput(accept="audio")
file_input.on_change('value', upload_song_add)

source2 = ColumnDataSource(data={'x':x, 'y':y, 'color':color, 'state':state, 'nameSound':nameSound, 'fillalpha':fillalpha})
source = ColumnDataSource({'x0': [], 'y0': [], 'x1': [], 'y1': []})
source3 = ColumnDataSource(dict(xs=[[0,0]], ys=[[0,0]]))


p = figure(width=1050, height=750, title='PyTart (beta)')


#source = ColumnDataSource({'x0': [], 'y0': [], 'x1': [], 'y1': []})
sr = p.segment(x0='x0', y0='y0', x1='x1', y1='y1', color='#D2CC1A', alpha=1, line_width=2, source=source, )
    
cr = p.circle('x', 'y', fill_color='color', size=5, alpha=1, hover_color='#ED553B', hover_alpha=1.0, source=source2)
glyph = cr.glyph
glyph.size = 20
glyph.fill_alpha = 0.8
glyph.line_color = "#ED553B"
glyph.line_width = 2

r = p.multi_line('xs', 'ys', source=source3)
draw_tool = FreehandDrawTool(renderers=[r])
p.add_tools(draw_tool)
p.toolbar.active_drag = draw_tool

point_tool = PointDrawTool(renderers=[cr])
p.add_tools(point_tool)
p.add_tools('lasso_select')
p.toolbar.active_tap = point_tool

p.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
p.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
p.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
p.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks
p.xaxis.major_label_text_font_size = '0pt'  # turn off x-axis tick labels
p.yaxis.major_label_text_font_size = '0pt'  # turn off y-axis tick labels

vol_slider = Slider(start=0, end=1, value=0.5, step=0.1, title="Volume")
len_slider = Slider(start=0, end=10, value=1, step=0.1, title="Max duration (in sec)")

selectX = Select(title="X representation:", value="Spectral Centroid", options=["Spectral Centroid", "Root Mean Square"])
selectY = Select(title="Y representation:", value="Root Mean Square", options=["Spectral Centroid", "Root Mean Square"])


div = Div(width=400, height=p.height, height_policy="fixed")
button = Button(label="Button", button_type="success")
layout = row(p, column(file_input, vol_slider,len_slider, selectX, selectY))



point_attributes = ['x', 'y', 'sx', 'sy'] 

code = """

const attrs = %s;
const data = {'x0': [], 'y0': [], 'x1': [], 'y1': []};

const x_cursor = Number(cb_obj[attrs[0]]).toFixed(10);
const y_cursor = Number(cb_obj[attrs[1]]).toFixed(10);

var dataCercle = source2.data;

var localX = 0;
var localY = 0;
var localMini = 1000.0;

var finalX = 0;
var finalY = 0;
var audioID = Number.MAX_SAFE_INTEGER;

const addr = audioAdresse

const lenValue = len.value;
const volslider = vol_slider.value;


    
for (let i = 0; i < circle.data.x.length; i++) {
    localX = circle.data.x[i]
    localY = circle.data.y[i]
    var localMiniBis = Math.hypot(Math.abs(x_cursor-localX), Math.abs(y_cursor-localY));
    
    if (localMiniBis < localMini){
        audioID = i;
        localMini = localMiniBis;
        finalX = localX;
        finalY = localY;
        
        dataCercle.fillalpha[i]=0.2 
        var el = Array.from(Array(circle.data.x.length).keys());
        delete el[i];
        for (const element of el) {
            dataCercle.fillalpha[element]=0.8;          
            }
        }    
    }
 
if (dataCercle.state[audioID] == "False" && dataCercle.fillalpha[audioID]==0.2){
    dataCercle.state[audioID] = "True";

    console.log(addr + dataCercle.nameSound[audioID])
    const player = new Pz.Sound(addr + dataCercle.nameSound[audioID], () => {
      player.volume = volslider;
      //player.sourceNode.playbackRate.value = PBrateslider1
      player.play();
    });

    setTimeout(function(){
        player.stop();
    }, lenValue*1000);

    }
var el = Array.from(Array(circle.data.x.length).keys());
delete el[audioID];
for (const element of el) {
    dataCercle.state[element]="False";          
    }
data['x0'].push(x_cursor);
data['y0'].push(y_cursor);
data['x1'].push(finalX);
data['y1'].push(finalY);

source2.change.emit();
segment.data = data;
""" % point_attributes

callback = CustomJS(args={'circle': cr.data_source, 'segment': sr.data_source, "div": div,  'source2':source2, 'audioAdresse':audioAdress,
'len':len_slider,
'vol_slider':vol_slider
}, code=code)

p.js_on_event(events.MouseMove, callback)
def modify_carto_X(valueX):
    if valueX == "Spectral Centroid":
        x = feature_table[:, 1]
    if valueX == "Root Mean Square":
        x = feature_table[:, 2]
    if x[0] == "Root Mean Square" or x[0] == "Spectral Centroid" :
        x = np.delete(x,0)
    xbis= []
    for i in x:
        xbis.append(np.float(i))
    source2.data['x'] = xbis
def modify_carto_Y(valueY):
    if valueY == "Spectral Centroid":
        y = feature_table[:, 1]
    if valueY == "Root Mean Square":
        y = feature_table[:, 2]
    if y[0] == "Root Mean Square" or y[0] == "Spectral Centroid" :
        y = np.delete(y,0)
    ybis= []
    for i in y:
        ybis.append(np.float(i))
    source2.data['y'] = ybis
    
def callback_X(attr,old,new):
    valueX = new
    print(valueX)
    modify_carto_X(valueX)
def callback_Y(attr,old,new):
    valueY = new
    modify_carto_Y(valueY)

selectX.on_change("value", callback_X)
selectY.on_change("value", callback_Y)


#show(layout)

curdoc().add_root(layout)