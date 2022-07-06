import createSingleDataset
import readDataset
import os

pr = os.fork()
# TODO: check for exceptions here
if pr == 0:
    readDataset.run()
else:
    cpe = os.wait()
    createSingleDataset.merge_json_files()
