# Start by importing the main TIMBER class, the analyzer
from TIMBER.Analyzer import analyzer
# next, import some of TIMBER's useful tools
from TIMBER.Tools.Common import *
# and pyROOT
import ROOT

if __name__ == '__main__':
    # instantiate the analyzer module. This class takes in either a ROOT file or a .txt list of ROOT files, all with the same trees (ideally)
    ana = analyzer('/home/physicist/rootfiles/nanoaod.root')
  
    print('Counts: ', ana.DataFrame.Count().GetValue())
    # Basic cuts on the events
    # keep all events with at least 2 muon
    ana.Cut('di_muon', 'nMuon >= 2')
    # drop muons in high pseudorapidity region (poor reconstruction)
    print('Counts: ', ana.DataFrame.Count().GetValue())
    ana.Cut('eta_cut', 'abs(Muon_eta[0]) < 2.1 && abs(Muon_eta[1]) < 2.1')
    print('Counts: ', ana.DataFrame.Count().GetValue())
    # drop muons with pT lower than 15 GeV
    ana.Cut('pt_cut', 'Muon_pt[0] >= 15 && Muon_pt[1] > 15')
    print('Counts: ', ana.DataFrame.Count().GetValue())
    # require quality cuts on the leaeding and sub-leading muons
    ana.Cut('highPurity_cut', 'Muon_highPurity[0] == true && Muon_highPurity[1] == true')
    print('Counts: ', ana.DataFrame.Count().GetValue())
    ana.Cut('Muon_isGlobal_cut', 'Muon_isGlobal[0] == true && Muon_isGlobal[1] == true')
    print('Counts: ', ana.DataFrame.Count().GetValue())
    ana.Cut('Muon_miniIsoId_cut', 'Muon_miniIsoId[0] >=3 && Muon_miniIsoId[1] >=3')
    print('Counts: ', ana.DataFrame.Count().GetValue())
    
    # Lot of good stuff in
    # https://github.com/ammitra/TopHBoostedAllHad/blob/master/THClass.py
    

    # Now that we've made some basic kinematic cuts, let's be a bit more specific. 
    # We'll call some custom C++ code to pick out the positively / negatively charged muons.
    # We can compile it using TIMBER via CompileCpp, imported from TIMBER.Tools.Common above
    CompileCpp('/home/physicist/rootfiles/Modules.cc')
    #See the Modules.cc code for more detail. Tthis custom function gets to run on EVERY row (event),
    # and the input to the function is that row's (event's) muon's charge in that event.
    ana.Define('OppChargeMuonsIdxs', 'PickOppChargeMuons(Muon_charge)')
    # Having defined this new variable, we make a cut on it, removing all rows (events) not meeting the criteria
    # PickOppChargeMuons() returns {-1, -1} if there opposite charge muons in the event
    ana.Cut('oppositeMuonExist', 'OppChargeMuonsIdxs[0] > -1 && OppChargeMuonsIdxs[1] > -1')
    # Naively, let's assume that the top is the 0th index and the phi the 1st. The vectors are ordered by pt, so this is a
    # possible, albeit inefficient, proxy for the top and phi identification
    # The ObjectFromCollection function takes a vector of vectors (FatJet_*) and makes a single vector based on the indices we defined prior (DijetIdxs)
    ana.ObjectFromCollection('MuonPlus','Muon','OppChargeMuonsIdxs[0]')
    ana.ObjectFromCollection('MuonNeg','Muon','OppChargeMuonsIdxs[1]')
#    ana.SubCollection('MuonPlus','Muon','OppChargeMuonsIdxs')
#    ana.SubCollection('MuonNeg','Muon','OppChargeMuonsIdxs')
    
#    ana.SubCollection('MuonNeg','Muon','OppChargeMuonsIdxs[1]')
    # At this point, we'll have a column corresponding to the pos and the neg charged muons. We can create TLorentz vectors from their pT, eta, phi and sotdrop masses
    ana.Define('MuonPlus_vect','hardware::TLvector(MuonPlus_pt, MuonPlus_eta, MuonPlus_phi, MuonPlus_mass)')
    ana.Define('MuonNeg_vect','hardware::TLvector(MuonNeg_pt, MuonNeg_eta, MuonNeg_phi, MuonNeg_mass)')
    # Finally, we can reconstruct the resonance by getting the invariant mass of the top and phi vectors we just defined
    ana.Define('invMass','hardware::InvariantMass({MuonPlus_vect, MuonNeg_vect})')

    # Now, let's plot the results of our naive top/phi identification (based solely on pT of the jets)
    # Create a TCanvas on which to draw our histograms
    c = ROOT.TCanvas('c')
    c.cd()
    # Tell the canvas we want to print multiple histograms in this PDF by magic character '['
    # See https://root-forum.cern.ch/t/how-to-save-the-multiple-histogram-in-one-pdf/41252/3
    c.Print("/home/physicist/rootfiles/plots.pdf[")
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
    h1 = ana.DataFrame.Histo2D(('h1','Invariant muon mass;m_{inv} [GeV];m_{inv} [GeV]',50,0.,150.,50,0.,150.),'invMass','invMass')
    h2 = ana.DataFrame.Histo1D(('h2','Invariant muon mass;m_{inv} [GeV]',150,0.,150.),'invMass')
    h1.Draw("LEGO2")
    c.Print('/home/physicist/rootfiles/plots.pdf')
    c.Clear()
    h2.Draw("COLZ")
    fit_result = h2.Fit("gaus","S","",60,120)
    mean = fit_result.Parameter(1)
    text = ROOT.TLatex(10,90,"Fit's mean = "+str(round(mean,2)))
    text.Draw("SAME")
    
    c.Print('/home/physicist/rootfiles/plots.pdf')
    c.Clear()
    # we're done with our multi-hist canvas, so close it out with ']'
    c.Print('/home/physicist/rootfiles/plots.pdf]')
