from pysspm_rhythia import SSPMParser
import pandas as pd
import glob


# W.I.P

parser = SSPMParser()

# function for using pytest
def test_read_sspm(): # Basic reading of sspm file format
    parser = SSPMParser()
    parser.ReadSSPM("./tests/Test.sspm")
    assert len(parser.Notes) > 0

# now we read and write the notes to a new sspm file.
def test_write_sspm(): # Writing a new SSPM file from parsed notes
    parser = SSPMParser()
    first = parser.ReadSSPM("./tests/Test.sspm")
    parser.WriteSSPM("./tests/Test2.sspm", mapName="KOCMOC_MAP_TESTING_SSPMLIB")
    second = parser.ReadSSPM("./tests/Test.sspm")

    # comparing values between first and second. should all be the same
    assert first.audioBytes == second.audioBytes
    print("Audio checked")
    assert first.Notes == second.Notes
    print("Notes checked")
    assert first.lastMs == second.lastMs
    assert first.coverBytes == second.coverBytes
    
# This last test starts from scratch, and applies all the values into the write function.
def test_write_sspm_from_scratch(): # Writing a new SSPM file from scratch
    parser = SSPMParser()
    parser.ReadSSPM("./tests/Test.sspm")

# Read the SSPM file and parse it into a list of notes.
parser.ReadSSPM("./tests/Test.sspm")
print(len(parser.Notes))
print(parser.Notes[1000:1020])
#parser.mapName = "KOCMOC_MAP_TESTING_SSPMLIB"
parser.WriteSSPM("./tests/Test2.sspm", mapName="KOCMOC_MAP_TESTING_SSPMLIB")

parser.ReadSSPM("./tests/Test2.sspm") # if we can open it again then its good.
print("-----------------------")
print(len(parser.Notes))
print(parser.Notes[1000:1020])