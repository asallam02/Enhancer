import sys
sys.path.append("..")

from Backend.USCS_connect import *
from math import ceil, floor
import numpy as np

SEQUENCE_LENGTH = 393216

class Query:

    def __init__(self, chromosome: str, start: int, end: int, enformer_model):
        """
        Upon initialization, calls the extract method to retrieve data from NCBI
        the data in question uses hg38. 
        """
        self.model = enformer_model

        #for the demo, we just set the tracks to 5 chosen ones instead of 5000.
        #an improvement in the future would involve making this settable. 
        #We have no idea how we could ge the user to chose out of 5000 options.

        self.tracks = [41, 147, 188, 1085, 5050]

        #THESE ARE THE MAIN VARIABLES, NEED RETURN FUNCTIONS
        self.seq_str = ""
        self.genes = []
        self.chromosome = None
        self.start = None
        self.end = None
        self.final_str = ""
        self.orig_result = None
        self.modded_result = None

        self.sub_str = ""
        self.sub_str_start = 0
        self.sub_str_end = 0

        self.extract(chromosome, start, end)


    def extract(self, chromosome: str, start: int, end: int):
        """
        Gets the interval on which Enformer will run. 
        assumes that start is strictly greater or equal to zero
        and that end is greater or equal to  start
        """

        #checking to see if any values have actually changed
        if (self.chromosome != chromosome or self.start != start or self.end != end):
            #get fasta 
            self.seq_str = get_fasta(chromosome, start, end).upper()
            #get genes in region
            self.genes = get_genes(chromosome, start, end)

            #update self values
            self.chromosome = chromosome
            self.start = start
            self.end = end


    def define_sub_seq(self, sub_start, sub_end) -> str:
        """
        Defines the subsequence region that will be patched onto before Enformer is run
        This allows the user to change certain regions of the fasta sequence

        Also returns what is currently at that location. 
        """
        if (sub_start >= self.start) and (sub_end <= self.end):

            #storing string indices of substring start and end (inclusive)
            self.sub_str_start = (sub_start - self.start)
            self.sub_str_end = self.sub_str_start + (sub_end - sub_start)

            #returning the substring for user viewing
            return self.seq_str[self.sub_str_start:self.sub_str_end+1]
        else:
            pass 


    def update_sub_seq(self, new_substr):
        """
        takes in a user input intended to replace the subsequence
        """
        self.sub_str = new_substr
    
    
    def return_mod_str(self) -> str:
        #the sub_sequence is only put onto the actual sequence at the last moment, to prevent errors
        self.final_str = self.seq_str[0:self.sub_str_start+1] + self.sub_str + self.seq_str[self.sub_str_end+1:]
        #gotta do some padding to make sequence the appropriate length
        current_length = len(self.final_str)
        length_diff = SEQUENCE_LENGTH - current_length

        #for positive length difference, ie the given sequence is shorter than allowed.
        if length_diff > 0:
            addleft = int(floor(length_diff/2))
            addright = int(ceil(length_diff/2))

            pad_upstream = 'N' * addleft
            pad_downstream = 'N' * addright

            self.final_str = pad_upstream + self.final_str + pad_downstream

        #takes care of negative difference, ie the given sequence is now larger than allowed
        if length_diff < 0:
            removeleft = int(floor(-length_diff/2))
            removeright = int(ceil(-length_diff/2))

            self.final_str = self.final_str[removeleft: -removeright]

        return self.final_str
    
    
    def return_orig_str(self)-> str:
        current_length = len(self.seq_str)
        length_diff = SEQUENCE_LENGTH - current_length

        #for positive length difference, ie the given sequence is shorter than allowed.
        if length_diff > 0:
            addleft = int(floor(length_diff/2))
            addright = int(ceil(length_diff/2))

            pad_upstream = 'N' * addleft
            pad_downstream = 'N' * addright

            self.seq_str = pad_upstream + self.seq_str + pad_downstream

        #takes care of negative difference, ie the given sequence is now larger than allowed
        if length_diff < 0:
            removeleft = int(floor(-length_diff/2))
            removeright = int(ceil(-length_diff/2))

            self.seq_str = self.seq_str[removeleft: -removeright]

        return self.seq_str
    
    def calculate_enformer(self):
        #slicing to get desireed tracks. 
        self.orig_result = self.model.enform(self.seq_str)[:, self.tracks]
        self.modded = self.model.enform(self.final_str)[:, self.tracks]

    def return_genes(self):
        return self.genes
    
    def return_orig_result(self, track_no):
        return self.orig_result[:, track_no]
    
    def return_modded(self, track_no):
        return self.modded[:, track_no]
    
    
        
