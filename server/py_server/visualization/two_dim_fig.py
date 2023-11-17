import plotly.express as px 
import random
import plotly.io as pio
import os
def scatter(x, y):
    fig=px.scatter(x, y, title="Scatter plot")
    return fig

def bar(x, y):
    fig=px.bar(x, y, title="Bar plot")
    return fig

def line(x, y):
    fig=px.line(x, y, title="Line plot")
    return fig

def hist(x, y):
    fig=px.histogram(x, y, title="Histogram")
    return fig

def pie(x):
    fig=px.pie(x, title="Pie chart")

x = list(range(2023, 2073))
y = [50 + 10 * i + random.randint(-5, 5) for i in range(50)]
# fig = px.scatter(title='Empty Figure')

choice=int(input("1.scatter 2.line 3.bar 4.histogram 5.pie\nEnter choice:"))
match choice:
    case 1: fig = scatter(x, y)
    case 2: fig = bar(x, y)
    case 3: fig = bar(x, y)
    case 4: fig= hist(x, y)
    case 5: fig=pie(x)
    
path=os.path.dirname(os.path.abspath(__file__))
path+='/images/result_graph.png'
# fig=px.line(x, y)
pio.write_image(fig, path)
