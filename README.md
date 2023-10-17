# TIMBER in a container
This repository contains the Dockerfile used to create a container running [TIMBER](https://github.com/lcorcodilos/TIMBER) and all its dependencies. Specifically, the resulting dockerfile makes use of the official [ROOT Docker image](https://hub.docker.com/r/rootproject/root) and a [modified version](https://github.com/mroguljic/TIMBER/tree/Zbb_branch_py3) of TIMBER that has support for Python 3 installation. Many thanks to Amitav Mitra for maintaining TIMBER and providing examples.

## Table of Contents
- [Setup](#setup)
- [TLDR](#tldr)
- [Longer Instructions](#longer-instructions)
  * [Pulling image](#pulling-image)
  * [Building image](#building-image)
  * [Running the container](#running-the-container)
  * [Once inside the container](#once-inside-the-container)
  * [Mounting volumes](#mounting-volumes)
  * [Enabling X11 forwarding](#enabling-x11-forwarding)
- [Some Exercises](#running-exercises)
  * [ROOT Exercise](#root-exercise)
  * [TIMBER Exercise](#timber-exercise)

## Setup
First, install [Docker](https://www.docker.com/) for your operating system. There are many tutorials online for this. 

After installing Docker and testing that it works (`docker run hello-world`), you are ready to either pull the `timber-docker` image from the [Docker Hub](https://hub.docker.com/) (recommended) or build it yourself. **NOTE:** The base ROOT image that this container is built on is 1.5GB and the final `timber-docker` image is ~2GB. Once you've pulled/built the container, you won't have to do it again.  

## TLDR
Here are the abridged instructions for getting started:
```
git clone https://github.com/tvami/timber-docker.git
docker run --network=host -it tvami/timber-docker:latest
source setup.sh
```
At this point, you'll be inside the container and ready to use TIMBER!

If you want to get setup for use with the tutorials included in this repository, then simply run:
```
source exercises.sh
```

**NOTE:** If you are running the container on an ARM-based processor (e.g. Macbook M1), you'll also need to specify `--platform linux/amd64` to avoid emulation issues.

## Longer Instructions
<details>
<summary>Longer setup instructions and info about Docker</summary>

### Pulling image
To pull the ready-made image, run `docker pull ammitra/tvami-docker:latest`

### Building image
To build the image, run `docker build --network=host -t timber-docker`. You can name the image whatever you'd like after the `-t` (tag) flag. 

### Running the container
After having built or pulled the image, you are ready to run it. First, run `docker images` to list the availabe images you have:
```
docker images
REPOSITORY              TAG                   IMAGE ID       CREATED          SIZE
tvami/timber-docker   latest                9b33f3426e07   8 minutes ago    2.29GB
```
Run the desired image via `docker run --network=host -it <IMAGE ID>`. So, in the example above I'd run `docker run --network=host --entrypoint /bin/bash -it 9b33f3426e07`. The `--network=host` option isn't strictly necessary, but helps avoid possible annoying internet connection issues. The `-it` flag means that we want to run this container interactively. 

You can also skip pulling/running the container image, and just directly run `docker run --network=host -it ammitra/timber-docker:latest`.

**NOTE:** Once you've entered the container interactively, if you exit from that container (i.e. via `Ctrl+d`), anything in the container will be lost. This is by design (most containers are not run interactively, and instead perform a single executable or service). To get around this, it's often useful to start the container in the background (detached) via the `-d` flag. Then, you can enter the container again via `docker exec -t <CONTAINER ID> bash`, do your work, then exit the container at any point and be able to return to your work. An example is shown below:
```
docker run --network=host -it -d ammitra/timber-docker:latest
d6a61e2b22c297bc771f1ab1a4a0ae84aecb9f48b70c9e8ad3bab8fd7bd5f7ff
docker container ls 
CONTAINER ID   IMAGE                          COMMAND       CREATED          STATUS          PORTS     NAMES
d6a61e2b22c2   ammitra/timber-docker:latest   "/bin/bash"   15 seconds ago   Up 14 seconds             brave_shaw
docker exec -it d6a61e2b22c2 bash
physicist@thinkpad:~$ touch test
physicist@thinkpad:~$ ls
setup.sh  test
physicist@thinkpad:~$ exit
docker exec -it d6a61e2b22c2 bash
physicist@thinkpad:~$ ls
setup.sh  test
```

### Once inside the container
Now that you've got the container up and running, you should see a fresh bash terminal. The first step is to `source` the setup script, which activates the TIMBER virtual environment containing all the necessary python packages. To do so, just run `source setup.sh`. You should see a message pop up, and the command prompt should change to indicate that you're in the python virtual environment: 
```
physicist@hostname:~$ source setup.sh
TIMBER added to PATH
(timber-env) physicist@hostname:~$
```
Now you're ready to use TIMBER in the container!

### Mounting volumes
For our purposes, mounting volumes will be very useful. By passing the `-v` flag to a container when running it, you can mount a local directory to the container, giving the container access to all the files within that directory. The syntax for mounting is as follows:
```
docker run -v /path/to/local_dir:/path/in/container
```

**NOTE:** It seems that most OSes will only mount volumes located in the User's directory (i.e. `~` on Mac, Linux). So, be sure to clone this repository to somewhere within your user home directory so that the `timber-docker/rootfiles` directory can be mounted within the container properly.

The `path/to/local_dir` is the explicit path to the directory you want to mount, and `/path/in/container` is the full path to where you'd like to have it mounted in the container. As an example, if I wanted to mount the `rootfiles` directory in this repository to the container, to have access to the files there once inside the container, I would do:
```
pwd
/home/amitav/JHU/TIMBER_Docker
docker run -it -v ~/JHU/timber-docker/rootfiles:/home/physicist/rootfiles ammitra/timber-docker:latest
physicist@1fd467d1e9b2:~$ ls
rootfiles  setup.sh
physicist@1fd467d1e9b2:~$ ls -alh rootfiles
total 26M
drwxr-xr-x 2 physicist physicist 4.0K Sep 18 22:01 .
drwxr-xr-x 1 physicist physicist 4.0K Sep 18 22:49 ..
-rw-r--r-- 1 physicist physicist  26M Sep 18 22:19 TprimeB-1800-125.root
physicist@1fd467d1e9b2:~$ pwd
/home/physicist
```
And now I can access the files in that mounted directory!

### Enabling X11 forwarding
If you want to use GUI applications (including the ROOT [TBrowser](https://root.cern.ch/doc/master/classTBrowser.html)), then you will need to enable X11 forwarding through the container. If you are unfamiliar with X11 forwarding, there are explanations and tutorials online (e.g. [here](https://www.businessnewsdaily.com/11035-how-to-use-x11-forwarding.html)). After having set up an Xserver, you can pass `--env="DISPLAY"` to the container to enable the forwarding and allow you to see the GUI output through the container. 

</details>

## Running Exercises
Included in the repository are a set of exercise to help you learn both ROOT's C++ interface and TIMBER's python interface. For reference:
* [Get started with ROOT](https://root.cern/get_started/)
* [ROOT's python interface](https://root.cern/manual/python/)
* [TIMBER docs](https://lucascorcodilos.com/TIMBER/)

### ROOT exercise

<details>
<summary>This exercise will introduce you to the ROOT universe. Though painful sometimes, it's a very impressive piece of software and it's important to be familiar with the C++ backend before using TIMBER or any other Python wrapper over it.</summary>
<br>
 
First, run the container and mount the `rootfiles` directory as a volume in the container with the `-v` flag.
```
docker run --network=host -it -v /path/to/timber-docker/rootfiles:/home/physicist/rootfiles ammitra/timber-docker:latest
```

Once inside the container, the ROOT software is already enabled by default so we can immediately start using it. Run
```
root -l rootfiles/TprimeB-1800-125.root
```

There may be some warnings about missing dictionaries, but just ignore those. You'll see something that looks like:
```
physicist@1fd467d1e9b2:~$ root -l rootfiles/TprimeB-1800-125.root
root [0]
Attaching file rootfiles/TprimeB-1800-125.root as _file0...
(TFile *) 0x55a2be2dac10
root [1]
```

You are now in the ROOT terminal, and your command prompt has been replaced with `root [x]`, where `x` denotes the number of commands you've performed.

Let's look inside the file we've opened:
```
root [1] .ls
TFile**         rootfiles/TprimeB-1800-125.root
 TFile*         rootfiles/TprimeB-1800-125.root
  KEY: TObjString       tag;1   Collectable string class
  KEY: TTree    Events;1        Events
  KEY: TTree    LuminosityBlocks;1      LuminosityBlocks
  KEY: TTree    Runs;1  Runs
  KEY: TTree    MetaData;1      Job metadata
  KEY: TTree    ParameterSets;1 Parameter sets
```

We see that the file (called a [TFile](https://root.cern.ch/doc/master/classTFile.html)) contains keys called [TTrees](https://root.cern.ch/doc/master/classTTree.html). These trees store physics variables, histograms, formulas, and other useful objects. These trees are also converted to [RDataFrames](https://root.cern/doc/master/classROOT_1_1RDataFrame.html) by the TIMBER Analyzer module. To check out what's in the tree, we can use `TTree::Print()`. Note that, the trees displayed by `.ls()` are all pointers, so we have to use the C++ dereference operator (`->`) on them to access their member functions (such as `Print()`):

Run `Events->Print()` in the ROOT terminal:

```
root [1] Events->Print()
******************************************************************************
*Tree    :Events    : Events                                                 *
*Entries :     8000 : Total =        92051425 bytes  File  Size =   24135006 *
*        :          : Tree compression factor =   3.79                       *
******************************************************************************
...
*............................................................................*
*Br  143 :FatJet_eta : Float_t eta                                           *
*Entries :     8000 : Total  Size=     105830 bytes  File Size  =      50976 *
*Baskets :        4 : Basket Size=      59904 bytes  Compression=   2.06     *
*............................................................................*
*Br  144 :FatJet_mass : Float_t mass                                         *
*Entries :     8000 : Total  Size=     105838 bytes  File Size  =      38992 *
*Baskets :        4 : Basket Size=      59904 bytes  Compression=   2.70     *
*............................................................................*
*Br  145 :FatJet_msoftdrop : Float_t Corrected soft drop mass with PUPPI     *
*Entries :     8000 : Total  Size=     105904 bytes  File Size  =      40132 *
*Baskets :        4 : Basket Size=      59904 bytes  Compression=   2.62     *
*............................................................................*
*Br  149 :FatJet_particleNetMD_Xbb :                                         *
*         | Float_t Mass-decorrelated ParticleNet tagger raw X->bb score. For X->bb vs QCD tagging, use Xbb/(Xbb+QCD)*
*Entries :     8000 : Total  Size=     106022 bytes  File Size  =      40780 *
*Baskets :        4 : Basket Size=      59904 bytes  Compression=   2.58     *
*............................................................................*
```

Right away, we can see that the tree contains 8,000 entries (events), each with a corresponding [TBranch](https://root.cern/doc/master/classTBranch.html) containing some physics information for each event. For instance, the branch `FatJet_msoftdrop` contains the [softdrop mass](https://arxiv.org/abs/1402.2657) of each of the jets in each event, and so on for all the other branches. Try running `Print()` on one of the TTrees in the file and see what other branches exist. 

We can then use `TTree::Scan()` to check out one of the branches individually. To do so, just pass the branch name to the `Scan()` function:
```
root [4] Events->Scan("FatJet_msoftdrop")
***********************************
*    Row   * Instance * FatJet_ms *
***********************************
*        0 *        0 *   168.875 *    <- Event 0, jet 1
*        0 *        1 *   131.125 *    <- Event 0, jet 2
*        0 *        2 * 5.1953125 *    <- Event 0, jet 3
*        1 *        0 *   136.875 *
*        1 *        1 * 8.3515625 *
*        2 *        0 *   175.375 *
*        2 *        1 *   118.625 *
*        3 *        0 *  104.9375 *
*        3 *        1 *  120.4375 *
...
Type <CR> to continue or q to quit ==> q
***********************************
```
From this, we can deduce that Event 1 (row 1) had three fat jets, with masses 169, 131, and 5 GeV. TTree tools like `Print()` and `Scan()` are useful when you want to find variables of interest in your datasets (which can then be used in TIMBER!)

**NOTE:** You can also use ROOT's [TBrowser](https://root.cern.ch/doc/master/classTBrowser.html) to open a GUI application to view all the trees and branches in your file. This is nice because it offers a user-friendly graphical representation of the structure and contents of your data files. To open from the ROOT prompt, just run 
```
root [0] TBrowser b
```
to open up the GUI window. From here, you can view your file interactively via a GUI. If you are running ROOT in the container, you'll need to have passed the `--env="DISPLAY"` flag when first running the container in order to access your display. 

Now that we have a variable of interest, what can we do with it? Normally, we might be interested in seeing a distribution of that variable for our dataset. So, let's make use of the [`TTree::Draw()`](https://root.cern.ch/doc/master/classTTree.html#a73450649dc6e54b5b94516c468523e45) function to produce a histogram of the softdrop masses of all jets in the dataset:
```
root [5] Events->Draw("FatJet_msoftdrop")
Info in <TCanvas::MakeDefCanvas>:  created default TCanvas with name c1
```
Normally, you'd see the histogram of masses pop up in a little GUI. However, dealing with X11 forwarding is difficult in containers and I haven't implemented that here. For more info, read [here](https://opendata-forum.cern.ch/t/x11-forwarding-with-docker/31). 

Finally, let's run a ROOT C++ macro which will actually give us the histogram we want. It is already written and located under `rootfiles/macro.C`, so you can study it and see what exactly it does. Close the ROOT shell, then run 
```
physicist@1fd467d1e9b2:~$ root rootfiles/macro.C
```
You'll see an output of:
```
root [0]
Processing rootfiles/macro.C...
Info in <TCanvas::Print>: pdf file /home/physicist/rootfiles/macro_output.pdf has been created
root [1]
```
If you look in the `rootfiles/` directory on your local machine, you'll see the output file. Take a look - this is the softdrop mass of all the jets in our sample! The sample in question is Monte Carlo simulation of a Beyond Standard Model process - a hypothetical heavy vector-like partner to the top quark, $T^{\prime}$ whose decay has been set in the generator to a top quark and a new scalar $\phi$. So, the jets in this sample are all from the decay of a top quark and the decay of the scalar. In this sample, the $m_{T^{\prime}}=1.8$ TeV and the $m_\phi=125$ GeV (the Higgs boson mass). The top quark has a mass of 173 GeV/c^2 - does the resulting plot make sense??

If the macro seemed complicated, that's understandable. There are several Python wrappers for ROOT, the most common being [pyROOT](https://root.cern/manual/python/), which comes bundled in our container. To try it out, simply run 
```
python rootfiles/macro.py
```
If you take a look at the code you'll see the parallels, but it's noticeably easier in Python since you don't have to worry about pointers or memory management (at least for this simple example). 

There is of course much more to learn about ROOT, but hopefully this gives you an idea of the power of ROOT as well as some insights into the tools you can make use of when writing analyses in TIMBER.
</details>

### TIMBER exercise

<details>
<summary>This exercise will introduce you to TIMBER, first interactively via the command line and then using a Python script.</summary>
<br>

The main goal of this exercise is to introduce you to some of the functionality of TIMBER. Most, if not all, of the time you use TIMBER it will be inside of a Python script which you then execute. However, for the sake of illustration we will run this exercise on the command line in a python shell. This way you can see the results of every step as it happens. The full exercise is also contained in the script `rootfiles/timber.py`, which you should run after the exercise to see an implementation of TIMBER in a script. The file also has a lot of comments which hopefully make things clear. 

For this exercise, it'll be useful to open the container in one window and this repository in another, so that you can look at the outputs locally once they've been processed. Begin by running:

```
docker run -it -v /path/to/timber-docker/rootfiles:/home/physicist/rootfiles ammitra/timber-docker:latest
source setup.sh
```

By `source`ing the setup file, we've activated the python virtual environment containing TIMBER and we are ready to call any of the TIMBER functions within a python shell or via a script. You'll see import errors if you forget to do this step. 
 
Open a python shell by invoking `python` on the command line, then run 
```
from TIMBER.Analyzer import analyzer
from TIMBER.Tools.Common import *
```
This will import the main TIMBER class, `analyzer`, as well as some other useful tools built-in to TIMBER. 
 
We can instantiate an analyzer object by passing it either a ROOT file or a `.txt` list of ROOT files. Upon instantiation, the analyzer will create an RDataFrame out of the file(s). For this example, we will just pass the analyzer the ROOT file containing Monte Carlo simulation of an 1800 GeV $T^{\prime}$, a hypothetical heavy partner to the top quark, which in this sample decays to a top quark and a new scalar $\phi$ of mass 125 GeV. 
```
ana = analyzer('/home/physicist/rootfiles/TprimeB-1800-125.root')
```

Our goal will now be to use TIMBER to define the events containing jets corresponding to a top quark and a $\phi$ (which will be most of them in this case), then use the invariant mass of those jets to reconstruct the $T^{\prime}$ resonance. 

Let's start by making some kinematic cuts targeting our signal topology. We expect the resonance to decay to two particles, so we will be looking for two jets roughly back-to-back. The $T^{\prime}$ itself is heavy, so the top and $\phi$ will be significantly Lorentz boosted which will cause their respective decay products ($t\to bW(qq)$ and $\phi\to b\bar{b}$) to be reconstructed as large-radius (AK8) jets. Here are some basic kinematic cuts:

```
ana.Cut('nJets', 'nFatJet > 2')
ana.Cut('pT_cut', 'FatJet_pt[0] > 400 && FatJet_pt[1] > 400')
ana.Cut('eta_cut', 'abs(FatJet_eta[0]) < 2.4 && abs(FatJet_eta[1]) < 2.4')
ana.Cut('msd_cut', 'FatJet_msoftdrop[0] > 50 && FatJet_msoftdrop[1] > 50') 
```

The `Cut()` function takes in the name of the cut for internal tracking and a string which evaluates to C++ actions on the DataFrame. The action must always only reference columns (variables) that exist in the DataFrame, C++ functions defined in the ROOT and TIMBER libraries (`abs()`, `min()`, etc.), or C++ functions that you define yourself and call via TIMBER. 
 
We will now show an example of calling a user-defined C++ function. First, you would write an implementation of the function in a `.cc` or `.cpp` file, then you would compile it via TIMBER. When we ran `from TIMBER.Tools.Common import *` earlier, we imported the `CompileCpp()` function, which takes in a string containing the path to the file containing the function you'd like to compile. There is already one written for this exercise, so compile via 
```
CompileCpp('/home/physicist/rootfiles/Modules.cc')
```

Now, let's invoke one of the custom functions on our DataFrame via TIMBER:
```
ana.Define('DijetIdxs', 'PickDijets(FatJet_pt, FatJet_eta, FatJet_phi, FatJet_msoftdrop)')
```
 
Here, we define a new column (variable) named `DijetIdxs`, which will represent the indices of any two jets in the event which meet the criteria that they are separated by at least 90 degrees. When we invoke `Define()`, whatever our action defined in the input string is will be applied *to each row in the DataFrame.* That means that our `PickDijets()` function will be applied to each event. You can look at the `rootfiles/Modules.cc` file for more details on the implementation, but essentially if we have an event that has, say, 4 jets and jets 0 and 2 are back-to-back, the `PickDijets()` function will return a vector of those indices: `{0, 2}` and assign it to that event. Specifically, the function will return a vector `{-1, -1}` if there are no jets in the event meeting our back-to-back criteria. 

We can now cut on this newly-defined variable:
```
ana.Cut('dijetsExist', 'DijetIdxs[0] > -1 && DijetIdxs[1] > -1')
```
 
For each event, the C++ logic evaluates to either `1`: this event has two jets meeting our criteria or `0`: this event does not have any jets meeting our criteria, which the RDataFrame then uses to filter eligible events. 
 
At this point, we've sufficiently "skimmed" our data and we can attempt to make some jet identification. We will start off with a naive method in which we assume that the 0th index in `DijetIdxs` represents the top and the 1st index the $\phi$ candidate. The vectors are ordered by pT, so this is not a terrible proxy for the top and $\phi$ identification in this case. 
 
We will make use of a special TIMBER function to create a new collection of columns (variables) based on an existing one. We will take the `FatJet_*` columns and recast them to be either `Top_*` or `Phi_*` columns based on the indices of each jet. To conceptualize this, let's draw a diagram. Currently, we have a DataFrame that looks like (values given are examples):
```
-----------------------------------------------------------------------------------------------------------------------
| Event # |          FatJet_pt             |          FatJet_phi          |          FatJet_eta        |   DijetIdxs  |
-----------------------------------------------------------------------------------------------------------------------
| Event 0 | {782.1, 600.1, 534.3, 456.7}   |  {-2.82, 0.44, -1.12, 1.14}  | {-0.03, 1.23, 0.08, -1.3}  |    {0, 2}    |
-----------------------------------------------------------------------------------------------------------------------
... and so on, for all events that have passed selection so far
```

We will now run the TIMBER commands
```
ana.ObjectFromCollection('Top','FatJet','DijetIdxs[0]')
ana.ObjectFromCollection('Phi','FatJet','DijetIdxs[1]')
```
 
Running this function will create a new group of variables containing all of the previously-named `FatJet_*` variables, but now containing just the single value based on the corresponding jet index. To help illustrate this, let's look back at the diagram we drew. The DataFrame with the new columns would look like:
```
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| Event # |          FatJet_pt            | Top_pt | Phi_pt |          FatJet_phi          | Top_phi | Phi_phi |         FatJet_eta          | Top_eta | Phi_eta |  DijetIdxs  |
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| Event 0 | {782.1, 600.1, 534.3, 456.7}  | 782.1  |  534.3 |  {-2.82, 0.44, -1.12, 1.14}  | -2.82   |  -1.12  |  {-0.03, 1.23, 0.08, -1.3}  |  -0.03  |   0.08  |   {0, 2}    |
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```

Now, we can create [TLorentz](https://github.com/lcorcodilos/TIMBER/blob/master/TIMBER/Framework/include/common.h#L119-L138) vectors from each newly-defined jet's pT, eta, phi, and softdrop mass:
```
ana.Define('Top_vect','hardware::TLvector(Top_pt, Top_eta, Top_phi, Top_msoftdrop)')
ana.Define('Phi_vect','hardware::TLvector(Phi_pt, Phi_eta, Phi_phi, Phi_msoftdrop)')
```

Then, we use these TLvectors to reconstruct the invariant mass of the resonance:
```
ana.Define('mtphi','hardware::InvariantMass({Top_vect, Phi_vect})')
```

Let's now plot the phi mass vs the resonance mass and see what it looks like:
```
c = ROOT.TCanvas('c')
c.cd()
c.Print("/home/physicist/rootfiles/output_timber.pdf[")
c.Clear()
h1 = ana.DataFrame.Histo2D(('h1','#phi mass vs resonance mass - naive method;m_{#phi} [GeV];m_{res} [GeV]',40,60,260,22,800,3000),'Phi_msoftdrop','mtphi')
h1.Draw("COLZ")
c.Print('/home/physicist/rootfiles/output_timber.pdf')
c.Clear()
h1.Draw("LEGO2")
c.Print('/home/physicist/rootfiles/output_timber.pdf')
c.Clear()
c.Print('/home/physicist/rootfiles/output_timber.pdf]')
```

When we define the 2D histogram `h1` on the 5th line, we are actually using RDataFrame directly through pyROOT via the TIMBER analyzer. This is one of the great features of TIMBER - the analyzer stores the RDataFrame internally, so we can actually use any RDataFrame method which has a pyROOT equivalent. In this case, we can call the [`RDataFrame.Histo2D()`](https://root.cern/doc/master/classROOT_1_1RDF_1_1RInterface.html#a0a29727f2ceca107e39cbff8b7cb3a1a) method, which takes in (in pyROOT at least) a tuple containing the histo name, title, axis labels (semicolon-delimited), and binning schema; followed by the column (variable) names you want to plot on the x- and y-axes. We then draw the histogram in two different ways and save them to a pdf file under `rootfiles/` so that it's accessible from outside the container as well. 
 
At the end, you should get two plots that look like this:
![image](https://user-images.githubusercontent.com/64038220/191665590-22687beb-9f49-45ee-8425-23558363ca72.png)
![image](https://user-images.githubusercontent.com/64038220/191665630-d03592d1-ba29-49ac-8ee7-e2fbe65679a0.png)

Does this plot of $\phi$ mass versus $T^{\prime}$ mass make sense? Recall that, for this signal sample, the mass of the $\phi$ is 125 GeV. What is causing that second bump appearing around 170 GeV? Why does that bump appear, even though we're plotting the $\phi$ mass? These are some things to think about, and you should also think of (and implement) ways of making the identification more robust.
 
This concludes the first TIMBER exercise. Since we're only running TIMBER on a small signal sample in this exercise, we're limited in what interesting physics we can do. But this should serve as an introduction to the TIMBER framework and provide a conceptual overview for how to use TIMBER.
 
</details>


