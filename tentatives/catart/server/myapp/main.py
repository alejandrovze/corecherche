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
# PLAY WITH A NEW SONG 
splitNewSong = False
######################


output_file("contrast.html")
#curdoc().theme = 'contrast'
curdoc().theme = Theme(filename="myapp/theme.yaml")

audioAdress = 'myapp/static/data/'

if splitNewSong:
    audioAdress = 'myapp/static/split/'
    song = AudioSegment.from_wav("myapp/static/music.wav")
    # spliting audio files
    audio_chunks = split_on_silence(song, min_silence_len=500, silence_thresh=-40 )
    #loop is used to iterate over the output list
    twodtable = ['Filename', 'FondFreq', 'Amplitude']
    for i, chunk in enumerate(audio_chunks):
        output_file = audioAdress+ "chunk{0}.wav".format(i)
        print("Exporting file", output_file)
        chunk.export(output_file, format="wav")
        y, sr = librosa.load(output_file)
        f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
        
        blockLinearRms= np.sqrt(np.mean(y**2)) # Linear value between 0 -> 1
        blockLogRms = 20 * math.log10(blockLinearRms) # Decibel (dB value) between 0 dB -> -inf dB
        twodtable.append(["chunk{0}.wav", f0, blockLogRms])
        np.savetxt('scores_combined.txt', twodtable)
        

import pandas as pd
dataFile = pd.read_csv(audioAdress + 'scores_combined.txt', sep="\t")
nameSound = dataFile.to_numpy()[:, 0]
x = dataFile.to_numpy()[:, 1]
y = dataFile.to_numpy()[:, 2]
state = ["False"]*len(x)
color= ["red"]*len(x)


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
paraDisto = Div(text="""<b>Distortion</b>""", height=20, align="center")
disto_slider1 = Slider(start=0, end=1, value=0, step=0.1, title="Gain")
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
layout = row(p, column(vol_slider,len_slider,paraDelay,delay_slider1,delay_slider2,delay_slider3,paraDisto,disto_slider1,paraRev,rev_slider1,rev_slider2,paraTrem,trem_slider1,trem_slider2,paraLp,lp_slider1,lp_slider2))

#source = ColumnDataSource({'x0': [], 'y0': [], 'x1': [], 'y1': []})
sr = p.segment(x0='x0', y0='y0', x1='x1', y1='y1', color='#D2CC1A', alpha=1, line_width=3, source=source, )
    
cr = p.circle('x', 'y', fill_color='color', size=30, alpha=1, hover_color='#ED553B', hover_alpha=1.0, source=source2)
glyph = cr.glyph
glyph.size = 60
glyph.fill_alpha = 0.8
glyph.line_color = "#ED553B"
#glyph.line_dash = [6, 3]
glyph.line_width = 2


varSong = 10


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

const lenValue = len.value;
const volslider = vol_slider.value;
const delayslider1 = delay_slider1.value;
const delayslider2 = delay_slider2.value;
const delayslider3 = delay_slider3.value;
const distoslider1 = disto_slider1.value;
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
    
    var distortion = new Pizzicato.Effects.Distortion({
        gain: distoslider1
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
    
    const player = new Pz.Sound('myapp/static/data/'+ dataCercle.nameSound[audioID], () => {
      player.addEffect(delay);
      player.addEffect(distortion);
      player.addEffect(reverb);
      player.addEffect(tremolo);
      player.addEffect(lowPassFilter);
      player.volume = volslider;
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

varSong = audioID;
source2.change.emit();
segment.data = data;
""" % point_attributes


#p.js_on_event(events.MouseMove, display_event(div, attributes=point_attributes))

callback = CustomJS(args={'circle': cr.data_source, 'segment': sr.data_source, "div": div, 'varSong':varSong, 'source2':source2,
'len':len_slider,
'vol_slider':vol_slider,
'delay_slider1':delay_slider1,
'delay_slider2':delay_slider2,
'delay_slider3':delay_slider3,
'disto_slider1':disto_slider1,
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

