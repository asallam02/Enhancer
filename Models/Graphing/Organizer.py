import sys
sys.path.append("..")

from .Metrics import *
"""
Class that stores and takes care of organizing the boxes with different metrics. 
Updates to the number of boxes, or box parameters are to be made here

Note: you will need to update parameters to reflect the metrics.py file
"""

class Organizer:

    #takes a result object, see backend
    def __init__(self, original, modded, start):
        #get these from the query object
        self.original = original 
        self.modded = modded
        self.startpos = start

        self.params = dict()
        self.colors = dict()

    def add_box(self, box_id, start, end, dm, nd, hs, color):
        """
        adding a new box in with distinct box_id
        """
        params = [int((start - self.startpos)/128), int((end-self.startpos)/128), dm, nd, hs]
        if (box_id not in self.params) or (self.params[box_id] != params):
            self.params[box_id] = params

        self.colors[box_id] = color

    def del_box(self,box_id):
        """
        deletes specified box if it exists
        """
        if box_id in self.params:
            del self.params[box_id]
            del self.colors[box_id]

    def return_boxes(self):
        """
        Calculates the box values first, then returns the boxes results for graphing. 
        Does this for the specified track index. 
        """
        self.box_calcs()
        return self.indices

    
    def return_dims(self):
        """
        returns dimensions of all boxes
        """
        boxes = list(self.params.keys())
        dims = dict()

        for i in boxes:
            dims[i] = [self.params[i][0], self.params[i][1]]

        return dims
    

    def return_colors(self):
        return self.colors


    def box_calcs(self):
        """
        does the calculations using the functions provided in Metrics using the box parameters for specified track.
        """
        boxes = list(self.params.keys())
        self.indices = dict()
        for i in boxes:
            params = self.params[i]
            X = comp(self.original, self.modded, params[0], params[1], params[2])
            X = clust(X, params[3])
            results = elim(X, params[4])
            self.indices[i] = results