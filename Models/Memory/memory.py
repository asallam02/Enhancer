import os

## TODO: update and test this class

# class to handle memory for sessions and sequences
class Memory:
    _dir = "./"
    _sessionName = ""
    _sequences = []

    def __init__(self, dir = "./"):
        self._dir = dir

    # change root dir based on input
    def change_root_dir(self, dir):
        # probably need to do os.chdir()
        self._dir = dir

    # create a new folder for the session
    def create_session(self, sessionName = None):
        # if session name is none: make it sessionX (with X being whatever number works)
        if sessionName == None:
            sessionName = "session1"
            sessionNum = 1
            while(os.path.exists(self._dir + "/" + sessionName)):
                sessionNum += 1
                sessionName = "session" + str(sessionNum)
        
        self._sessionName = sessionName
        os.makedirs(self._dir + sessionName)

    # set the directory and session name based on inputs
    # set the sequences based on the file names
    def open_session(self, dir, sessionName):
        self.change_root_dir(dir)
        self._sessionName = sessionName

        # get all the file names in that directory
        # store them in the sequences array
        self._sequences = os.listdir(dir + sessionName)


    # save a sequence
    def save_seq(self, sequence, MLOutput, fileName = None):
        # create a fileName if it doesn't exist
        if fileName == None:
            fileName = "sequence1"
            sequenceNum = 1
            while(os.path.exists(self._dir + "/" + self._sessionName + "/" + fileName)):
                sequenceNum += 1
                fileName = "sequence" + str(sequenceNum)
        
        # create the file, write the sequence and output to it 
        fp = open(self._dir + "/" + self._sessionName + "/" + fileName, "w")
        fp.write(sequence)
        fp.write(" ") # whitespace to parse 
        fp.write(MLOutput) # this one is probably wrong should double check based on the actual output
        fp.close()

    # open sequence file
    def open_seq(self, fileName):
        # open a sequence based on the file name
        # return the sequence and enformer results
        fp = open(self._dir + "/" + self._sessionName + "/" + fileName)
        sequence = fp.read()
        fp.read()
        MLOutput = fp.read()
        return sequence, MLOutput

    # delete sequence
    def delete_seq(self, fileName):
        os.remove(self._dir + "/" + self._sessionName + "/" + fileName)
        pass
    
    # delete session
    def delete_session(self, sessionName):
        # make sure we're in the right session
        if(sessionName != self._sessionName):
            return
        
        # delete all the sequences, then remove directory
        for sequence in self._sequences:
            self.delete_seq(sequence)
        os.rmdir(self._dir + "/" + sessionName)


if __name__ == "__main__":
    memory = Memory()
    print("created memory object")