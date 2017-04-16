import commentCompiler
import pickle

load = open("DBsave.pickle", "r")

DBUnpickle = pickle.load(load)

load.close()

for d in DBUnpickle:
    for p in DBUnpickle[d]:
        print DBUnpickle[d][p]
