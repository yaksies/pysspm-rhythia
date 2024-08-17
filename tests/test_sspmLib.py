from sspmLib import SSPMParser
import pandas as pd
import glob


# W.I.P

parser = SSPMParser()

#parser.ReadSSPM(r"")
print(len(parser.Notes))
print(parser.Notes[1000:1020])
parser.mapName = "KOCMOC_MAP_TESTING_SSPMLIB"
with open("test.sspm", 'wb') as f:
    f.write(parser.WriteSSPM())

parser.ReadSSPM(r"test.sspm") # if we can open it again then its good.
print("-----------------------")
print(len(parser.Notes))
print(parser.Notes[1000:1020])
# csv = pd.DataFrame()
# 
# for sspm in glob(r""):
#     parser.ReadSSPM(sspm)
# 
"""
with open("cover.png", 'wb') as f:
    f.write(parser.coverBytes)

with open("audio.mp3", "wb") as f:
    f.write(parser.audioBytes)


input("Completed")"""