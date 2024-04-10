from Enformer import *
from Tracks import *
from typing import List
from numpy import log10

class Result:
    """
    This class just serves as a container to hold all the enformer results
    Any modificatons to the results (log, etc) should be made here. 
    """

    def __init__(self, tracks: Tracks, orig_results, mod_results) -> None:
        self.tracks = tracks
        self.orig = orig_results
        self.mod = mod_results

    #Return user specified tracks for both original and modded
    def return_tracks(self, track: str, scale = 'linear'):
        orig_results = self.orig_results[:,self.tracks.find_index(track)]
        mod_results = self.mod_results[:,self.tracks.find_index(track)]

        #add scaling options here
        match scale:
            case 'linear':
                pass
            case 'log10':
                orig_results = log10(1+ orig_results)
                mod_results = log10(1+ mod_results)

        return orig_results, mod_results

