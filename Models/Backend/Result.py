from Enformer import *
from Tracks import *
from typing import List
from numpy import log10

class Result:
    """
    This class just serves as a container to hold all the enformer results
    Any modificatons to the results (log, etc) should be made here. 
    """

    def __init__(self, tracks: Tracks, results) -> None:
        self.tracks = tracks
        self.results = results

    def return_tracks(self, track_list: List[str], scale = 'linear'):
        values = dict()

        for track in track_list:
            track_results = self.results[:,self.tracks.find_index(track)]

            #add scaling options here
            match scale:
                case 'linear':
                    pass
                case 'log10':
                    track_results = log10(1+ track_results)

            values[track] = track_results

        return values

