# Start by importing the main TIMBER class, the analyzer
from TIMBER.Analyzer import analyzer
# next, import some of TIMBER's useful tools
from TIMBER.Tools.Common import *
# and pyROOT
import ROOT

if __name__ == "__main__":
    # instantiate the analyzer module. This class takes in either a ROOT file or a .txt list of ROOT files, all with the same trees (ideally)
    ana = analyzer("/home/physicist/rootfiles/TprimeB-1800-125.root")

    # let's look at using the analyzer to filter events
    # Let's filter all jets which have a softdrop mass inside of the higgs mass window
    # this defines a new variable of all jets meeting the mass requirement
    ana.Define("higgs_like", "FatJet_msoftdrop > 100 && FatJet_msoftdrop < 150")
    # now let's plot it, using the analyzer's built-in RDataFrame!
    c = ROOT.TCanvas('c','c')
    c.cd()
    c.Clear()
    # we defined the variable earlier, now we reference it.
    hist = ana.DataFrame.Histo1D("higgs_like")  # the above filter will now be executed, before it was only booked
    hist.Draw()
    c.Print("/home/physicist/rootfiles/timber_define1.pdf")
