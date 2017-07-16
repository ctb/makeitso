# makeitso

![Make it so!](https://media.giphy.com/media/bKnEnd65zqxfq/giphy.gif)

makeitso is a simple [task pool/tuple space](http://wiki.c2.com/?TupleSpace) implementation for running CWL workflows. It's a demo/hack, not a robust implementation :).

See https://github.com/ctb/makeitso for version.

## Currently implemented functionality

### Run CWL workflow on current computer

run from github.com/ctb/salmon, branch master
```
makeitso run ctb/salmon[:master] params.json
```
-- this will automatically assume github etc.

* how does it know what CWL file to look at? defaults + allow override.


### Set up task pool server

to collect and distribute tasks to workers. also optionally will set up a web form at 127.0.0.1/ to accept tasks.

```
makeitso server
```

* what kind of authentication?

### Set up task pool runner

to run tasks

```
makeitso worker [ -S server_URL ]
```
in future take this from `MAKEITSO_SERVER`

### Send task to task pool server

```
maketiso sendtask [ -S server_URL] ctb/salmon[:master] params.json
```

## Demo on a Jetstream m1.medium

Starting from Ubuntu 16.04 on Jetstream.

### Install `cwltool`

Now, install the Common Workflow Language reference runner:
```

pip install 'setuptools>=28.8.0'
pip install cwlref-runner 'cwltool>=1.0.20170713144155'
```

### Add your user account to the docker group

```
sudo usermod -aG docker $USER
exec newgrp docker
```

The configuration/install stuff is now done and you're ready to run!

### Running a CWL workflow from dockstore

Let's run the [`dockstore-tool-bamstats`](https://dockstore.org/containers/registry.hub.docker.com/cancercollaboratory/dockstore-tool-bamstats) tool from the dockstore.org registry.

Download some input data:
```
curl -o /tmp/rna.SRR948778.bam -L https://github.com/CancerCollaboratory/dockstore-tool-bamstats/raw/develop/rna.SRR948778.bam
```

Construct a params file:

```
cat >params.yaml <<EOF
bam_input:
    class: File
    path: /tmp/rna.SRR948778.bam
mem_gb: 4
EOF
```

You can test-run run the tool like so --

```
cwl-runner https://github.com/CancerCollaboratory/dockstore-tool-bamstats/raw/develop/Dockstore.cwl \
    params.yaml
```

and that should succeed.

## Running it using `makeitso run`

First, install `makeitso`.

```
cd ~/
git clone https://github.com/ctb/makeitso

echo 'export PYTHONPATH=~/makeitso' >> ~/.bashrc
source ~/.bashrc
```

Now you can run workflows off of github using a bit of a shorthand, which is nice --

```
python -m makeitso run \
    CancerCollaboratory/dockstore-tool-bamstats:develop \
    params.yaml
```
-- but not the whole story.

## Run a task pool server

```
makeitso/server-makeitso  >& /tmp/out &
```

## Run a task pool worker

```
python -m makeitso worker --quit
```

(This will exit immediately if there are no tasks.)

## Send a task

```
python -m makeitso sendtask \
    CancerCollaboratory/dockstore-tool-bamstats:develop \
    params.yaml
```
and run task processor again:

```
python -m makeitso --quit
```

You can send tasks from anywhere and run workers anywhere.

## Unexplored issues

Other than basic robustness and stability and testing,

* what is the right way to bring in input files?
* what's the right cleanup? we need to clean up docker images as well.
* what are good recipes for killing AWS/GCP/etc. machines and what is the right way to integrate them into something like makeitso.
* the biggest issue is what to do with the output files.
    * punt to a local file server (running proximally) - security etc becomes an issue
    * shove into an S3 bucket or other programmatic storage
    * ???
    * implement dat => home location, but then you deal with egress.
    * you should also update the task pool with "done" and location of output
* Question from RTS: how do you avoid re-running multiple identical tasks (one answer - calculate hashes of inputs and workers)

## Notes

https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

https://stackoverflow.com/questions/17301938/making-a-request-to-a-restful-api-using-python

https://zerotier.com/

https://software-carpentry.org/blog/2011/03/tuple-spaces-or-good-ideas-dont-always-win.html