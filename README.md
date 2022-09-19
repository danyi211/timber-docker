# TIMBER in a container
This repository contains the Dockerfile used to create a container running [TIMBER](https://github.com/lcorcodilos/TIMBER) and all its dependencies. Specifically, the resulting dockerfile makes use of the official [ROOT Docker image](https://hub.docker.com/r/rootproject/root) and a [modified version](https://github.com/mroguljic/TIMBER/tree/Zbb_branch_py3) of TIMBER that has support for Python 3 installation.

## Table of Contents
- [Setup](#setup)
- [TLDR](#tldr)
- [Longer Instructions](#longer-instructions)
  * [Pulling image](#pulling-image)
  * [Building image](#building-image)
  * [Running the container](#running-the-container)
  * [Once inside the container](#once-inside-the-container)
  * [Mounting volumes](#mounting-volumes)
- [Some Exercises](#running-exercises)
  * [ROOT Exercise](#root-exercise)
  * [TIMBER Exercise](#timber-exercise)

## Setup
First, install [Docker](https://www.docker.com/) for your operating system. There are many tutorials online for this. 

After installing Docker and testing that it works (`docker run hello-world`), you are ready to either pull the `timber-docker` image from the [Docker Hub](https://hub.docker.com/) (recommended) or build it yourself. **NOTE:** The base ROOT image that this container is built on is 1.5GB and the final `timber-docker` image is ~2GB. Once you've pulled/built the container, you won't have to do it again.  

## TLDR
Here are the abridged instructions for getting started:
```
git clone https://github.com/ammitra/timber-docker.git
docker run --network=host -it ammitra/timber-docker:latest
source setup.sh
```
At this point, you'll be inside the container and ready to use TIMBER!

## Longer Instructions
<details>
<summary>Longer setup instructions and info about Docker</summary>

### Pulling image
To pull the ready-made image, run `docker pull ammitra/timber-docker:latest`

### Building image
To build the image, run `docker build --network=host -t timber-docker`. You can name the image whatever you'd like after the `-t` (tag) flag. 

### Running the container
After having built or pulled the image, you are ready to run it. First, run `docker images` to list the availabe images you have:
```
[amitav@thinkpad ~]: docker images
REPOSITORY              TAG                   IMAGE ID       CREATED          SIZE
ammitra/timber-docker   latest                9b33f3426e07   8 minutes ago    2.29GB
```
Run the desired image via `docker run --network=host -it <IMAGE ID>`. So, in the example above I'd run `docker run --network=host --entrypoint /bin/bash -it 9b33f3426e07`. The `--network=host` option isn't strictly necessary, but helps avoid possible annoying internet connection issues. The `-it` flag means that we want to run this container interactively. 

You can also skip pulling/running the container image, and just directly run `docker run --network=host -it ammitra/timber-docker:latest`.

**NOTE:** Once you've entered the container interactively, if you exit from that container (i.e. via `Ctrl+d`), anything in the container will be lost. This is by design (most containers are not run interactively, and instead perform a single executable or service). To get around this, it's often useful to start the container in the background (detached) via the `-d` flag. Then, you can enter the container again via `docker exec -t <CONTAINER ID> bash`, do your work, then exit the container at any point and be able to return to your work. An example is shown below:
```
[amitav@thinkpad ~]: docker run --network=host -it -d ammitra/timber-docker:latest
d6a61e2b22c297bc771f1ab1a4a0ae84aecb9f48b70c9e8ad3bab8fd7bd5f7ff
[amitav@thinkpad ~]: docker container ls 
CONTAINER ID   IMAGE                          COMMAND       CREATED          STATUS          PORTS     NAMES
d6a61e2b22c2   ammitra/timber-docker:latest   "/bin/bash"   15 seconds ago   Up 14 seconds             brave_shaw
[amitav@thinkpad ~]: docker exec -it d6a61e2b22c2 bash
physicist@thinkpad:~$ touch test
physicist@thinkpad:~$ ls
setup.sh  test
physicist@thinkpad:~$ exit
[amitav@thinkpad ~]: docker exec -it d6a61e2b22c2 bash
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
The `path/to/local_dir` is the explicit path to the directory you want to mount, and `/path/in/container` is the full path to where you'd like to have it mounted in the container. As an example, if I wanted to mount the `rootfiles` directory in this repository to the container, to have access to the files there once inside the container, I would do:
```
[amitav@thinkpad ~]: pwd
/home/amitav/JHU/TIMBER_Docker
[amitav@thinkpad ~]: docker run -it -v ~/JHU/TIMBER_Docker/rootfiles:/home/physicist/rootfiles ammitra/timber-docker:latest
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
docker run --network=host -it -v /path/to/TIMBER_Docker/rootfiles:/home/physicist/rootfiles
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

We see that the file (called a [TFile](https://root.cern.ch/doc/master/classTFile.html)) contains keys called [TTrees](https://root.cern.ch/doc/master/classTTree.html). These trees store physics variables, histograms, formulas, and other useful objects. These trees are also converted to [RDataFrames](https://root.cern/doc/master/classROOT_1_1RDataFrame.html) by the TIMBER Analyzer module. To check out what's in the tree, we can use `TTree::Print()`:
```
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
*        0 *        0 *   168.875 *
*        0 *        1 *   131.125 *
*        0 *        2 * 5.1953125 *
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

Now that we have a variable of interest, what can we do with it? Normally, we might be interested in seeing a distribution of that variable for our dataset. So, let's make use of the [`TTree::Draw()`](https://root.cern.ch/doc/master/classTTree.html#a73450649dc6e54b5b94516c468523e45) function to produce a histogram of the softdrop masses of all jets in the dataset:
```
root [5] Events->Draw("FatJet_msoftdrop")
Info in <TCanvas::MakeDefCanvas>:  created default TCanvas with name c1
```
Normally, you'd see the histogram of masses pop up in a little GUI. However, dealing with X11 forwarding is difficult in containers and I haven't implemented that here. For more info, read [here](https://opendata-forum.cern.ch/t/x11-forwarding-with-docker/31). 

Finally, let's run a ROOT C++ macro which will actually give us the histogram we want. It is already written and located under `rootfiles/macro.C`, so you can study it and see what exactly it does.
```
root [0]
Processing rootfiles/macro.C...
Info in <TCanvas::Print>: pdf file /home/physicist/rootfiles/output.pdf has been created
root [1]
```
If you look in the `rootfiles/` directory on your local machine, you'll see the output file. Take a look - this is the softdrop mass of all the jets in our sample! The sample in question is Monte Carlo simulation of a Beyond Standard Model process - a hypothetical heavy vector-like partner to the top quark, $T^{\prime}$ whose decay has been set in the generator to a top quark and a new scalar $\phi$. So, the jets in this sample are all from the decay of a top quark and the decay of the scalar. In this sample, the $m_{T^{\prime}}=1.8$ TeV and the $m_\phi=125$ GeV (the Higgs boson mass). The top quark has a mass of 173 GeV/c^2 - does the resulting plot make sense??

There is of course much more to learn about ROOT, but hopefully this gives you an idea of the power of ROOT as well as some insights into the tools you can make use of when writing analyses in TIMBER. The next section will cover an example of how to use TIMBER to do the same thing as we just did here, but in a *much* more readable and painless manner!
</details>

### TIMBER exercise
This exercise will introduce you to pyROOT and TIMBER, which are a bit easier to work with than the C++ interface. To begin, simply run 
```
docker run -it -v ~/path/to/TIMBER_Docker/rootfiles:/home/physicist/rootfiles ammitra/timber-docker:latest
source setup.sh
python rootfiles/timber.py
```
That's all - the `timber.py` script contains everything you need to replicate what we just did previously. **MORE CONTENT TO COME**



