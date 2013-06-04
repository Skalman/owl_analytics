import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import numpy as np
import matplotlib.collections as collections
import json


class MyLocator(mticker.MaxNLocator):
    def __init__(self, *args, **kwargs):
        mticker.MaxNLocator.__init__(self, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return mticker.MaxNLocator.__call__(self, *args, **kwargs)

plt.rc('axes', grid=True)
plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
textsize = 9

#####
#
# Rectangle for axises
#
#####
left, width = 0.1, 0.8
rect1 = [left, 0.5, width, 0.4]  # left, bottom, width, height
rect2 = [left, 0.3, width, 0.2]
rect3 = [left, 0.1, width, 0.2]

#####
#
# Figure
#
#####
fig = plt.figure(figsize=(20, 12), facecolor='white')
axescolor = '#f6f6f6'  # axises background color

ax1 = fig.add_axes(rect1, axisbg=axescolor)
ax1t = ax1.twinx()
ax2 = fig.add_axes(rect2, axisbg=axescolor, sharex=ax1)
ax3 = fig.add_axes(rect3, axisbg=axescolor, sharex=ax1)

#####
#
# Plot price and volume
#
#####
from apps.marketdataConsumer import intradaydata_np as intradata
from apps.marketdataConsumer import intradaydata_json

# DATE,CLOSE,HIGH,LOW,OPEN,VOLUME. Note! 1 = CLOSE
prices = intradata[:, 1]
t = intradata[:, 0]
fillcolor = 'darkgoldenrod'

low = intradata[:, 3]
high = intradata[:, 2]

deltas = np.zeros_like(prices)
deltas[1:] = np.diff(prices)
up = deltas > 0
ax1.vlines(t[up], low[up], high[up], color='black', label='_nolegend_')
ax1.vlines(t[~up], low[~up], high[~up], color='red', label='_nolegend_')

volume = (intradata[:, 4] * intradata[:, 5]) / 1e6  # volume in millions
vmax = volume.max()
poly = ax1t.fill_between(t, volume, 0, label='Volume', facecolor=fillcolor, edgecolor=fillcolor)
ax1t.set_ylim(0, 5 * vmax)
ax1t.set_yticks([])

#####
#
# MACD indicator axis
#
#####
from techmodels.indicators.trend.price.macd import MACDIndicator

fillcolor = 'darkslategrey'
nslow, nfast, nema = 35, 10, 5

macd_oscillator = MACDIndicator(nslow=35, nfast=10, nema=5)
y1 = macd_oscillator.indicator(prices)
y2 = macd_oscillator.indicator_inverse(prices)

ax2.fill_between(t, y1, 0, where=y2 <= y1, alpha=0.5, facecolor='green', edgecolor=fillcolor)
ax2.fill_between(t, y1, 0, where=y2 >= y1, alpha=0.5, facecolor='red', edgecolor=fillcolor)
ax2.vlines(t, y1, 0, color='blue', lw=0.5)
ax2.text(0.025, 0.95, 'MACD (%d, %d, %d)' % (nfast, nslow, nema), va='top', transform=ax2.transAxes, fontsize=textsize)

#####
#
# DPO indicator axis
#
#####
from techmodels.indicators.trend.price.dpo import DPOIndicator

fillcolor = 'darkslategrey'
n = 10  # Default 10

dpo = DPOIndicator(n)
y1 = dpo.indicator(prices)
y2 = dpo.indicator_inverse(prices)

ax3.fill_between(t, y1, 0, where=y2 <= y1, alpha=0.5, facecolor='gray', edgecolor=fillcolor)
ax3.fill_between(t, y1, 0, where=y2 >= y1, alpha=0.5, facecolor='black', edgecolor=fillcolor)
ax3.text(0.025, 0.95, 'DPO (%d)' % (n), va='top', transform=ax3.transAxes, fontsize=textsize)

#####
#
# Shading-Region overlay
#
#####
from visualization.matplotlib.utils.transform.regionshadingoverlay.regiontoshade import TranformRegionToShade

legend = ''


def shaderegion(chunkdata,
                color_p='green', color_n='red', color_alpha=0.1,
                legend=''):
    ymin, ymax = ax1.get_ylim()
    collection = collections.BrokenBarHCollection.span_where(
                    mdates.date2num(chunkdata.positiveTimestamps()),
                    ymin,
                    ymax,
                    where=chunkdata.positiveFlag(),
                    facecolor=color_p,
                    alpha=color_alpha)
    ax1.add_collection(collection)

    collection = collections.BrokenBarHCollection.span_where(
                    mdates.date2num(chunkdata.negativeTimestamps()),
                    ymin,
                    ymax,
                    where=chunkdata.negativeFlag(),
                    facecolor=color_n,
                    alpha=color_alpha)
    ax1.add_collection(collection)

    ax1.text(0.025, 0.95, legend, va='top',
             transform=ax1.transAxes, fontsize=textsize)

###
# MACD_CHUNK shading overlay
###
from sequences.io.trend.price.macd.s_chunk import macd_chunk

nfast, nslow, nema = 10, 35, 5
legend += '%s (%d, %d, %d)\n' % ('CHUNK-MACD', nfast, nslow, nema)
macd_chunkdata = TranformRegionToShade(macd_chunk(
                                            json.loads(intradaydata_json),
                                            nfast, nslow, nema,
                                            getter=lambda x: x[u'close']))
shaderegion(chunkdata=macd_chunkdata, legend=legend)

###
# DPO_CHUNK shading overlay
###
from sequences.io.trend.price.dpo.s_chunk import dpo_chunk
n = 10
legend += '%s (%d)\n' % ('CHUNK-DPO', n)
dpo_chunkdata = TranformRegionToShade(dpo_chunk(
                                            json.loads(intradaydata_json),
                                            n,
                                            getter=lambda x: x[u'close']))
shaderegion(chunkdata=dpo_chunkdata,
            color_p='gray', color_n='black', color_alpha=0.4,
            legend=legend)

#####
#
# Axis labeling
#
#####
# turn off upper axis tick labels, rotate the lower ones, etc
for ax in ax1, ax1t, ax2, ax3:
    if ax != ax3:
        for label in ax.get_xticklabels():
            label.set_visible(False)
    else:
        for label in ax.get_xticklabels():
            label.set_rotation(30)
            label.set_horizontalalignment('right')

    ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')

#####
#
# Eye candy
#
#####
# at most 5 ticks, pruning the upper and lower so they don't overlap
# with other ticks
ax1.yaxis.set_major_locator(MyLocator(5, prune='both'))
ax2.yaxis.set_major_locator(MyLocator(5, prune='both'))

#####
#
# Multiple-axes cursor (crosshair)
#
#####
from matplotlib.widgets import MultiCursor
# Note! set useblit = True on gtkagg for enhanced performance
multi = MultiCursor(fig.canvas, (ax1, ax2, ax3), color='r',
                    useblit=True, alpha=0.5, linewidth=1)

#####
#
# Display plot
#
#####
plt.show()
