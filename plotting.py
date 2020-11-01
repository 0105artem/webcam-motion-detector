# plotting.py -  visualizes the times when the object entered and exited the video frame
# and represents in in html file Graph.html

from motion_detector import df
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

df["Start_string"] = df["Start"].dt.strftime("%Y-%m-%D %H:%M:%S")
df["End_string"] = df["Endtime"].dt.strftime("%Y-%m-%D %H:%M:%S")

cds = ColumnDataSource(df)

plot = figure(x_axis_type = 'datetime', height = 100, width = 500,
           sizing_mode = "scale_width", title = "Motion Graph")

plot.yaxis.minor_tick_line_color = None
plot.yaxis.ticker.desired_num_ticks = 1

hover = HoverTool(tooltips=[("Start", "@Start_string"), ("Endtime", "@End_string")])
plot.add_tools(hover)

quadrant = plot.quad(left = "Start", right = "Endtime", bottom = 0,
                  top = 1, color = "green", source = cds)

output_file("Graph.html")
show(plot)