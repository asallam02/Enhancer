#made so that the tracks.txt is only accessed once.
#This will be accessed by the front end (to get all available options)
#and the results, to find the index of the selected option

class Tracks:
    def __init__(self) -> None:
        self.legend = dict()
        input_file = "Backend/tracks.txt"

        #for each line in txt, make last number the value, and the rest of the line the key.
        with open(input_file, "r") as f:
            for line in f:
                parts = line.strip().split(" ")
                key = " ".join(parts[:-1])
                value = int(parts[-1])

                self.legend[key] = value

    def return_all_options(self):
        return(list(self.legend.keys()))
    
    def find_index(self, track: str) -> int:
        try:
            return(self.legend[track])
        except:
            print("No such key")