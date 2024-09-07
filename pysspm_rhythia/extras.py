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


def calcStarRating(self: SSPMParser, notes) -> float:
    """
    This calculation method is the method used in rhythia-online. | May change in future updates
    """
    return len(self.Notes) / 100 