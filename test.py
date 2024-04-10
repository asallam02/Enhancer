from Backend.Query import Query
from Backend.Enformer import Enformer
from Graphing.Organizer import Organizer
from Graphing.Plotter import Plotter

import plotly
import plotly.graph_objects as go
import plotly.io as pio

import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from flask import Flask, render_template_string
from threading import Thread

chromosome = 'chr1'
start = 1
end = 30216

model = Enformer()
testQuery = Query(chromosome, start, end, model)

#making modded and original strings 
testQuery.define_sub_seq(36,55)
testQuery.update_sub_seq("ATGGCTAACCGGATAGCTAC")
testQuery.return_mod_str()
testQuery.return_orig_str()

#running enformer stuff
testQuery.calculate_enformer()

#making organizer
track = 1
testOrganizer = Organizer(testQuery.return_orig_result(track), testQuery.return_modded(track))

#making sample boxes
testOrganizer.add_box(0, 0, 400, 0.02, 3, 4, "red")
testOrganizer.add_box(1, 600, 1000, 0.04, 5, 2, "blue")

fig = Plotter(testQuery, testOrganizer, track)

graph_html = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

print(graph_html)
def get_html():
    return graph_html
