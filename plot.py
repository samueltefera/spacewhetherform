from pickle import FALSE
from unicodedata import name
import numpy as np
import pandas as pd
from datetime import date
from time import sleep
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})
from mpl_toolkits.axes_grid1 import make_axes_locatable
import re
import cartopy.crs as ccrs
import datetime
import os
import download
import cartopy.feature as fc
stop = False
current_downloaded = False
fig_size = [14, 10]
plt.rcParams['figure.figsize'] = fig_size
def current_date():
    return datetime.date.today()
    
def current_year():
    return current_date().year

def day_of_year():
    return current_date().timetuple().tm_yday

def day_of_the_month():
    return current_date().day
downloaded_day_year = day_of_year()    
def parse_map(tecmap, exponent = -1):
    tecmap = re.split('.*END OF TEC MAP', tecmap)[0]
    return np.stack([np.fromstring(l, sep=' ') for l in re.split('.*LAT/LON1/LON2/DLON/H\\n',tecmap)[1:]])*10**exponent
ims = []    
def get_tecmaps(filename):
    with open(filename) as f:
        ionex = f.read()
        return [parse_map(t) for t in ionex.split('START OF TEC MAP')[1:]]

def ionex_filename(year, day, centre, zipped = True):
    return '{}g{:03d}0.{:02d}i{}'.format(centre, day, year % 100, '.Z' if zipped else '')


def ionex_local_path(year, day, centre = 'c2p', directory = os.getcwd() + '\\TECfile\\', zipped = False):
    return directory + '' + ionex_filename(year, day, centre, zipped)
    
start_month = current_date().month
start_month   = current_date().month 
start_day = 0

def timestamp(year, day):
    global  start_month, start_day
    start_date=date(year,start_month, start_day + day) 
    end_date = date(year,start_month, start_day + day+1) 
    time = pd.date_range(start= start_date , end=end_date, periods=25)
    return time

time=timestamp(current_year(),int(day_of_the_month()))  
#abc = get_tecmaps(ionex_local_path(current_year(), day_of_year()))
previous_year = current_year()
previous_day_of_year = day_of_year()
dir = 'tmpPlots'

def Ionex_plot():
    global current_downloaded, downloaded_day_year,stop
    while True:
        print('tread ionex')
        if stop:
            break
        if current_downloaded and downloaded_day_year == day_of_year():
            sleep(1)
            #print("print many times")
            continue
    
        down = download.download()

        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))

        for i,tecmap in zip(range(25),get_tecmaps(ionex_local_path(current_year(), day_of_year()))):
            date_stamp = time[i]
            proj = ccrs.PlateCarree()
            f, ax = plt.subplots(1, 1, subplot_kw=dict(projection=proj))

            ax.coastlines()
            ax.add_feature(fc.BORDERS,edgecolor='#80bfff')
            ax.add_feature(fc.COASTLINE,edgecolor='#80bfff')

            h = plt.imshow(tecmap, cmap='jet', vmin=0, vmax=100, extent = (-20, 70, -40, 60), transform=proj)
            plt.title('Total Electron Content (TEC)   '+ ' '+str(date_stamp)+ ' UT')
            divider = make_axes_locatable(ax)
            ax_cb = divider.new_horizontal(size='5%', pad=0.1, axes_class=plt.Axes)
            f.add_axes(ax_cb)
            cb = plt.colorbar(h, cax=ax_cb)
            plt.rc('text', usetex=True)
            cb.set_label('TECU ($10^{16} \\mathrm{el}/\\mathrm{m}^2$)')   
            plt.savefig('tmpPlots/'+str(date_stamp)[:-6], bbox_inches = 'tight')
            downloaded_day_year = day_of_year()
            current_downloaded = True            
def stop_thread():
    global stop
    stop = True

if __name__ == "__main__":
    Ionex_plot()