import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
import plotly.graph_objs as go

class GraphTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.webview = QWebEngineView()
        layout.addWidget(self.webview)
        self.setLayout(layout)

    def plot_graph(self):
        # Example graph plotting with Plotly
        x = [1, 2, 3, 4, 5]
        y = [10, 11, 12, 13, 14]
        data = [go.Scatter(x=x, y=y, mode='lines')]
        layout = go.Layout(title='Enformer Graph')
        fig = go.Figure(data=data, layout=layout)

        # Convert Plotly figure to HTML
        plotly_html = fig.to_html(include_plotlyjs='cdn')
        self.webview.setHtml(plotly_html)

class VizPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        # Create tabs and add them to the tab widget
        tab1 = GraphTab()
        tab2 = GraphTab()
        tab3 = GraphTab()

        self.tabs.addTab(tab1, "Graph 1")
        self.tabs.addTab(tab2, "Graph 2")
        self.tabs.addTab(tab3, "Graph 3")

        layout.addWidget(self.tabs)
        self.setLayout(layout)

        # Plot initial graphs
        tab1.plot_graph()
        tab2.plot_graph()
        tab3.plot_graph()


def main():
    app = QApplication(sys.argv)
    window = VizPage()
    window.setWindowTitle('Graphs')
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
