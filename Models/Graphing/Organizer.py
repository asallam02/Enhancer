import Metrics as mets
"""
Class that stores and takes care of organizing the boxes with different metrics. 
Updates to the number of boxes, or box parameters are to be made here

Note: you will need to update parameters to reflect the metrics.py file
"""

class Organizer:

    def __init__(self, seq1, seq2):
        self.seq1 = seq1
        self.seq2 = seq2
        self.params = dict()
        self.colors = dict()

    def return_tracks(self):
        return self.seq1, self.seq2

    def set_defaults(self, dm, nd, hs):
        """
        sets the defaults. For now, ordering is taken care of by this object. 
        So the values can be passed in individually.
        """
        start = 0
        end = len(self.seq1)-1
        params = [start, end, dm, nd, hs]

        if ("default" not in self.params) or (self.params["default"] != params):
            self.params["default"] = params

        self.colors["default"] = "rgb(203,213,232)"

    def add_box(self, box_id, start, end, dm, nd, hs, color):
        """
        adding a new box in with distinct box_id
        """
        params = [start, end, dm, nd, hs]
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
        """
        boxes = list(self.params.keys())
        indices = dict()

        for i in boxes:
            indices[i] = self.box_calcs(i)

        return indices, self.colors

    def return_defaults(self):
        """
        Calculates the default box values first, then returns the default results for graphing
        """
        return self.box_calcs("default")
    
    def return_dims(self):
        """
        returns dimensions of all boxes
        """
        boxes = list(self.params.keys())
        dims = dict()

        for i in boxes:
            dims[i] = [self.params[i][0], self.params[i][1]]

        return dims

    def box_calcs(self, box_id):
        """
        does the calculations using the functions provided in Metrics using the box parameters for each track.
        """
        params = self.params[box_id]
        X = mets.comp(self.seq1, self.seq2, params[0], params[1], params[2])
        X = mets.clust(X, params[3])
        results = mets.elim(X, params[4])
        return results