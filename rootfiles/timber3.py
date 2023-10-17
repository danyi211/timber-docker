# Start by importing the main TIMBER class, the analyzer
from TIMBER.Analyzer import analyzer
# next, import some of TIMBER's useful tools
from TIMBER.Tools.Common import *
# and pyROOT
import ROOT

if __name__ == '__main__':
    # instantiate the analyzer module. This class takes in either a ROOT file or a .txt list of ROOT files, all with the same trees (ideally)
    ana = analyzer('/home/physicist/rootfiles/ntupleSignal.root',eventsTreeName = 'muonPhiAnalyzer/tree')
  
    # We are looking at a Monte Carlo signal sample of a T' decaying to a top quark and a new scalar phi. 
    # Let's use TIMBER to define the top and phi, then use their invariant mass to reconstruct the T'
    ana.Cut('di_muon', 'muon_n >= 2')     # keep all events with at least 2 muon
#    ana.Cut('charge', 'muon_charge[0] == - muon_charge[1]')
    ana.Cut('eta_cut', 'abs(muon_eta[0]) < 2.1 && abs(muon_eta[1]) < 2.1') # drop jets in high pseudorapidity region (poor reconstruction)
    ana.Cut('pt_cut', 'muon_pt[0] >= 15 && muon_pt[1] > 15')  # drop jets with masses lower than 50 GeV
    ana.Cut('muon_dtSeg_found_cut', 'muon_dtSeg_found[0] == true && muon_dtSeg_found[1] == true')

    # Now that we've made some basic kinematic cuts, let's be a bit more specific. 
    # We'll call some custom C++ code to pick out the dijets.
    # We can compile it using TIMBER via CompileCpp, imported from TIMBER.Tools.Common above
#    CompileCpp('/home/physicist/rootfiles/Modules.cc')
    # Now we define a vector of integers for each of the events describing which (if any) of the jets in that event
    # are separated by at least 90 degrees. See the Modules.cc code for more detail. The important thing to understand
    # is that this custom function gets run on EVERY row (event), and the input to the function is that row's (event's)
    # phi vector, representing the angle of each jet in that event. 
#    ana.Define('DijetIdxs', 'PickDijets(FatJet_pt, FatJet_eta, FatJet_phi, FatJet_msoftdrop)')
#    ana.Define('PosCharge', 'muon_charge>0')
#    ana.Define('NegCharge', 'muon_charge<0')
    # Having defined this new variable, we make a cut on it, removing all rows (events) not meeting the criteria
    # PickDijets() returns {-1, -1} if there are no back-to-back jets in the event
#    ana.Cut('dijetsExist', 'DijetIdxs[0] > -1 && DijetIdxs[1] > -1')

    # Naively, let's assume that the top is the 0th index and the phi the 1st. The vectors are ordered by pt, so this is a 
    # possible, albeit inefficient, proxy for the top and phi identification
    # The ObjectFromCollection function takes a vector of vectors (FatJet_*) and makes a single vector based on the indices we defined prior (DijetIdxs)
#    ana.ObjectFromCollection('MuonPlus','Muon','PosCharge[0]')
#    ana.ObjectFromCollection('MuonNeg','Muon','NegCharge[0]')
    # At this point, we'll have a column corresponding to the Top and the Phi (defined naively based on pT). We can create TLorentz vectors from their pT, eta, phi and sotdrop masses
#    ana.Define('MuonPlus_vect','hardware::TLvector(MuonPlus_pt, MuonPlus_eta, MuonPlus_phi, MuonPlus_mass)')
#    ana.Define('MuonNeg_vect','hardware::TLvector(MuonNeg_pt, MuonNeg_eta, MuonNeg_phi, MuonNeg_mass)')
#    ana.Define('Phi_vect','hardware::TLvector(Phi_pt, Phi_eta, Phi_phi, Phi_msoftdrop)')
    # Finally, we can reconstruct the resonance by getting the invariant mass of the top and phi vectors we just defined
#    ana.Define('invMass','hardware::InvariantMass({MuonPlus_vect, MuonNeg_vect})')

    # Now, let's plot the results of our naive top/phi identification (based solely on pT of the jets)
    # Create a TCanvas on which to draw our histograms
    c = ROOT.TCanvas('c')
    c.cd()
    # Tell the canvas we want to print multiple histograms in this PDF by magic character '['
    # See https://root-forum.cern.ch/t/how-to-save-the-multiple-histogram-in-one-pdf/41252/3
    c.Print("/home/physicist/rootfiles/plotsEarthDM.pdf[")
    c.Clear()

    # The TIMBER analyzer object stores the actual RDataFrame generated from the ROOT file(s) fed into it. This means that *any* RDataFrame method that has
    # a pyROOT implemention can be accessed and used - this is especially useful when making histograms.
    # The RDataFrame has a method for generating 1D and 2D histograms from any of its columns, including ones that the user defines. So, let's use it to make
    # a 2D histogram of the Phi mass vs the resonance mass, both of which we just defined!
    # Note that the first time we access the results of our TIMBER definitions/cuts, we will execute all of the actions booked on the DataFrame. Up until that point,
    # the actions have not been executed. So, once we call Histo2D() below, all of our Define() and Cut() calls will be implemented.

    # The RDataFrame::Histo2D() constructor takes in the following arguments in pyROOT:
    # tuple: ("hist name", "hist title;x axis title;y axis title", nBinsX, xMin, xMax, nBinsY, yMin, yMax)
    # string: Column (variable) to plot on x-axis
    # string: Column (variable) to plot on y-axis
    # Note that ROOT can use LaTeX formatting in its strings, but the ROOT latex command invocation is the pound symbol (#) not the backslash (\)
    h1 = ana.DataFrame.Histo1D(('h1','#phi mass vs resonance mass - naive method;m_{res} [GeV]',150,0.,150.),'muon_pt')
    h2 = ana.DataFrame.Histo1D(('h2','#phi mass vs resonance mass - naive method;m_{res} [GeV]',150,0.,150.),'muon_pt')
    
    # This is one way of drawing the data
#    h1.Draw("COLZ")
#    c.Print('/home/physicist/rootfiles/plotsEarthDM.pdf')
#    c.Clear()
    # Now let's draw it in a different way
    h1.Draw("LEGO2")
    c.Print('/home/physicist/rootfiles/plotsEarthDM.pdf')
    c.Clear()
    h2.Draw("COLZ")
    h2.Fit("gaus","","",60,120)
    c.Print('/home/physicist/rootfiles/plotsEarthDM.pdf')
    c.Clear()
    # we're done with our multi-hist canvas, so close it out with ']'
    c.Print('/home/physicist/rootfiles/plotsEarthDM.pdf]')
