# myapp.py

from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, CustomJS, Slider, Div, Button, Paragraph
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

# PLAY WITH A NEW SONG 
splitNewSong = True
######################


output_file("contrast.html")
#curdoc().theme = 'contrast'
curdoc().theme = Theme(filename="myapp/theme.yaml")

audioAdress = 'myapp/static/data/'

win_s = 4096
hop_s = 512
tolerance = 0.8

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
    
    def single_split(self, from_min, to_min, split_filename):
        t1 = from_min  * 1000
        t2 = to_min  * 1000
        split_audio = self.audio[t1:t2]
        split_audio.export(self.finalFolder + split_filename, format="wav")
        
    def multiple_split(self, sec_per_split):
        total_mins = math.ceil(self.get_duration())
        for i in range(0, total_mins, sec_per_split):
            split_fn = str(i) + '_' + self.filename
            self.arrayName.append(split_fn)
            self.single_split(i, i+sec_per_split, split_fn)
            print(str(i) + ' Done')
            if i == total_mins - sec_per_split:
                print('All splited successfully')


                
                
if splitNewSong:
    audioAdress = 'myapp/static/split/'
    split_wav = SplitWavAudioMubin('myapp/static/', 'drum_sega1.wav', audioAdress)
    split_wav.multiple_split(sec_per_split=1)
    twodtable = [np.array(['Filename', 'FondFreq', 'Amplitude'])]
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
    split_wav.multiple_split(sec_per_split=1)
    twodtable = [np.array(['Filename', 'FondFreq', 'Amplitude'])]
    for segSound in split_wav.arrayName:  
        y, sr = librosa.load(audioAdress + segSound)
        cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        meanCentroid = np.mean(cent)
        
        rms = librosa.feature.rms(y=y)
        meanRMS = np.mean(rms)
   
        
        twodtable.append(np.array([segSound, meanCentroid, meanRMS]))
    np.savetxt(audioAdress + 'scores_combined.txt', np.array(twodtable),fmt='%s', delimiter = "\t")
    
        
dataFile = pd.read_csv(audioAdress + 'scores_combined.txt', sep="\t")
nameSound = dataFile.to_numpy()[:, 0]
x = dataFile.to_numpy()[:, 1]
y = dataFile.to_numpy()[:, 2]
state = ["False"]*len(x)
color= ["red"]*len(x)

def upload_song(attr,old,new):
    decoded = base64.b64decode(new)
    wav_file = open(audioAdress+ 'temp.wav', "wb")
    wav_file.write(decoded)
    
    set_carto('temp.wav')
    
    dataFile = pd.read_csv(audioAdress + 'scores_combined.txt', sep="\t")
    nameSound = dataFile.to_numpy()[:, 0]
    x = dataFile.to_numpy()[:, 1]
    y = dataFile.to_numpy()[:, 2]
    state = ["False"]*len(x)
    color= ["red"]*len(x)
        
    source2.data = dict(x=x, y=y, color=color, state=state, nameSound=nameSound)
    
    

file_input = FileInput(accept="audio")
file_input.on_change('value', upload_song)

source2 = ColumnDataSource(data=dict(x=x, y=y, color=color, state=state, nameSound=nameSound))
source = ColumnDataSource({'x0': [], 'y0': [], 'x1': [], 'y1': []})



p = figure(width=1050, height=750, tools="pan,wheel_zoom,zoom_in,zoom_out,reset", title='PyTart (beta)')

p.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
p.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks

p.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
p.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks

p.xaxis.major_label_text_font_size = '0pt'  # turn off x-axis tick labels
p.yaxis.major_label_text_font_size = '0pt'  # turn off y-axis tick labels

vol_slider = Slider(start=0, end=1, value=0.5, step=0.1, title="Volume")
len_slider = Slider(start=0, end=10, value=1, step=0.1, title="Max duration (in sec)")
paraDelay = Div(text="""<b>Delay</b>""", height=20, align="center")
delay_slider1 = Slider(start=0, end=1, value=0.6, step=0.1, title="Feedback")
delay_slider2 = Slider(start=0, end=1, value=0.4, step=0.1, title="Time")
delay_slider3 = Slider(start=0, end=1, value=0, step=0.1, title="Mix")
paraPBrate = Div(text="""<b>Playback rate</b>""", height=20, align="center")
PBrate_slider1 = Slider(start=0.1, end=10, value=1, step=0.1, title="Gain")
paraRev = Div(text="""<b>Reverb</b>""", height=20, align="center")
rev_slider1 = Slider(start=0, end=1, value=0.01, step=0.01, title="Time")
rev_slider2 = Slider(start=0, end=1, value=0, step=0.1, title="Mix")
paraTrem = Div(text="""<b>Tremolo</b>""", height=20, align="center")
trem_slider1 = Slider(start=0, end=20, value=7, step=1, title="Speed")
trem_slider2 = Slider(start=0, end=1, value=0, step=0.1, title="Mix")
paraLp = Div(text="""<b>Low-pass filter</b>""", height=20, align="center")
lp_slider1 = Slider(start=10, end=22050, value=22000, step=1, title="Frequency")
lp_slider2 = Slider(start=0.01, end=50, value=10, step=0.01, title="Peak")



div = Div(width=400, height=p.height, height_policy="fixed")
button = Button(label="Button", button_type="success")
layout = row(p, column(file_input, vol_slider,len_slider,paraDelay,delay_slider1,delay_slider2,delay_slider3,paraPBrate,PBrate_slider1,paraRev,rev_slider1,rev_slider2,paraTrem,trem_slider1,trem_slider2,paraLp,lp_slider1))

#source = ColumnDataSource({'x0': [], 'y0': [], 'x1': [], 'y1': []})
sr = p.segment(x0='x0', y0='y0', x1='x1', y1='y1', color='#D2CC1A', alpha=1, line_width=3, source=source, )
    
cr = p.circle('x', 'y', fill_color='color', size=30, alpha=1, hover_color='#ED553B', hover_alpha=1.0, source=source2)
glyph = cr.glyph
glyph.size = 60
glyph.fill_alpha = 0.8
glyph.line_color = "#ED553B"
#glyph.line_dash = [6, 3]
glyph.line_width = 2




point_attributes = ['x', 'y', 'sx', 'sy'] 


code = """

const attrs = %s;
const data = {'x0': [], 'y0': [], 'x1': [], 'y1': []};

const x_cursor = Number(cb_obj[attrs[0]]).toFixed(2);
const y_cursor = Number(cb_obj[attrs[1]]).toFixed(2);

var dataCercle = source2.data;

var localX = 0;
var localY = 0;
var localMini = Number.MAX_SAFE_INTEGER;

var finalX = 0;
var finalY = 0;
var audioID = Number.MAX_SAFE_INTEGER;

const addr = audioAdresse

const lenValue = len.value;
const volslider = vol_slider.value;
const delayslider1 = delay_slider1.value;
const delayslider2 = delay_slider2.value;
const delayslider3 = delay_slider3.value;
const PBrateslider1 = PBrate_slider1.value;
const revslider1 = rev_slider1.value;
const revslider2 = rev_slider2.value;
const tremslider1 = trem_slider1.value;
const tremslider2 = trem_slider2.value;
const lpslider1 = lp_slider1.value;
const lpslider2 = lp_slider2.value;
    
for (let i = 0; i < circle.data.x.length; i++) {
    localX = circle.data.x[i]
    localY = circle.data.y[i]
    
    var localMiniBis = Math.sqrt( Math.pow((x_cursor-localX), 2) + Math.pow((y_cursor-localY), 2) );
    
    if (localMiniBis < localMini){
        audioID = i;
        localMini = localMiniBis;
        finalX = localX;
        finalY = localY;
        
        dataCercle.color[i]='#D2CC1A' 
        var el = Array.from(Array(circle.data.x.length).keys());
        delete el[i];
        for (const element of el) {
            dataCercle.color[element]='#ED553B';          
            }
        }    
    }
 
if (dataCercle.state[audioID] == "False" && dataCercle.color[audioID]=='#D2CC1A'){
    dataCercle.state[audioID] = "True";
    
    var delay = new Pizzicato.Effects.Delay({
        feedback: delayslider1,
        time: delayslider2,
        mix: delayslider3
    });
    
    
    var reverb = new Pizzicato.Effects.Reverb({
        time: revslider1,
        decay: 0.01,
        reverse: false,
        mix: revslider2
    });
    
    var tremolo = new Pizzicato.Effects.Tremolo({
        speed: tremslider1,
        depth: 0.8,
        mix: tremslider2
    });
    
    var lowPassFilter = new Pizzicato.Effects.LowPassFilter({
        frequency: lpslider1,
        peak: lpslider2
    });
    
    const player = new Pz.Sound(addr + dataCercle.nameSound[audioID], () => {
      player.addEffect(delay);
      player.addEffect(reverb);
      player.addEffect(tremolo);
      player.addEffect(lowPassFilter);
      player.volume = volslider;
      //player.sourceNode.playbackRate.value = PBrateslider1
      player.play();
    });

    setTimeout(function(){
        player.pause();
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


#p.js_on_event(events.MouseMove, display_event(div, attributes=point_attributes))

callback = CustomJS(args={'circle': cr.data_source, 'segment': sr.data_source, "div": div,  'source2':source2, 'audioAdresse':audioAdress,
'len':len_slider,
'vol_slider':vol_slider,
'delay_slider1':delay_slider1,
'delay_slider2':delay_slider2,
'delay_slider3':delay_slider3,
'PBrate_slider1':PBrate_slider1,
'rev_slider1':rev_slider1,
'rev_slider2':rev_slider2,
'trem_slider1':trem_slider1,
'trem_slider2':trem_slider2,
'lp_slider1':lp_slider1,
'lp_slider2':lp_slider2 }, code=code)

def callback2(event):
    el = source2.color.index("yellow")
    print("Indice")
    print(el)
    if source2.state[el] == "False":
        source2.state[el] = "True"
        play(song)
        print("YOOO")

        
#p.on_event(events.MouseMove, callback3)
p.js_on_event(events.MouseMove, callback)
#len_slider.js_on_change('value', callback)


show(layout)
#from bokeh.embed import json_item
#from bokeh.resources import CDN
#import json
#item_text = json.dumps(json_item(layout, "myplot"))


curdoc().add_root(layout)

