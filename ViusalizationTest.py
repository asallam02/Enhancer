import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
import plotly.graph_objects as go
import plotly.io as pio

import plotly.express as px
import subprocess

def generate_plotly_graph_html():
    # Run test.py and capture its stdout output
    result = subprocess.run(['python', 'test.py'], capture_output=True, text=True)
    
    # The HTML string is in result.stdout
    return result.stdout

class GraphWindow(QMainWindow):
    def __init__(self, graph_html):
        super().__init__()
        self.setWindowTitle("Plotly Graph")
        self.setGeometry(100, 100, 800, 600)
        
        # Create a QWebEngineView widget
        self.webEngineView = QWebEngineView()
        self.setCentralWidget(self.webEngineView)
        
        # Load the Plotly graph HTML
        self.webEngineView.setHtml(graph_html)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    graph_html = generate_plotly_graph_html()
    mainWindow = GraphWindow(graph_html)
    mainWindow.show()
    
    sys.exit(app.exec())
