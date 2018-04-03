import pandas as pd
from bokeh.models import (HoverTool, FactorRange, Plot, LinearAxis, Grid,
                          Range1d)
from bokeh.models.glyphs import VBar
from bokeh.plotting import figure
# from bokeh.charts import Bar
# from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource
import getData
import analyzeData

df = getData.get_data()
airlines = analyzeData.claims_by_field('airline', df)[0:20]


def airlineGraph(series, title, x_name, y_name):
    width = 1200
    height = 300

    df = series.to_frame()

    print(df)
    # source = ColumnDataSource(df)
    # print(source)
    # xdr = FactorRange(factors=df[x_name])
    # ydr = Range1d(start=0, end=max(df[y_name])*1.5)
    #
    # plot = figure(title=title, x_range=xdr, y_range=ydr, plot_width=width,
    #               plot_height=height, min_border=0, responsive=True, outline_line_color="#666666")
    #
    # glyph = VBar(x=x_name, top=y_name, bottom=0, width=.8,
    #              fill_color="#e12127")
    # plot.add_glyph(source, glyph)
    #
    # xaxis = LinearAxis()
    # yaxis = LinearAxis()
    #
    # plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    # plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
    # plot.toolbar.logo = None
    # plot.min_border_top = 0
    # plot.xgrid.grid_line_color = None
    # plot.ygrid.grid_line_color = "#999999"
    # plot.yaxis.axis_label = "Bugs found"
    # plot.ygrid.grid_line_alpha = 0.1
    # plot.xaxis.axis_label = "Days after app deployment"
    # plot.xaxis.major_label_orientation = 1
    # return plot


if __name__ == '__main__':
    airlineGraph(airlines, 'airlines', "hi", "hey")