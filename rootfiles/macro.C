// First we include libraries with functions we want (like import in Python)
#include <iostream>
#include "TCanvas.h"	// used for making a canvas for our histogram to be drawn on
#include "TFile.h"	// used to read/write ROOT files
#include "TTree.h"	// used to access TTrees in TFiles

void macro() {
    /* 
     * This is our function that ROOT will compile and run 
    */
    // open the file    
    TFile *f = TFile::Open("/home/physicist/rootfiles/TprimeB-1800-125.root");	// lines must end with ;
    // book an empty histogram (1d histogram of floating point values)
    // constructor takes name, 'title;x title;y title', nBins, min, max
    TH1F *myh = new TH1F("m_sd", "softdrop mass;m_{SD} (GeV);N_{Events}", 400, 0, 400);
    // Get the Events TTree
    TTree *t = (TTree*)f->Get("Events");
    // create a canvas to draw it onto
    TCanvas *c = new TCanvas("c","c");
    c->cd();
    c->Clear();
    // Draw the desired column into the histogram we booked via >> operator
    t->Draw("FatJet_msoftdrop>>m_sd");
    // draw histo, will populate the canvas
    myh->Draw();
    // print canvas, save file
    c->Print("/home/physicist/rootfiles/macro_output.pdf");
}
