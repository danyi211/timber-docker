#!/usr/bin/python3

import ROOT
import sys
import os

QCDSamples = [
    "GenJet_QCD_HT50to100.root",
    "GenJet_QCD_HT100to200.root",
    "GenJet_QCD_HT200to300.root",
    "GenJet_QCD_HT300to500.root",
    "GenJet_QCD_HT500to700.root",
    "GenJet_QCD_HT700to1000.root",
    "GenJet_QCD_HT1000to1500.root",
    "GenJet_QCD_HT1500to2000.root",
    "GenJet_QCD_HT2000toInf.root"
]

# unit fb-1
crossSectionArray = {
    "GenJet_QCD_HT50to100.root" : 187700000.0,  # +-1639000
    "GenJet_QCD_HT100to200.root" : 23500000.0,  # +-207400
    "GenJet_QCD_HT200to300.root" : 1552000.0,  # +-14450.0
    "GenJet_QCD_HT300to500.root" : 321100.0,  # +-2968.0
    "GenJet_QCD_HT500to700.root" : 30250.0,  # +-284.0
    "GenJet_QCD_HT700to1000.root" : 6398.0,  # +-59.32
    "GenJet_QCD_HT1000to1500.root" : 1122.0,  # +- 10.41
    "GenJet_QCD_HT1500to2000.root" : 109.4,  # +-1.006
    "GenJet_QCD_HT2000toInf.root" : 21.74, # +-0.2019
}

if __name__ == '__main__':
    
    intLumi = 100000.0 #100/fb
    
    fileInArray = []
    for sample in QCDSamples:
        sample = "plots_fullSample_rescale/" + sample
        if not os.path.exists(sample): continue
        fileInArray.append(ROOT.TFile.Open(sample,"UPDATE"))
    
    for fileIn in fileInArray:
        if not (fileIn.Get("GenJet_HT")):
            print("GenJet_HT not found, exit for "+str(fileIn))
            continue
        nEvetsPreTrig = fileIn.Get("GenJet_HT").Integral()
        if (nEvetsPreTrig == 0):
            print("nEvetsPreTrig is zero, exiting")
            continue
        # str(TFile) = 'Name: plots/GenJet_QCD_HT50to100.root Title: '
        nameFromTFile = str(fileIn)[str(fileIn).find("Name")+6:str(fileIn).find("Title")-1]
        basename = nameFromTFile.split("/")[-1]
        if not (crossSectionArray.get(basename)):
            print("No crossSectionArray for "+str(nameFromTFile))
            continue
        
        # rescale weight
        weight = intLumi * crossSectionArray.get(basename) / nEvetsPreTrig
        print(nameFromTFile+" is reweighted with " + str(weight))
        if (abs(1-weight) < 0.0001) : continue
        
        for i in range(0, fileIn.GetListOfKeys().GetEntries()):
            name = fileIn.GetListOfKeys().At(i).GetName()
            obj = fileIn.Get(name)
            if not (obj) : continue
            if (obj.GetEntries() == 0 ) : continue
            if obj.InheritsFrom("TObject"):
                obj.Scale(weight)

        fileIn.Write("",ROOT.TObject.kOverwrite)
        fileIn.Close()
    