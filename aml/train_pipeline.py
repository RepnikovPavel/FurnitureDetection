import os
from typing import Dict,List,Any,Tuple
import plotly
import plotly.graph_objects as go
import numpy as np
import webbrowser

import plotly
from plotly.io._base_renderers import BaseHTTPRequestHandler, HTTPServer


def DictToListOfPairs(dict:Dict[str,Any])->List[Tuple[str,Any]]:
    # input: key-value table 
    # output: array of pairs <key,value>
    out_=  []
    for k,v in dict.items():
        out_.append((k,v))
    return out_

def BatchMaker(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]



def init_figure(x_label='batch index',y_label='loss'):
    plotly.io.templates.default = 'plotly_dark'
    fig = go.Figure(
            layout=go.Layout(
            # title="",
            xaxis_title=x_label,
            yaxis_title=y_label,
            # xaxis=dict(rangeslider=dict(visible=True)), # add slider
            # width=1900, height=4000
            # margin=dict(
            #     l=0,
            #     r=0,
            #     b=0,
            #     t=0,
            #     pad=4
            # ),
        ))
    return fig

def save_fig_to_html(fig, path, filename):

    if not os.path.exists(path):
        os.makedirs(path)

    fig.write_html(os.path.join(path,filename))

def add_line_to_fig(fig, x:np.array, y: np.array, line_name,mode='markers',line_style=None):
    '''
        mode: 'lines+markers','lines','markers'
    '''
    number_of_points = len(y)
    target_number_of_points = min(1000, number_of_points)
    step_ = int(number_of_points / target_number_of_points)
    fig.add_trace(go.Scatter(x=x[::step_],
                             y=y[::step_],
                             name=line_name,
                             fill=None,
                             line=dict(width=4, dash=line_style),
                             mode=mode
                             )
                  )