// Root RVectors are the default type of vector used in RDataFrames
#include "ROOT/RVec.hxx"
// Get some of the functions provided by TIMBER in the hardware namespace
#include "TIMBER/Framework/include/common.h"

/* namespaces allow us to provide a scope to functions, variables, etc
 * Instead of having to type out ROOT::VecOps::RVec every time we want an RVector,
 * now we can just type RVec. Be careful though, because using namespaces can 
 * come into conflict with other functions outside of the namespace with the same name */
using namespace ROOT::VecOps;

/* Here we define our first function. 
 * We first declare what the function returns - in this case a vector of integers.
 * We then declare the function name and its arguments. 
 * This function just looks at the angle phi between the two jets and makes sure that 
 * they are at least 90 degrees apart 
 *
 * Each RVec<int> input can have a different size. When we call this function via TIMBER,
 * what's actually happening under the hood is that it applies this function to *every* 
 * event (row) in the dataframe. Each event may have more than two jets. For example, if 
 * an event has 4 jets, it's phi vector that gets passed to this function will look like:
 * 	{phi0, phi1, phi2, phi3}
 * corresponding to the measured phi of each of the four jets.
 * */
RVec<int> PickDijets(RVec<float> pt, RVec<float> eta, RVec<float> phi, RVec<float> mass) {
    // initialize two integers representing indices to test values
    int jet0Idx = -1;
    int jet1Idx = -1;
    // For-loops in C++ first specify the index to loop over (ijet=0)
    // Then they specify how long to loop (less than the size of the input vector phi)
    // Then they increment the iterator by one after the end of all statements (ijet++)
    for (int ijet=0; ijet<phi.size(); ijet++) {
	// begin loop over all jets in the event. We are going to compare the angle of the 0th
	// jet to all other jets in the event and see if they are separated by at least pi/2
	if (jet1Idx == -1) {	// we haven't yet found a jet that meets our criteria
	    if (pt[ijet] > 350 && std::abs(eta[ijet]) < 2.4 && mass[ijet] > 50) {
		if (jet0Idx == -1) {
		    jet0Idx = ijet;
		}
		else {
		    if (hardware::DeltaPhi(phi[jet0Idx], phi[ijet]) > M_PI/2) {
			jet1Idx = ijet;
			break;
		    }
		}
	    }
	}
    }
    // The loop has now fully ended. We return the vector of integers representing the indices of
    // the two jets that are at least 90 degrees apart.
    // If none of the jets in the event are 90 degrees apart, return {-1, -1}
    // Otherwise, we found two jets matching our criteria, return their indices in the original vector.
    // Going back to our example of an input vector of four jets, if jets 0 and 2 were at least 90 degrees
    // apart, we'd return:
    // 		input:    {jet0, jet1, jet2, jet3}
    // 			    ^           ^
    // 			(these two meet our criteria)
    // 		return:		{0,2}
    return {jet0Idx, jet1Idx};
};

// This is the function for picking which jets are top ID'd. We will take in the indices (idxs) of the jets we defined to be 
// separated by at least 90 degrees above, then determine which (if not both) belong to the top jet based on  whether it's in the 
// top mass window [105, 210] GeV and has the requisite TvsQCD score (nominally > 0.94)
RVec<int> PickTop(RVec<float> mass, RVec<float> tagScore, RVec<int> idxs, std::pair<float,float> massCut, float scoreCut) {
    if (idxs.size() > 2) {
	std::cout << "PickTop -- WARNING: You have input more than two indices. Only two accepted. Assuming first two indices.";
    }
    // create a vector to hold the values of the indices of our top jet(s)
    RVec<int> out(2);	    // specify that it contains 2 indices
    float WP = scoreCut;    // store the Working Point we use for the top ID threshold

    // get the values of the indices assigned to our compatible (90deg separation) jets
    int idx0 = idxs[0];
    int idx1 = idxs[1];
    // get the values of the min and max of our top mass window
    float m_min = massCut.first;	// first, second are how to access indices of the std::pair data type. I suppose one could make massCut a vector instead
    float m_max = massCut.second;
    // store logic to determine whether top jet is 0th index or 1st index
    bool isTop0, isTop1;

    // main logic for determining which index belongs to the top jet
    isTop0 = (mass[idx0] > m_min) && (mass[idx0] < m_max) && (tagScore[idx0] > WP);
    isTop0 = (mass[idx1] > m_min) && (mass[idx1] < m_max) && (tagScore[idx1] > WP);

    // now apply logic for ordering the resulting index output vector
    if (isTop0 && isTop1) {	// then both jets pass our top ID
	// we will order them based on which has higher top score
	if (tagScore[idx0] > tagScore[idx1]) {	// index 0 jet has higher TvsQCD score
	    out[0] = idx0;
	    out[1] = idx1;
	}
	else {	// index 1 jet has higher TvsQCD score
	    out[0] = idx1;
	    out[1] = idx0;
	}
    }
    else if (isTop0) {	// only index 0 jet met top requirements
        out[0] = idx0;
        out[1] = idx1;
    }
    else if (isTop1) {	// only index 1 jet met top requirements
        out[0] = idx1;
        out[1] = idx0;
    }
    else {	// neither jet met top requirements
        out[0] = -1;
        out[1] = -1;
    }
    // we are done, return the vector of the indices of jets meeting top tag
    return out;
};
