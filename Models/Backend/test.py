from Enformer import Enformer
from Query import Query
from Result import Result 
from Tracks import Tracks
from USCS_connect import *

chromosome = 'chr1'
start = 1
end = 393216
fasta = get_fasta(chromosome, start, end).upper()
print(fasta)
genes = get_genes(chromosome, start, end)
print(genes)

#testing Query object
# testQuery = Query(chromosome, start, end)
# print(testQuery.patch())

#testing buffing with 10 N on each end
# testQuery = Query(chromosome, start, end-20)
# results = testQuery.patch()
# print(results[:100])
# print(results[-100:]) 

#testing reduction by 10 chars
# testQuery = Query(chromosome, start, end+20)
# results = testQuery.patch()
# print(results[-100:]) 
# print(fasta[-100:])

#testing addition of 20 characters
testQuery = Query(chromosome, start, end)
testQuery.define_sub_seq(36,55)
testQuery.update_sub_seq("ATGGCTAACCGGATAGCTAC")
seq = testQuery.patch()
print(fasta[:60])
print(seq[:60])


Enformertest = Enformer()
results = Enformertest.enform(seq)

testTracks = Tracks()
testkey = testTracks.return_all_options()[10]
print(testkey)

testResult = Result(testTracks, results)
print(testResult.return_tracks([testkey]))




