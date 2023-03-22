import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
import numpy as np
import numpy as np
from datetime import datetime
import datetime
import subprocess
from dash.dependencies import Input, Output

# Load the data
ma_size = 4
episode = ""

def mega(boot):
    if boot[-2] == "G":    
        return float(boot[:-2].replace(",", "."))*1000
    elif boot[-2] == "M":    
        return float(boot[:-2].replace(",", "."))
    elif boot[-2] == "K":    
        return float(boot[:-2].replace(",", "."))/1000
    else:
        return float(boot[:-1].replace(",", "."))/1000
    
def ma(x, w=10):
    if w == 1:
        return x
    c = np.convolve(x, np.ones(w), 'same') / w
    c[:w] = np.mean(x[:w])
    c[-w:] = np.mean(x[-w:])
    return list(c)

def get_y_txps():
    f1 = f'{episode}log_txps.txt'
    with open(f1) as file:
        lines = file.readlines()
        lines = [line.rstrip().split(" ") for line in lines]
    txps = [int(line[7]) for line in lines]
    return ma(txps, ma_size)

def get_x_txps():
    f1 = f'{episode}log_txps.txt'
    with open(f1) as file:
        lines = file.readlines()
        lines = [line.rstrip().split(" ") for line in lines]
    t = [int(float(line[0].replace('\x00',''))) for line in lines]
    t = [datetime.datetime.fromtimestamp(ts) for ts in t]
    return t

def get_x_stakers():
    # get_logs_cmd = "scp -r root@195.134.167.226:/root/massa-benchmark-main/benchmark_E20/*.txt ."
    # try:
    #     subprocess.check_output(get_logs_cmd, shell=True, stderr=subprocess.STDOUT)
    #     print("Log files retrieved!")
    # except:
    #     print("Error retrieving files")
    f1 = f'{episode}log_txps.txt'
    with open(f1) as file:
        lines = file.readlines()
        lines = [line.rstrip().split(" ") for line in lines]
    t = [int(float(line[0].replace('\x00',''))) for line in lines]
    t = [datetime.datetime.fromtimestamp(ts) for ts in t]
    return t

def get_y_stakers():
    f1 = f'{episode}log_txps.txt'
    with open(f1) as file:
        lines = file.readlines()
        lines = [line.rstrip().split(" ") for line in lines]
    stakers = [int(line[4]) for line in lines]
    return stakers

def get_x_cpu():
    f2 = f'{episode}sys_load_cpu_ram_io.txt'
    with open(f2) as file:
        lines = file.readlines()
        lines = [line.rstrip().split() for line in lines if line[0] != "#"]
    t2 = [int(lines[i][0]) for i in range(len(lines)-1) if len(lines[i])==1 and not len(lines[i+1])==1]
    cpus = [float(lines[i][7].replace(",", ".")) for i in range(len(lines)-1) if len(lines[i])>8 and len(lines[i+1])==1][:len(t2)]
    t2[-len(cpus):]
    t2 = [datetime.datetime.fromtimestamp(ts) for ts in t2]
    return t2

def get_y_cpu():
    f2 = f'{episode}sys_load_cpu_ram_io.txt'
    with open(f2) as file:
        lines = file.readlines()
        lines = [line.rstrip().split() for line in lines if line[0] != "#"]
    t2 = [int(lines[i][0]) for i in range(len(lines)-1) if len(lines[i])==1 and not len(lines[i+1])==1]
    cpus = [float(lines[i][7].replace(",", ".")) for i in range(len(lines)-1) if len(lines[i])>8 and len(lines[i+1])==1][:len(t2)]
    return(ma(cpus, ma_size))

def get_x_ram():
    f2 = f'{episode}sys_load_cpu_ram_io.txt'
    with open(f2) as file:
        lines = file.readlines()
        lines = [line.rstrip().split() for line in lines if line[0] != "#"]
    t2 = [int(lines[i][0]) for i in range(len(lines)-1) if len(lines[i])==1 and not len(lines[i+1])==1]
    cpus = [float(lines[i][7].replace(",", ".")) for i in range(len(lines)-1) if len(lines[i])>8 and len(lines[i+1])==1][:len(t2)]
    t2[-len(cpus):]
    t2 = [datetime.datetime.fromtimestamp(ts) for ts in t2]
    return t2

def get_y_ram():
    f2 = f'{episode}sys_load_cpu_ram_io.txt'
    with open(f2) as file:
        lines = file.readlines()
        lines = [line.rstrip().split() for line in lines if line[0] != "#"]
    t2 = [int(lines[i][0]) for i in range(len(lines)-1) if len(lines[i])==1 and not len(lines[i+1])==1]
    rams = [float(lines[i][13].replace(",", ".")) for i in range(len(lines)-1) if len(lines[i])>8 and len(lines[i+1])==1][:len(t2)]
    return [ram*31.1/100 for ram in rams]

def get_x_io():
    f2 = f'{episode}sys_load_cpu_ram_io.txt'
    with open(f2) as file:
        lines = file.readlines()
        lines = [line.rstrip().split() for line in lines if line[0] != "#"]
    t2 = [int(lines[i][0]) for i in range(len(lines)-1) if len(lines[i])==1 and not len(lines[i+1])==1]
    cpus = [float(lines[i][7].replace(",", ".")) for i in range(len(lines)-1) if len(lines[i])>8 and len(lines[i+1])==1][:len(t2)]
    t2[-len(cpus):]
    t2 = [datetime.datetime.fromtimestamp(ts) for ts in t2]
    return t2

def get_y_io():
    f2 = f'{episode}sys_load_cpu_ram_io.txt'
    with open(f2) as file:
        lines = file.readlines()
        lines = [line.rstrip().split() for line in lines if line[0] != "#"]
    t2 = [int(lines[i][0]) for i in range(len(lines)-1) if len(lines[i])==1 and not len(lines[i+1])==1]
    ios = [float(lines[i][17].replace(",", ".")) for i in range(len(lines)-1) if len(lines[i])>8 and len(lines[i+1])==1][:len(t2)]
    return ma(ios, ma_size)

def get_x_block_prop():
    f3 = f'{episode}log_proptime.txt'
    with open(f3) as file:
        lines = file.readlines()
        lines = [line.rstrip().split() for line in lines]
    t3 = [int(line[0].replace('\x00','')) for line in lines]
    t3 = [datetime.datetime.fromtimestamp(ts) for ts in t3]
    return t3
    
def get_y_block_prop():
    f3 = f'{episode}log_proptime.txt'
    with open(f3) as file:
        lines = file.readlines()
        lines = [line.rstrip().split() for line in lines]
    prop_mean_b = [int(line[9]) for line in lines]
    return prop_mean_b

def get_x_header_prop():
    f3 = f'{episode}log_proptime.txt'
    with open(f3) as file:
        lines = file.readlines()
        lines = [line.rstrip().split() for line in lines]
    t3 = [int(line[0].replace('\x00','')) for line in lines]
    t3 = [datetime.datetime.fromtimestamp(ts) for ts in t3]
    return t3

def get_y_header_prop():
    f3 = f'{episode}log_proptime.txt'
    with open(f3) as file:
        lines = file.readlines()
        lines = [line.rstrip().split() for line in lines]
    prop_mean_h = [int(line[5]) for line in lines]
    return prop_mean_h

def get_x_storage():
    f5 = f'{episode}sys_load_store.txt'
    with open(f5) as file:
        lines = file.readlines()
        lines = [line.rstrip().split() for line in lines]
    t5 = [int(line[0].replace('\x00','')) for line in lines if line and len(line)== 1]
    t5 = [datetime.datetime.fromtimestamp(ts) for ts in t5]
    storage = []
    for line in lines:
        if len(line) == 1:
            storage.append(0)
        else:
            storage[-1] = storage[-1] + int(line[0])
    storage = storage[:len(t5)]
    return t5[-len(storage):]

def get_y_storage():
    f5 = f'{episode}sys_load_store.txt'
    with open(f5) as file:
        lines = file.readlines()
        lines = [line.rstrip().split() for line in lines]
    t5 = [int(line[0].replace('\x00','')) for line in lines if line and len(line)== 1]
    storage = []
    for line in lines:
        if len(line) == 1:
            storage.append(0)
        else:
            storage[-1] = storage[-1] + int(line[0])
    storage = storage[:len(t5)]
    return [s/1000 for s in storage]

def get_x_peers():
    f1 = f'{episode}log_txps.txt'
    with open(f1) as file:
        lines = file.readlines()
        lines = [line.rstrip().split(" ") for line in lines]
    t = [int(float(line[0].replace('\x00',''))) for line in lines]
    t = [datetime.datetime.fromtimestamp(ts) for ts in t]
    peers = [int(line[8]) for line in lines if len(line)>8]
    return t[-len(peers):]

def get_y_peers():
    f1 = f'{episode}log_txps.txt'
    with open(f1) as file:
        lines = file.readlines()
        lines = [line.rstrip().split(" ") for line in lines]
    peers = [int(line[8]) for line in lines if len(line)>8]
    return peers

def get_x_upbandwidth():
    f4 = f'{episode}sys_load_net.txt'
    with open(f4) as file:
        lines = file.readlines()
        lines = [line.rstrip().split() for line in lines]
    bandwidths = [mega(line[4]) for line in lines if len(line) > 1]
    t4 = [int(line[0].replace('\x00','')) for line in lines if line and line[0].replace('\x00','').isdigit()]
    t4 = [datetime.datetime.fromtimestamp(ts) for ts in t4]
    return t4[-len(bandwidths):]

def get_y_upbandwidth():
    f4 = f'{episode}sys_load_net.txt'
    with open(f4) as file:
        lines = file.readlines()
        lines = [line.rstrip().split() for line in lines]
    up_bandwidths = [mega(line[2]) for line in lines if len(line) > 1]
    return [8*b/60 for b in ma(up_bandwidths,ma_size)]

def get_x_downbandwidth():
    f4 = f'{episode}sys_load_net.txt'
    with open(f4) as file:
        lines = file.readlines()
        lines = [line.rstrip().split() for line in lines]
    bandwidths = [mega(line[4]) for line in lines if len(line) > 1]
    t4 = [int(line[0].replace('\x00','')) for line in lines if line and line[0].replace('\x00','').isdigit()]
    t4 = [datetime.datetime.fromtimestamp(ts) for ts in t4]
    return t4[-len(bandwidths):]

def get_y_downbandwidth():
    f4 = f'{episode}sys_load_net.txt'
    with open(f4) as file:
        lines = file.readlines()
        lines = [line.rstrip().split() for line in lines]
    down_bandwidths = [mega(line[3]) for line in lines if len(line) > 1]
    return [8*b/60 for b in ma(down_bandwidths, ma_size)]

def get_x_bootstrapbandwidth():
    # get_logs_cmd = "scp -r root@158.69.120.215:root/sys_load_net.txt ./sys_load_net_testnet3_boot.txt"
    # try:
    #     subprocess.check_output(get_logs_cmd, shell=True, stderr=subprocess.STDOUT)
    #     print("Log files retrieved!")
    # except:
    #     print("Error retrieving files")
    f6 = f'{episode}sys_load_net_testnet3_boot.txt'
    with open(f6) as file:
        lines = file.readlines()
        lines = [line.rstrip().split() for line in lines]
    t6 = [int(line[0].replace('\x00','')) for line in lines if line and line[0].replace('\x00','').isdigit()]
    boot_bandwidths = [mega(line[2]) for line in lines if len(line) > 1]
    t6 = [datetime.datetime.fromtimestamp(ts) for ts in t6]
    return t6[-len(boot_bandwidths):]

def get_y_bootstrapbandwidth():
    f6 = f'{episode}sys_load_net_testnet3_boot.txt'
    with open(f6) as file:
        lines = file.readlines()
        lines = [line.rstrip().split() for line in lines]
    boot_bandwidths = [mega(line[2]) for line in lines if len(line) > 1]
    return [b/60 for b in ma(boot_bandwidths, ma_size)]

def get_x_blocks_sec():
    f1 = f'{episode}log_txps.txt'
    with open(f1) as file:
        lines = file.readlines()
        lines = [line.rstrip().split(" ") for line in lines]
    t = [int(float(line[0].replace('\x00',''))) for line in lines]
    t = [datetime.datetime.fromtimestamp(ts) for ts in t]
    return t

def get_y_blocks_sec():
    f1 = f'{episode}log_txps.txt'
    with open(f1) as file:
        lines = file.readlines()
        lines = [line.rstrip().split(" ") for line in lines]
    bps = [float(line[6]) for line in lines]
    return [bps_*50 for bps_ in ma(bps,ma_size)]

# Create the Dash app
app = dash.Dash()
server = app.server
# Define the layout of the app

app = dash.Dash()

# create the options for the dropdown menu
dropdown_options = [
    {'label': 'Txps', 'value': 'txps'},
    {'label': 'Stakers', 'value': 'stakers'},
    {'label': 'CPU Usage', 'value': 'cpu'},
    {'label': 'RAM Usage', 'value': 'ram'},
    {'label': 'IO Usage', 'value': 'io'},
    {'label': 'Avg Block Propagation Time', 'value': 'blockprop'},
    {'label': 'Avg Header Propagation Time', 'value': 'headerprop'},
    {'label': 'Storage', 'value': 'storage'},
    {'label': 'Blocks/sec', 'value': 'blocksec'},
    {'label': 'Peers', 'value': 'peers'},
    {'label': 'Bootstrap Bandwidth usage', 'value': 'bootstrap'},
    {'label': 'Up Bandwidth usage', 'value': 'upbandwidth'},
    {'label': 'Down Bandwidth usage', 'value': 'downbandwidth'},
]

episode_options = [
    {'label': 'Episode 20', 'value': 'ep20'},
    {'label': 'Episode 19', 'value': 'ep19'},
    {'label': 'Episode 18', 'value': 'ep18'},
    {'label': 'Episode 17', 'value': 'ep17'},
    {'label': 'Episode 16', 'value': 'ep16'},
    {'label': 'Episode 15', 'value': 'ep15'},
    {'label': 'Episode 14', 'value': 'ep14'},
    {'label': 'Episode 12', 'value': 'ep12'},
    {'label': 'Episode 11', 'value': 'ep11'},
    {'label': 'Episode 10', 'value': 'ep10'},
    {'label': 'Episode 9', 'value': 'ep9'},
    {'label': 'Episode 8', 'value': 'ep8'},
    {'label': 'Episode 7', 'value': 'ep7'},
    {'label': 'Episode 6', 'value': 'ep6'},
]

app.layout = html.Div([
    html.Label('Select graphs to display or compare:'),
    dcc.Dropdown(
        id='dropdown',
        options=dropdown_options,
        value=['txps'],
        multi=True
    ),
    dcc.Graph(id='graph'),

    html.Label('Switch episode'),
    dcc.Dropdown(
        id='dropdown_episode',
        options=episode_options,
    )
])

@app.callback(Output('graph', 'figure'),
              Input('dropdown', 'value'), 
              Input('dropdown_episode', 'value'))
def update_graph(selected_values, episode_values):
    data = []
    global episode
    if episode_values:
        if 'ep20' in episode_values:
            episode = ""
        elif 'ep19' in episode_values:
            episode = "ep19/"
        elif 'ep18' in episode_values:
            episode = "ep18/"
        elif 'ep17' in episode_values:
            episode = "ep17/"
        elif 'ep16' in episode_values:
            episode = "ep16/"
        elif 'ep15' in episode_values:
            episode = "ep15/"
        elif 'ep14' in episode_values:
            episode = "ep14/"
        elif 'ep12' in episode_values:
            episode = "ep12/"
        elif 'ep11' in episode_values:
            episode = "ep11/"
        elif 'ep10' in episode_values:
            episode = "ep10/"
        elif 'ep9' in episode_values:
            episode = "ep9/"
        elif 'ep8' in episode_values:
            episode = "ep8/"
        elif 'ep7' in episode_values:
            episode = "ep7/"
        elif 'ep6' in episode_values:
            episode = "ep6/"
    if selected_values:
        for value in selected_values:
            if value == 'txps':
                data.append({'x': get_x_txps(), 'y': get_y_txps(), 'type': 'scatter', 'name': 'Transactions/sec', 'hovertemplate': '%{x|%Y-%m-%d %H:%M:%S}: %{y:.2f} Tx/sec'})
            if value == 'stakers':
                data.append({'x': get_x_stakers(), 'y': get_y_stakers(), 'type': 'scatter', 'name': 'Stakers', 'hovertemplate': '%{x|%Y-%m-%d %H:%M:%S}: %{y:.2f} Stakers'})
            if value == 'cpu':
                data.append({'x': get_x_cpu(), 'y': get_y_cpu(), 'type': 'scatter', 'name': 'CPU Usage', 'hovertemplate': '%{x|%Y-%m-%d %H:%M:%S}: %{y:.2f} %'})
            if value == 'ram':
                data.append({'x': get_x_ram(), 'y': get_y_ram(), 'type': 'scatter', 'name': 'RAM Usage', 'hovertemplate': '%{x|%Y-%m-%d %H:%M:%S}: %{y:.2f} GB'})
            if value == 'io':
                data.append({'x': get_x_io(), 'y': get_y_io(), 'type': 'scatter', 'name': 'IO Usage', 'hovertemplate': '%{x|%Y-%m-%d %H:%M:%S}: %{y:.2f} kB/sec'})
            if value == 'blockprop':
                data.append({'x': get_x_block_prop(), 'y': get_y_block_prop(), 'type': 'scatter', 'name': 'Avg Block Propagation Time', 'hovertemplate': '%{x|%Y-%m-%d %H:%M:%S}: %{y:.2f} ms'})
            if value == 'headerprop':
                data.append({'x': get_x_header_prop(), 'y': get_y_header_prop(), 'type': 'scatter', 'name': 'Avg Header Propagation Time', 'hovertemplate': '%{x|%Y-%m-%d %H:%M:%S}: %{y:.2f} ms'})
            if value == 'storage':
                data.append({'x': get_x_storage(), 'y': get_y_storage(), 'type': 'scatter', 'name': 'Storage', 'hovertemplate': '%{x|%Y-%m-%d %H:%M:%S}: %{y:.2f} MB'})
            if value == 'blocksec':
                data.append({'x': get_x_blocks_sec(), 'y': get_y_blocks_sec(), 'type': 'scatter', 'name': 'Blocks/sec', 'hovertemplate': '%{x|%Y-%m-%d %H:%M:%S}: %{y:.2f} %'})
            if value == 'peers':
                data.append({'x': get_x_peers(), 'y': get_y_peers(), 'type': 'scatter', 'name': 'Peers', 'hovertemplate': '%{x|%Y-%m-%d %H:%M:%S}: %{y:.2f} Peers'})
            if value == 'bootstrap':
                data.append({'x': get_x_bootstrapbandwidth(), 'y': get_y_bootstrapbandwidth(), 'type': 'scatter', 'name': 'Bootstrap Bandwidth Usage', 'hovertemplate': '%{x|%Y-%m-%d %H:%M:%S}: %{y:.2f} MB/sec'})
            if value == 'upbandwidth':
                data.append({'x': get_x_upbandwidth(), 'y': get_y_upbandwidth(), 'type': 'scatter', 'name': 'Up Bandwidth Usage', 'hovertemplate': '%{x|%Y-%m-%d %H:%M:%S}: %{y:.2f} MB/sec'})
            if value == 'downbandwidth':
                data.append({'x': get_x_downbandwidth(), 'y': get_y_downbandwidth(), 'type': 'scatter', 'name': 'Down Bandwidth Usage', 'hovertemplate': '%{x|%Y-%m-%d %H:%M:%S}: %{y:.2f} MB/sec'})
    return {'data': data}

if __name__ == '__main__':
    app.run_server(debug=True)
