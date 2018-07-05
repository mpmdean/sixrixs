import numpy as np
import pandas as pd
pd.set_option('display.height', 500)
pd.set_option('display.max_rows', 500)
from collections import OrderedDict
import datetime, time

import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcdefaults()
from cycler import cycle

from databroker import get_events, get_table, DataBroker as db

import ipywidgets as widgets

markers = cycle(['o', 's', '^', 'v', 'p', '<', '>', 'h'])

# Functions
def stopped(header):
    try:
        status = header.stop['exit_status']
    except KeyError:
        status = 'Python crash before exit'
    
    if status == 'success':
        return True
    else:
        return False
    
    
def get_scan_id_dict(headers):
    return OrderedDict([(get_scan_desc(header), header) for header in headers if stopped(header)])

def get_keys(header):
    try:
        keys = header.table().keys()
        key_list = sorted(list(keys))
        return key_list
    except:
        return []

def get_scanned_motor(header):
    try:
        return ' '.join(header.start['motors'])
    except:
        return ''

def get_scan_desc(header):
    return '{} {} {}'.format(header.start['scan_id'], header.start['plan_name'], get_scanned_motor(header))

# Widgets

today_string = str(datetime.datetime.now().date())
db_search_widget = widgets.Text(description='DB search',
                                value='since=\'{}\''.format(today_string))

#refresh_headers_widget = widgets.Button(description='Refresh')

select_scan_id_widget = widgets.Select(description='Select uid')

select_x_widget = widgets.Dropdown(description='x')

select_y_widget = widgets.Dropdown(description='y')

select_mon_widget = widgets.Dropdown(description='mon')

use_mon_widget = widgets.Checkbox(description='Normalize')

plot_button = widgets.Button(description='Plot')

clear_button = widgets.Button(description='Clear')

baseline_button = widgets.Button(description='Display baseline')

baseline_display = widgets.HTML('Baseline')
#starting_values_display = widgets.Textarea(min_width='1500px')


# bindings

def wrap_refresh(change):
    try:
        query = eval("dict({})".format(db_search_widget.value))
        headers = db(**query)
    except NameError:
        headers = []
        db_search_widget.value += " -- is an invalid search"
    
    scan_id_dict = get_scan_id_dict(headers)
    select_scan_id_widget.options = scan_id_dict

db_search_widget.on_submit(wrap_refresh)
#refresh_headers_widget.on_click(wrap_refresh)
    
def wrap_select_scan_id(change):
    keys = get_keys(select_scan_id_widget.value)
    select_x_widget.options = keys
    scanned_motor = get_scanned_motor(select_scan_id_widget.value)
    try:
        usekey =  next((key for key in keys if scanned_motor in key), keys[0])
        select_x_widget.value = usekey
    except:
        pass
    
    select_y_widget.options = keys
    default_y = 'fccd_stats1_total'
    select_mon_widget.options = keys
    try:
        select_y_widget.value = default_y
    except:
        pass

select_scan_id_widget.observe(wrap_select_scan_id)

def wrap_plotit(change):
    header = select_scan_id_widget.value
    table = header.table()
    x = table[select_x_widget.value].values
    if use_mon_widget.value:
        y = table[select_y_widget.value].values / table[select_mon_widget.value].values
    else:
        y = table[select_y_widget.value].values
    
    label= header.start['scan_id']
    
    ax = plt.gca()
    ax.plot(x, y, marker=next(markers), label=label)
    ax.set_xlabel(select_x_widget.value)
    ax.set_ylabel(select_y_widget.value)
    ax.legend()

plot_button.on_click(wrap_plotit)


def wrap_baseline(change):
    header = select_scan_id_widget.value
    baseline_table = header.table(stream_name='baseline')
    baseline_table.index=['Before', "After"]
    title = "<strong> Scan_id {} baseline </strong>".format(header.start['scan_id'])
    baseline_display.value = title + baseline_table.transpose().to_html()

baseline_button.on_click(wrap_baseline)

def wrap_clearit(change):
    plt.gca().cla()
    
clear_button.on_click(wrap_clearit)

