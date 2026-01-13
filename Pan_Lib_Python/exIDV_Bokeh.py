# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
@date:2022/04/26
@author: A108222040
@subject:
"""

import os,sys
outputPath = os.path.join("..","Output")
InputPath = os.path.join("..","Input")
imagePath = os.path.join("..","Image")
LibPath = os.path.join("Python")

###import packages
import numpy as np

import random
from bokeh.plotting import curdoc, figure, output_file, show 
from bokeh.models import CustomJS, ColumnDataSource
from bokeh.models import Slider, RangeSlider, Spinner, Div, Button

from bokeh.layouts import row, column, gridplot, layout
from bokeh.palettes import RdYlBu3


###Codes
fileNamePre = outputPath + "/bokehIDV_"
#Methods
#---Line
def case1():
    output_file(fileNamePre + "line.html")
    p = figure(width=400, height=300, title="Line")
    p.line([1,2,3,4,5],[5,4,3,2,1])
    show(p)
    
def case2():
    output_file(fileNamePre + "circle.html")
    p = figure(width=400, height=300, title="Circle")
    p.circle([1,2,3],[2,5,3],size=[10,20,30],color=["pink","olive","gold"])
    show(p)
     
#Q1 add two more figure let them be 2 in row1, 3 in row 2
def case3():
    output_file(fileNamePre + "circle.html")
    s1 = figure(width=250, height=250, title="Fig.1: Circle")
    s1.circle([1,2,3,4],[1,2,3,4],size=10,color=["pink","olive","gold","red"])
    
    s2 = figure(width=250, height=250, x_range=s1.x_range, title="Fig.2: Trangle")
    s2.triangle([1,2,3,4],[4,2,1,3],size=10,color=["pink","olive","gold","red"])
    
    s3 = figure(width=250, height=250, x_range=s1.x_range, title="Fig.3: Square")
    s3.square([1,2,3,4],[3,2,1,4],size=10,color=["pink","olive","gold","red"])
    
    s4 = figure(width=250, height=250, x_range=s1.x_range, title="Fig.4: Diamond")
    s4.diamond([1,2,3,4],[2,1,3,4],size=10,color=["pink","olive","gold","red"])
    
    s5 = figure(width=250, height=250, x_range=s1.x_range, title="Fig.5: Star")
    s5.star([1,2,3,4],[3,2,1,4],size=10,color=["pink","olive","gold","red"])
    
    p = gridplot([[s1,s2],[s3,s4,s5]], toolbar_location=None)
    show(p)
    
def case4():
    output_file(fileNamePre + "slider.html")
    p = figure(width=400, height=300, title="Slider")
    p.line([1,2,3,4,5],[5,4,3,2,1])
    slide = Slider(start=1, end=5, step=1, value=3, width=400)
    layout = column(p, slide)
    show(layout)
    
#Q2 : change line color in figure, turn off toolbar    
def case5():
    x = np.linspace(0, 10, 500)
    y = np.sin(x)
    source = ColumnDataSource(data=dict(x=x, y=y))
    
    #line figure
    pp = figure(y_range=(-10, 10), plot_width=400, plot_height=400, title="Slider Demo", toolbar_location=None)
    pp.line('x', 'y', source=source, line_width=3, line_alpha=0.6, color= '#ff0000')
    
    #Slider
    amp_slider = Slider(start=0.1, end=10, value=1, step=.1, title="Amplitude",bar_color = '#ff0000', height_policy = 'fit')
    freq_slider = Slider(start=0.1, end=10, value=1, step=.1, title="Frequency",bar_color = '#ff0000', height=60)
    phase_slider = Slider(start=0, end=6.4, value=0, step=.1, title="Phase",bar_color = '#ff0000', height=90)
    offset_slider = Slider(start=-5, end=5, value=0, step=.1, title="Offset",bar_color = '#ff0000', height=120)
    
    #slider event handler
    callback = CustomJS(args=dict(source=source, amp=amp_slider, freq=freq_slider, phase=phase_slider, offset=offset_slider),
                        code="""
                        const data = source.data;
                        const A = amp.value;
                        const k = freq.value;
                        const phi = phase.value;
                        const B = offset.value;
                        const x = data['x']
                        const y = data['y']
                        for (var i = 0; i <x.length; i++){
                                y[i] = B + A*Math.sin(k*x[i]+phi);
                        }
                        source.change.emit()
                        """)
    
    #set slider event
    amp_slider.js_on_change('value', callback)
    freq_slider.js_on_change('value', callback)
    phase_slider.js_on_change('value', callback)
    offset_slider.js_on_change('value', callback)
    
    #output
    layout = row(pp,
                 column(amp_slider, freq_slider, phase_slider, offset_slider))
    output_file(fileNamePre + "JScallback_slider.html", title="Slider Example")
    show(layout)

#Q3 data randomly generate 1~10 integer for x
#                          -100~100 integer for y
def case7():
    x = [random.randint(1, 10) for p in range(0, 10)]
    y = [random.randint(-100, 100) for i in range(0, 10)]
    
    #x = [random.randint(1, 10) for p in range(0, 10)]
    #y = [random.randint(-100, 100) for i in range(0, 10)]
    

    pp = figure(x_range=(1, 9), width=500, height=250, title="Spinner_Slider Example")
    points = pp.circle(x=x, y=y, size=30, fill_color="#ff55df")

    #set up
    div = Div(text="""<p>Select the circle's size using this control element:</p>""",
              width=200, height=30,)
    
    #set up spinner
    spinner = Spinner(title="Circle size",
                      low=0,
                      high=60,
                      step=5,
                      value=points.glyph.size,
                      width=200,)
    spinner.js_link("value", points.glyph, "size")
    
    #set up RangeSlider
    range_slider = RangeSlider(title="Adjust x-axis range",
                               start=0,
                               end=10,
                               step=1,
                               value=(pp.x_range.start, pp.x_range.end),)
    range_slider.js_link("value", pp.x_range, "start", attr_selector=0)
    range_slider.js_link("value", pp.x_range, "end", attr_selector=1)
    
    #result
    resultPlot = layout([[div, spinner],
                         [range_slider],
                         [pp]])
    output_file(fileNamePre + "spinner_slider.html")
    show(resultPlot)

from bokeh.sampledata.iris import flowers
def case8():
    colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
    colors = [colormap[x] for x in flowers['species']]
    
    pp = figure(title="Iris Morphology")
    pp.xaxis.axis_label = 'Pental Length'
    pp.yaxis.axis_label = 'Pental Width'
    
    pp.scatter(flowers["petal_length"], flowers["petal_width"],
               color=colors, fill_alpha=0.2, size=10)
    
    show(pp)

if (__name__ == "__main__"):
    #case1()
    #case2()
    case3()
    case4()
    case5()
    case7()
    #case8()