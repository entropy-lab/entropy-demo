from typing import List

import numpy as np

from bokeh.models import Renderer
from bokeh.plotting import Figure
from entropylab.api.plot import PlotGenerator
from matplotlib.figure import Figure as matplotlibFigure
from plotly import graph_objects as go
import plotly.express as px
from scipy.stats import linregress


class LinfitPlotGenerator(PlotGenerator):

    def __init__(self) -> None:
        super().__init__()

    def plot_bokeh(self, figure: Figure, data, **kwargs) -> Renderer:
        raise NotImplementedError()

    def plot_matplotlib(self, figure: matplotlibFigure, data, **kwargs):
        raise NotImplementedError()

    def plot_plotly(self, figure: go.Figure, data, **kwargs) -> Figure:
        axis_labels = data[1]
        data= data[0]
        if isinstance(data, List) and len(data) == 2 and len(data[0]) == len(data[1]):
            x = data[0]
            y = data[1]

            fig = px.scatter(x=x, y=y, trendline='ols')
            # fig.update_traces(marker=dict(size=12), line=dict(color='Green'))
            fig.data[0].marker=dict(color='green',size=12)
            figure.add_trace(fig.data[0])
            fig.data[1].line.color = 'red'

            figure.add_trace(
                fig.data[1]
            )
            figure.update_layout(
                title="Plot Title",
                xaxis_title=axis_labels['xlabel'],
                yaxis_title=axis_labels['ylabel'])


            return figure
        else:
            raise TypeError("data type is not supported")

class MyImShowPlotGenerator(PlotGenerator):
    def __init__(self) -> None:
        super().__init__()

    def plot_bokeh(self, figure: Figure, data, **kwargs) -> Renderer:
        pass

    def plot_matplotlib(self, figure: matplotlibFigure, data, **kwargs):
        pass

    def plot_plotly(self, figure: go.Figure, data, **kwargs) -> None:
        fig = px.imshow(data)
        # fig.data[0].autocolorscale = True
        figure.add_trace(fig.data[0])
        return figure

