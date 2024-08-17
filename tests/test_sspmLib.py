from pysspm_rhythia import SSPMParser
import pandas as pd
import glob


# W.I.P

parser = SSPMParser()

parser.ReadSSPM("./tests/Test.sspm")
print(len(parser.Notes))
print(parser.Notes[1000:1020])
#parser.mapName = "KOCMOC_MAP_TESTING_SSPMLIB"
parser.WriteSSPM("./tests/Test2.sspm", mapName="KOCMOC_MAP_TESTING_SSPMLIB")

parser.ReadSSPM("./tests/Test2.sspm") # if we can open it again then its good.
print("-----------------------")
print(len(parser.Notes))
print(parser.Notes[1000:1020])