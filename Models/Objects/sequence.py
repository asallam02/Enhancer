# class to create a sequence object 
class Sequence:
    def __init__(self, sequence, time):
        self.sequence = sequence
        self.last_updated = time

    def update_sequence(self, sequence, time):
        self.sequence = sequence
        self.last_updated = time