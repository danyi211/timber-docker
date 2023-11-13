#!/usr/bin/python3

import ROOT
import os

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetPadRightMargin(.15)
ROOT.gStyle.SetPadTopMargin(0.1)
ROOT.gStyle.SetPadBottomMargin(0.14)
ROOT.gStyle.SetPadLeftMargin(0.15)

# colors
color_comp1=634    # kRed+2
color_comp2=862    # kAzure+2
color_comp3=797    # kOrange-3
color_comp4=882    # kViolet+2
color_comp5=419    # kGreen+3
color_comp6=603    # kBlue+3
color_comp7=802    # kOrange+2
color_comp8=616    # kMagenta
color_comp9=600    # kBlue
color_comp10=434   # kCyan+2
color_comp11=800   # kOrange
color_comp12=417   # kGreen+1
color_comp13=632   # kRed

colors = {}
colors['color_comp1'] = color_comp1
colors['color_comp2'] = color_comp2
colors['color_comp3'] = color_comp3
colors['color_comp4'] = color_comp4
colors['color_comp5'] = color_comp5
colors['color_comp6'] = color_comp6
colors['color_comp7'] = color_comp7
colors['color_comp8'] = color_comp8
colors['color_comp9'] = color_comp9
colors['color_comp10'] = color_comp10
colors['color_comp11'] = color_comp11
colors['color_comp12'] = color_comp12
colors['color_comp13'] = color_comp13

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

if __name__ == '__main__':
    fileInArray = []
    
    for sample in QCDSamples:
        sample = "plots_fullSample_rescale/" + sample
        if not os.path.exists(sample): continue
        fileInArray.append(ROOT.TFile.Open(sample,"READ"))
    
    ROOT.gStyle.SetOptStat(0)
    can = ROOT.TCanvas("can", "", 800, 600)
    can.SetLogy()
    # can.SetLogx()
    leg = ROOT.TLegend(0.5, 0.6, 0.85, 0.9)
    
    i = 0
    for fileIn in fileInArray:
        # str(TFile) = 'Name: plots/GenJet_QCD_HT50to100.root Title: '
        nameFromTFile = str(fileIn)[str(fileIn).find("Name")+6:str(fileIn).find("Title")-1]
        basename = nameFromTFile.split("/")[-1]
        label = basename.split(".root")[0]
        
        hist = fileIn.Get("GenJet_HT")
        hist.GetYaxis().SetTitle("Scale to 100 fb^{-1}")
        hist.Draw("hist same")
        hist.SetLineColor(colors['color_comp{}'.format(i+1)])
        hist.SetLineWidth(2)
        hist.GetYaxis().SetRangeUser(1e2, 1e13)
        
        leg.AddEntry(hist, label)
        leg.Draw("same")
        
        i += 1
    
    can.Print("plots/QCD_HT_fullSample_rescale100ifb.png")