# this will call pyROOT, one of the python wrappers for ROOT
import ROOT

# this is the main function. It will be run when you call this script via the command line.
# While not strictly necessary, it's good practice to have one of these
if __name__ == '__main__':
    # first let's replicate what we did in the C++ macro, but in python
    # compare this code to the C++ code and try to understand how it works.

    # open the file, get the events TTree
    f = ROOT.TFile.Open("/home/physicist/rootfiles/TprimeB-1800-125.root")
    events = f.Get("Events")

    # book empty histogram
    hist = ROOT.TH1F("m_sd", "softdrop mass;m_{SD} (GeV);N_{Events}", 400, 0, 400)

    # create a canvas
    c = ROOT.TCanvas('c','c')
    c.cd()
    c.Clear()

    # draw from TTree into histo
    events.Draw("FatJet_msoftdrop>>m_sd") # unlike macro, no need to book a hist first!
    hist.Draw()  # draw the hist
    c.Print("/home/physicist/rootfiles/python_output.pdf")

    # just for illustration, here are all the various varaibles we just created:
    print('--------------------------------------------------------------')
    print(' Variable     |       Type                                   |')
    print('--------------------------------------------------------------')
    print('   f:            {}'.format(type(f)))
    print('   events:       {}'.format(type(events)))
    print('   c:            {}'.format(type(c)))
    print('   hist:         {}'.format(type(hist)))
    print('--------------------------------------------------------------')
