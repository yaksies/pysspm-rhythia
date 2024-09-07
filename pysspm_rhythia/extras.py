from pysspm import SSPMParser

def calcObsiidRating(self: SSPMParser, notes: list = None) -> SSPMParser:
    """
    calculates difficulty by using Obsiids difficulty calculation.
    This method is essentially just the dot product of the notes
    """

    print(self.Notes[1:5])

    if not notes: # if we pass in notes
        pass
    raise NotImplementedError("CalcObsiidRating function is a W.I.P.")

    return self


def calcPP(self: SSPMParser, notes) -> SSPMParser:
    """
    This calculation method is the method used in rhythia-online.
    """
    pass