"""
Source Code references: 
    - http://nighttimecuriosities.blogspot.fi/2012/08/historical-intraday-stock-price-data.html
    - http://matplotlib.org/examples/api/span_regions.html
    - https://github.com/vnoel/coderesearch/blob/master/niceplots.py
"""
### Example on how to use and plot this data
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import numpy as np
from Intraday_Marketdata_Extractor_NumpyArray_JSON import intradata, ticker, t_mChunk_up, ymin_mChunk_up, ymax_mChunk_up, flag_mChunk_up, t_mChunk_down, ymin_mChunk_down, ymax_mChunk_down, flag_mChunk_down, all_chunked
import matplotlib.collections as collections
 
def moving_average(p, n, type='simple'):
    """
    compute an n period moving average.
 
    type is 'simple' | 'exponential'
    """
    p = np.asarray(p)
    if type=='simple':
        weights = np.ones(n)
    else:
        weights = np.exp(np.linspace(-1., 0., n))
 
    weights /= weights.sum()
 
 
    a =  np.convolve(p, weights, mode='full')[:len(p)]
    a[:n] = a[n]
    return a
 
def moving_average_convergence(p, nslow=26, nfast=12):
    """
    compute the MACD (Moving Average Convergence/Divergence) using a fast and slow exponential moving avg'
    return value is emaslow, emafast, macd which are len(p) arrays
    """
    emaslow = moving_average(p, nslow, type='exponential')
    emafast = moving_average(p, nfast, type='exponential')
    return emaslow, emafast, emafast - emaslow
 
plt.rc('axes', grid=True)
plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
 
textsize = 9
left, width = 0.1, 0.8
#left, bottom, width, height
rect1 = [left, 0.5, width, 0.4] #Default [left, 0.3, width, 0.4] 
rect2 = [left, 0.1, width, 0.4] #Default [left, 0.1, width, 0.2]
rect3 = [left, 0.1, width, 0.4] #Default [left, 0.1, width, 0.2]
 
 
fig = plt.figure(figsize=(20,12), facecolor='white')
axescolor  = '#f6f6f6'  # the axies background color

ax1 = fig.add_axes(rect1, axisbg=axescolor) #left, bottom, width, height
ax1t = ax1.twinx()
ax2  = fig.add_axes(rect2, axisbg=axescolor, sharex=ax1)

### plot the price and volume data

# DATE,CLOSE,HIGH,LOW,OPEN,VOLUME, so 1 = CLOSE
prices = intradata[:,1]
t = intradata[:,0]
fillcolor = 'darkgoldenrod'

low = intradata[:,3]
high = intradata[:,2]
 
deltas = np.zeros_like(prices)
deltas[1:] = np.diff(prices)
up = deltas>0
ax1.vlines(t[up], low[up], high[up], color='black', label='_nolegend_')
ax1.vlines(t[~up], low[~up], high[~up], color='red', label='_nolegend_')

# Shading Region
ymin, ymax = ax1.get_ylim()
#collection = collections.BrokenBarHCollection.span_where(mdates.date2num(t), ymin, ymax, where=~up, facecolor='red', alpha=0.1)
collection = collections.BrokenBarHCollection.span_where(
                mdates.date2num(t_mChunk_up), ymin, ymax, where=flag_mChunk_up, facecolor='green', alpha=0.1)
ax1.add_collection(collection)

collection = collections.BrokenBarHCollection.span_where(
                mdates.date2num(t_mChunk_down), ymin, ymax, where=flag_mChunk_down, facecolor='red', alpha=0.1)
ax1.add_collection(collection)

ax1.text(0.025, 0.95, 'MACD_CHUNKER (%d, %d, %d)'%(10, 35, 5), va='top',
         transform=ax1.transAxes, fontsize=textsize)

#ma5 = moving_average(prices, 5, type='simple')
#ma50 = moving_average(prices, 50, type='simple')
#linema5, = ax1.plot(t, ma5, color='blue', lw=2, label='MA (5)')
#linema50, = ax1.plot(t, ma50, color='red', lw=2, label='MA (50)')
 
#props = font_manager.FontProperties(size=10)
#leg = ax1.legend(loc='center left', shadow=True, fancybox=True, prop=props)
#leg.get_frame().set_alpha(0.5)
 
volume = (intradata[:,4]*intradata[:,5])/1e6  # dollar volume in millions
vmax = volume.max()
poly = ax1t.fill_between(t, volume, 0, label='Volume', facecolor=fillcolor, edgecolor=fillcolor)
ax1t.set_ylim(0, 5*vmax)
ax1t.set_yticks([])
 
### compute the MACD indicator
fillcolor = 'darkslategrey'
nslow = 35 # Default 26
nfast = 10 # Default 12
nema = 5 # Default 9
emaslow, emafast, macd = moving_average_convergence(prices, nslow=nslow, nfast=nfast)
ema9 = moving_average(macd, nema, type='exponential')


#ax2.plot(t, macd, color='blue', lw=0.5)
#ax2.plot(t, ema9, color='red', lw=0.5)
#ax2.fill_between(t, macd-ema9, 0, alpha=0.5, facecolor=fillcolor, edgecolor=fillcolor)
y1 = macd-ema9
y2 = ema9-macd
ax2.fill_between(t, y1, 0, where=y2<=y1, alpha=0.5, facecolor='green', edgecolor=fillcolor) 
ax2.fill_between(t, y1, 0, where=y2>=y1, alpha=0.5, facecolor='red', edgecolor=fillcolor)
ax2.vlines(t, macd-ema9, 0, color='blue', lw=0.5)

ax2.text(0.025, 0.95, 'MACD (%d, %d, %d)'%(nfast, nslow, nema), va='top',
         transform=ax2.transAxes, fontsize=textsize)


# turn off upper axis tick labels, rotate the lower ones, etc
for ax in ax1, ax1t, ax2:
    if ax!=ax2:
        for label in ax.get_xticklabels():
            label.set_visible(False)
    else:
        for label in ax.get_xticklabels():
            label.set_rotation(30)
            label.set_horizontalalignment('right')
 
    ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
 
class MyLocator(mticker.MaxNLocator):
    def __init__(self, *args, **kwargs):
        mticker.MaxNLocator.__init__(self, *args, **kwargs)
 
    def __call__(self, *args, **kwargs):
        return mticker.MaxNLocator.__call__(self, *args, **kwargs)
 
# at most 5 ticks, pruning the upper and lower so they don't overlap
# with other ticks
ax1.yaxis.set_major_locator(MyLocator(5, prune='both'))
ax2.yaxis.set_major_locator(MyLocator(5, prune='both'))
 
plt.show()
