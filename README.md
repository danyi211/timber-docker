# TIMBER in a container
This repository contains the Dockerfile used to create a container running TIMBER and all its dependencies.

## Setup
First, install [Docker](https://www.docker.com/) for your operating system. There are many tutorials online for this. 

After installing Docker and testing that it works (`docker run hello-world`), you are ready to either pull the `timber-docker` image from the [Docker Hub](https://hub.docker.com/) (recommended) or build it yourself. **NOTE:** The base ROOT image that this container is built on is 1.5GB and the final `timber-docker` image is ~2GB. Once you've pulled/built the container, you won't have to do it again.  

### Pulling image (recommended)
To pull the ready-made image, run `docker pull ammitra/timber-docker:latest`

### Building image
To build the image, run `docker build --network=host -t timber-docker`. You can name the image whatever you'd like after the `-t` (tag) flag. 

## Running the container
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

## Once inside the container
Now that you've got the container up and running, you should see a fresh bash terminal. The first step is to `source` the setup script, which activates the TIMBER virtual environment containing all the necessary python packages. To do so, just run `source setup.sh`. You should see a message pop up, and the command prompt should change to indicate that you're in the python virtual environment: 
```
physicist@hostname:~$ source setup.sh
TIMBER added to PATH
(timber-env) physicist@hostname:~$
```
Now you're ready to use TIMBER in the container!

