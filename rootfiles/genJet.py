#!/usr/bin/python3

# Start by importing the main TIMBER class, the analyzer
from TIMBER.Analyzer import analyzer
# next, import some of TIMBER's useful tools
from TIMBER.Tools.Common import *
# and pyROOT
import ROOT
import sys

if __name__ == '__main__':
    
    if len(sys.argv) >= 3:
        print(f"argumrnts:{sys.argv[1]}---{sys.argv[2]}")
        fileDir = sys.argv[1]
        prc = sys.argv[2]
        print(f"Process type: {prc}")
    else:
        print("Usage: python3 genJet.py PATH_TO_NTUPLE PROCESS_NAME")
        exit()

    ana = analyzer(fileDir)
    max_nJets = int(ana.DataFrame.Max('nGenJet').GetValue())
    min_nJets = int(ana.DataFrame.Min('nGenJet').GetValue())
    print("Maximum and minimum nGenJet are ", min_nJets, max_nJets)
    
    # compile modules
    CompileCpp('Modules.cc')
    
    # define new variables
    ana.Define('GenJet_HT','sumJetPt(GenJet_pt)')
    
    hist_dict = {
        'nJet' : None,
        'GenJet_HT' : None,
    }
    
    # histo pre nJet cut
    hist_dict['nJet'] = ana.DataFrame.Histo1D(('nGenJet','Number of GenJet;nGenJet',30,0.,30),'nGenJet')
    hist_dict['GenJet_HT'] = ana.DataFrame.Histo1D(('GenJet_HT','Scalar sum of GenJet p_{T};GenJet_HT [GeV]',250,0.,5000.),'GenJet_HT')
    
    preJetCutNode = ana.GetActiveNode()
    
    for nJet in range(min_nJets, max_nJets+1):
        print(f'---------- Filtering for nGenJet == {nJet} ----------')
        ana.SetActiveNode(preJetCutNode)
        print('Counts: ', ana.DataFrame.Count().GetValue())
        # keep all events with at exactly n gen jets
        ana.Cut(f'{nJet}GenJet_cut', f'nGenJet == {nJet}')
        print('Counts after cut: ', ana.DataFrame.Count().GetValue())
    
        hist_dict[f'{nJet}Jet_eta']  = ana.DataFrame.Histo1D((f'{nJet}GenJet_eta' ,f'{nJet} GenJet #eta;GenJet #eta',100,-6.,6.),'GenJet_eta')
        hist_dict[f'{nJet}Jet_phi']  = ana.DataFrame.Histo1D((f'{nJet}GenJet_phi' ,f'{nJet} GenJet #phi;GenJet #phi',100,-4.,4.),'GenJet_phi')
        hist_dict[f'{nJet}Jet_pt']   = ana.DataFrame.Histo1D((f'{nJet}GenJet_pt'  ,'%d GenJet p_{T};GenJet p_{T} [GeV]' % nJet,250,0.,5000.),'GenJet_pt')
        hist_dict[f'{nJet}Jet_mass'] = ana.DataFrame.Histo1D((f'{nJet}GenJet_mass',f'{nJet} GenJet mass;GenJet mass [GeV]',100,0.,400.),'GenJet_mass')
    
    
    outfile_name = f'/home/physicist/rootfiles/plots/GenJet_{prc}'
    outfile = ROOT.TFile(f"{outfile_name}.root", "RECREATE")
    for key, h in hist_dict.items():
        h.Write()
    outfile.Close()

'''
    # Make histograms
    maxPt = ana.DataFrame.Max('GenJet_pt').GetValue()
    maxMass = ana.DataFrame.Max('GenJet_mass').GetValue()
    # print("Max pT is {}".format(maxPt))
    maxPt = 50 * round(maxPt/50)
    maxMass = 50 * round(maxMass/50)
    if fileDir.find("WJets") >= 0:
        maxPt = 300
        maxMass = 30
'''