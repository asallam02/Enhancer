from Backend.Query import Query
from Backend.Enformer import Enformer
from Graphing.Organizer import Organizer
from Graphing.Plotter import Plotter

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

Plotter(testQuery, testOrganizer, track)



