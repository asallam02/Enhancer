'''This page is the visualization page, it is used to 
graph and show the results from the ML model. 
'''

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
import plotly.graph_objs as go
from Models.Graphing.Plotter import Plotter

class GraphTab(QWidget):
    '''This class creates a graphing tab widget to be 
    used within other widgets. It takes a given DNA seq,
    the model results, the wanted track, and shows the 
    graph. 
    '''
    def __init__(self, track_no, parent=None):
        self.track = track_no
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        # create a webview to show plotly figures as html object
        self.webview = QWebEngineView()
        layout.addWidget(self.webview)
        self.setLayout(layout)

    def plot_graph(self, query, organizer):
        # create the plotly figure
        fig = Plotter(query, organizer, self.track)

        # convert Plotly figure to HTML
        plotly_html = fig.to_html(include_plotlyjs='cdn')

        # set the page to show the figure
        self.webview.setHtml(plotly_html)

class VizPage(QWidget):
    '''This page creates a visualization page.
    Currently it only shows 5 pre-set tracks, but this 
    should be changed to allow users to select needed 
    tracks. 

    The visualization page consists of several tabs 
    using the GraphTab widget above.  
    '''
    organizer = None
    query = None

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        # Create tabs and add them to the tab widget
        self.track1 = GraphTab(0)
        self.track2 = GraphTab(1)
        self.track3 = GraphTab(2)
        self.track4 = GraphTab(3)
        self.track5 = GraphTab(4)

        self.tabs.addTab(self.track1, "DNASE:CD14-positive monocyte female")
        self.tabs.addTab(self.track2, "DNASE:skeletal muscle cell")
        self.tabs.addTab(self.track3, "DNASE:T-cell")
        self.tabs.addTab(self.track4, "CHIP:CTCF:keratinocyte female")
        self.tabs.addTab(self.track5, "CAGE:Wilms' tumor cell line:G-401")

        layout.addWidget(self.tabs)
        self.setLayout(layout)
    
    def plot_graphs(self):
        # Plot initial graphs
        self.track1.plot_graph(self.query, self.organizer)
        self.track2.plot_graph(self.query, self.organizer)
        self.track3.plot_graph(self.query, self.organizer)
        self.track4.plot_graph(self.query, self.organizer)
        self.track5.plot_graph(self.query, self.organizer)


def main():
    app = QApplication(sys.argv)
    window = VizPage()
    window.setWindowTitle('Graphs')
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
