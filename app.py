import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import datetime
import subprocess

# Load the data
f1 = "log_txps.txt"
f2 = "sys_load_cpu_ram_io.txt"
f3 = "log_proptime.txt"
f4 = "sys_load_net.txt"
f5 = "sys_load_store.txt"
f6 = "sys_load_net_testnet3_boot.txt"


with open(f1) as file:
    lines = file.readlines()
    lines = [line.rstrip().split(" ") for line in lines]
    
    
    
def ma(x, w=10):
    if w == 1:
        return x
    c = np.convolve(x, np.ones(w), 'same') / w
    c[:w] = np.mean(x[:w])
    c[-w:] = np.mean(x[-w:])
    return list(c)
    

t = [int(float(line[0].replace('\x00',''))) for line in lines]



cycles = [int(line[3]) for line in lines]
stakers = [int(line[4]) for line in lines]
print("max stakers", max(stakers))
rolls = [int(line[5]) for line in lines]
bps = [float(line[6]) for line in lines]
txps = [int(line[7]) for line in lines]
peers = [int(line[8]) for line in lines if len(line)>8]



ma_size = 4

with open(f2) as file:
    lines = file.readlines()
    lines = [line.rstrip().split() for line in lines if line[0] != "#"]


t2 = [int(lines[i][0]) for i in range(len(lines)-1) if len(lines[i])==1 and not len(lines[i+1])==1]
cpus = [float(lines[i][7].replace(",", ".")) for i in range(len(lines)-1) if len(lines[i])>8 and len(lines[i+1])==1][:len(t2)]
rams = [float(lines[i][13].replace(",", ".")) for i in range(len(lines)-1) if len(lines[i])>8 and len(lines[i+1])==1][:len(t2)]
ios = [float(lines[i][17].replace(",", ".")) for i in range(len(lines)-1) if len(lines[i])>8 and len(lines[i+1])==1][:len(t2)]

t2 = t2[-len(cpus):]



with open(f3) as file:
    lines = file.readlines()
    lines = [line.rstrip().split() for line in lines]

t3 = [int(line[0].replace('\x00','')) for line in lines]
prop_mean_h = [int(line[5]) for line in lines]
prop_mean_b = [int(line[9]) for line in lines]



def mega(boot):
    if boot[-2] == "G":    
        return float(boot[:-2].replace(",", "."))*1000
    elif boot[-2] == "M":    
        return float(boot[:-2].replace(",", "."))
    elif boot[-2] == "K":    
        return float(boot[:-2].replace(",", "."))/1000
    else:
        return float(boot[:-1].replace(",", "."))/1000

with open(f4) as file:
    lines = file.readlines()
    lines = [line.rstrip().split() for line in lines]

t4 = [int(line[0].replace('\x00','')) for line in lines if line and line[0].replace('\x00','').isdigit()]
up_bandwidths = [mega(line[2]) for line in lines if len(line) > 1]
down_bandwidths = [mega(line[3]) for line in lines if len(line) > 1]
bandwidths = [mega(line[4]) for line in lines if len(line) > 1]



with open(f6) as file:
    lines = file.readlines()
    lines = [line.rstrip().split() for line in lines]

t6 = [int(line[0].replace('\x00','')) for line in lines if line and line[0].replace('\x00','').isdigit()]
boot_bandwidths = [mega(line[2]) for line in lines if len(line) > 1]



with open(f5) as file:
    lines = file.readlines()
    lines = [line.rstrip().split() for line in lines]
t5 = [int(line[0]) for line in lines if line and len(line)== 1]
storage = []
for line in lines:
    if len(line) == 1:
        storage.append(0)
    else:
        storage[-1] = storage[-1] + int(line[0])
        
storage = storage[:len(t5)]

t = [datetime.datetime.fromtimestamp(ts) for ts in t]
t2 = [datetime.datetime.fromtimestamp(ts) for ts in t2]
t3 = [datetime.datetime.fromtimestamp(ts) for ts in t3]
t4 = [datetime.datetime.fromtimestamp(ts) for ts in t4]
t5 = [datetime.datetime.fromtimestamp(ts) for ts in t5]
t6 = [datetime.datetime.fromtimestamp(ts) for ts in t6]
# Create the Dash app
app = dash.Dash()
server = app.server
# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children='Massa Dashboard'),
    
    html.Div(children='''
        Stakers and Transaction Rate
    '''),
    
    dcc.Graph(
        id='stakers-graph',
        figure={
            'data': [
                go.Scatter(
                    x=t,
                    y=stakers,
                    mode='lines',
                    name='Stakers'
                ),
                go.Scatter(
                    x=t,
                    y=ma(txps, ma_size),
                    mode='lines',
                    name='Transactions/sec'
                ),
            ],
            'layout': go.Layout(
                xaxis={'title': 'Time'},
                yaxis={'title': 'Number of Stakers or Transactions/sec'},
                margin={'l': 50, 'b': 50, 't': 50, 'r': 50},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    ),

    html.Div(children='''
        CPU Usage rate
    '''),
    
    dcc.Graph(
        id='cpu-graph',
        figure={
            'data': [
                go.Scatter(
                    x=t2,
                    y=ma(cpus, ma_size),
                    mode='lines',
                    fill='tozeroy',
                    name='Cpu Usage',
                    hovertemplate='%{x|%Y-%m-%d %H:%M:%S}: %{y:.2f} %'
                ),
            ],
            'layout': go.Layout(
            title='CPU Usage',
            xaxis={'title': 'Time'},
            yaxis={'title': 'CPU Usage (%)'}
        )
    }
    ),

    html.Div(children='''
        RAM Usage
    '''),
    
    dcc.Graph(
        id='ram-graph',
        figure={
            'data': [
                go.Scatter(
                    x=t4[-len(bandwidths):],
                    y=[8*b/60 for b in ma(down_bandwidths, ma_size)],
                    mode='lines',
                    fill='tozeroy',
                    name='RAM usage',
                    hovertemplate='%{x|%Y-%m-%d %H:%M:%S}: %{y:.2f} GB'
                ),
            ],
            'layout': go.Layout(
            title='Current RAM Usage:',
            xaxis={'title': 'Time'},
            yaxis={'title': 'Current RAM Usage (GB):'}
        )
    }
    ),

    html.Div(children='''
        Average Block Propagation Time
    '''),
    
    dcc.Graph(
        id='block-prop-graph',
        figure={
            'data': [
                    go.Scatter(
                    x=t3,
                    y=ma(prop_mean_b, ma_size),
                    mode='lines',
                    name='Avg Block Prop Time (ms)',
                    hovertemplate='%{x|%Y-%m-%d %H:%M:%S}: %{y:.2f} ms'
                ),
            ],
           'layout': go.Layout(
                xaxis={'title': 'Time'},
                yaxis={'title': 'Avg Block Prop Time (ms)'},
                margin={'l': 50, 'b': 50, 't': 50, 'r': 50},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
        )
    }
    ),
    
    html.Div(children='''
        Average Header Propagation Time
    '''),
    
    dcc.Graph(
        id='header-prop-graph',
        figure={
            'data': [
                go.Scatter(
                    x=t3,
                    y=ma(prop_mean_h, ma_size),
                    mode='lines',
                    name='Avg Header Prop Time (ms)',
                    hovertemplate='%{x|%Y-%m-%d %H:%M:%S}: %{y:.2f} ms'
                ),
            ],
            'layout': go.Layout(
                xaxis={'title': 'Time'},
                yaxis={'title': 'Avg Header Prop Time (ms)'},
                margin={'l': 50, 'b': 50, 't': 50, 'r': 50},
                legend={'x': 0, 'y': 1}
            )
        }
    ),

    html.Div(children='''
        Current IO Usage
    '''),
    
    dcc.Graph(
        id='io-graph',
        figure={
            'data': [
                go.Scatter(
                    x=t2,
                    y=ma(ios, ma_size),
                    mode='lines',
                    name='IO Usage',
                    hovertemplate='%{x|%Y-%m-%d %H:%M:%S}: %{y:.2f} kB/s'
                ),
            ],
            'layout': go.Layout(
            title='IO Usage (kB/s)',
            xaxis={'title': 'Time'},
            yaxis={'title': 'IO Usage (kB/s)'}
        )
    }
    ),

    html.Div(children='''
        Storage
    '''),
    
    dcc.Graph(
        id='Storage-graph',
        figure={
            'data': [
                go.Scatter(
                    x=t5[-len(storage):],
                    y=[s/1000 for s in storage],
                    mode='lines',
                    name='Storage',
                    hovertemplate='%{x|%Y-%m-%d %H:%M:%S}: %{y:.2f} MB'
                ),
            ],
            'layout': go.Layout(
            title='Storage (MB)',
            xaxis={'title': 'Time'},
            yaxis={'title': 'Storage (MB)'}
        )
    }
    ),

    html.Div(children='''
        Blocks/sec
    '''),
    
    dcc.Graph(
        id='blocks-sec-graph',
        figure={
            'data': [
                go.Scatter(
                    x=t,
                    y=[bps_*50 for bps_ in ma(bps,ma_size)],
                    mode='lines',
                    name='Blocks/sec',
                    hovertemplate='%{x|%Y-%m-%d %H:%M:%S}: %{y:.2f} %'
                ),
            ],
            'layout': go.Layout(
            title='Blocks/sec (%)',
            xaxis={'title': 'Time'},
            yaxis={'title': 'Blocks/sec (%)'}
        )
    }
    ),

    html.Div(children='''
        Peers
    '''),
    
    dcc.Graph(
        id='peers-graph',
        figure={
            'data': [
                go.Scatter(
                    x=t[-len(peers):],
                    y=peers,
                    mode='lines',
                    name='Peers'
                ),
            ],
            'layout': go.Layout(
            title='Peers',
            xaxis={'title': 'Time'},
            yaxis={'title': 'Peers'}
        )
    }
    ),

    html.Div(children='''
        Current Up Bandwidth usage (MB/sec)
    '''),
    
    dcc.Graph(
        id='bandwidth-graph',
        figure={
            'data': [
                go.Scatter(
                    x=t4[-len(bandwidths):],
                    y=[8*b/60 for b in ma(up_bandwidths,ma_size)],
                    mode='lines',
                    name='Bandwidth',
                    hovertemplate='%{x|%Y-%m-%d %H:%M:%S}: %{y:.2f} MB/s'
                ),
            ],
            'layout': go.Layout(
            title='Current Up Bandwidth usage (Mb/sec):',
            xaxis={'title': 'Time'},
            yaxis={'title': 'Bandwidth usage (Mb/sec)'}
        )
    }
    ),

    html.Div(children='''
        Current Bootstrap Bandwidth usage (Mb/sec)
    '''),
    
    dcc.Graph(
        id='bootstrap-bandwidth-graph',
        figure={
            'data': [
                go.Scatter(
                    x=t6[-len(boot_bandwidths):],
                    y=[b/60 for b in ma(boot_bandwidths, ma_size)],
                    mode='lines',
                    name='Bootstrap Bandwidth usage',
                    hovertemplate='%{x|%Y-%m-%d %H:%M:%S}: %{y:.2f} MB/s'
                ),
            ],
            'layout': go.Layout(
            title='Current Bootstrap Bandwidth usage (Mb/sec):',
            xaxis={'title': 'Time'},
            yaxis={'title': 'Bootstrap Bandwidth usage (Mb/sec)'}
        )
    }
    ),

    html.Div(children='''
        Current Down Bandwidth usage (Mb/sec):
    '''),
    
    dcc.Graph(
        id='down-bandwidth-graph',
        figure={
            'data': [
                go.Scatter(
                    x=t4[-len(bandwidths):],
                    y=[8*b/60 for b in ma(down_bandwidths, ma_size)],
                    mode='lines',
                    name='Down Bandwidth usage',
                    hovertemplate='%{x|%Y-%m-%d %H:%M:%S}: %{y:.2f} MB/s'
                ),
            ],
            'layout': go.Layout(
            title='Current Down Bandwidth usage (Mb/sec):',
            xaxis={'title': 'Time'},
            yaxis={'title': 'Down Bandwidth usage (Mb/sec)'}
        )
    }
    ),

])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)