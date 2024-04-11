import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
import plotly.graph_objs as go
from Models.Graphing.Plotter import Plotter

class GraphTab(QWidget):
    def __init__(self, track_no, parent=None):
        self.track = track_no
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.webview = QWebEngineView()
        layout.addWidget(self.webview)
        self.setLayout(layout)

    def plot_graph(self, query, organizer):
        # Example graph plotting with Plotly
        # x = [1, 2, 3, 4, 5]
        # y = [10, 11, 12, 13, 14]
        # data = [go.Scatter(x=x, y=y, mode='lines')]
        # layout = go.Layout(title='Enformer Graph')
        # fig = go.Figure(data=data, layout=layout)
        fig = Plotter(query, organizer, self.track)

        # Convert Plotly figure to HTML
        plotly_html = fig.to_html(include_plotlyjs='cdn')
        self.webview.setHtml(plotly_html)

class VizPage(QWidget):
    organizer = None
    query = None

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        # Create tabs and add them to the tab widget
        self.track1 = GraphTab(1)
        self.track2 = GraphTab(2)
        self.track3 = GraphTab(3)
        self.track4 = GraphTab(4)
        self.track5 = GraphTab(5)

        self.tabs.addTab(self.track1, "Track 1")
        self.tabs.addTab(self.track2, "Track 2")
        self.tabs.addTab(self.track3, "Track 3")
        self.tabs.addTab(self.track4, "Track 4")
        self.tabs.addTab(self.track5, "Track 5")

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
