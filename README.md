# DataScienceBox

[![travis-ci](https://travis-ci.org/danielfrg/datasciencebox.svg)](https://travis-ci.org/danielfrg/datasciencebox)

Command line utility to create instances in the cloud ready for data science.
Includes conda package management plus some Big Data frameworks (spark).

## Installation

`pip install datasciencebox`

## Usage

The basic usage is very similar to `vagrant`, `fabric` or `docker` in which you create a
`Vagrantfile`, `fabfile` or `Dockerfile` respectively and execute the command line
in the directory that contains that file.

In this case you create a `dsbfile` and use the `dsb` (or `datasciencebox`) command.

This makes it possible to version control everything, from box settings to custom salt states.

A `dsbfile` is a python file and looks like this:

```python
# AWS
ID = 'daniel'

# AWS
CLOUD = 'aws'
NUMBER_NODES = 2
AWS_KEY = ''
AWS_SECRET = ''
AWS_KEYNAME = ''
AWS_REGION = 'us-east-1'
AWS_IMAGE = 'ami-d05e75b8'
AWS_SIZE = 'm3.large'
AWS_SECURITY_GROUPS = ['default']
AWS_ROOT_SIZE = 100
AWS_ROOT_TYPE = 'gp2'

USERNAME = 'ubuntu'
KEYPAIR = '~/.ssh/mykey.pem'

# GCP
CLOUD = 'gcp'
NUMBER_NODES = 2
GCP_EMAIL = ''
GCP_KEY_FILE = '~/.ssh/mykey.json'
GCP_PUBLIC_KEY = '~/.ssh/id_rsa.pub'
GCP_PROJECT = ''
GCP_DATACENTER = 'us-central1-f'
GCP_SIZE = 'n1-standard-1'
GCP_IMAGE = 'ubuntu-1404'
GCP_NETWORK = 'allopen'
GCP_ROOT_SIZE = 100
GCP_ROOT_TYPE = 'pd-ssd'

USERNAME = ''
KEYPAIR = '~/.ssh/id_rsa'

# BARE
CLOUD = 'bare'
NODES = ['0.0.0.0', '0.0.0.0']

USERNAME = 'ubuntu'
KEYPAIR = '~/.ssh/id_rsa'
```

**Supported OS**: At this moment only Ubuntu 14.04 is supported.

**Credentials**: You don't want credentials to be uploaded to the version control (trust me).
But since the `dsbfile` is a python file you can always do something like this
to read from environment variables for example:

```python
import os

AWS_KEY = os.environ['AWS_KEY']
AWS_SECRET = os.environ['AWS_SECRET']
```

**Note**: No security groups or keypairs are created for you its up to you to create
those in AWS or similar.

## Creating the instances

Once the `dsbfile` is created you can create the instance(s) running `dsb up`.

This will create the instance(s) in the cloud provider and create a `.dsb` directory
in the same location as the `dsbfile`.

The `.dsb` directoy can be ignored for basic usage. It contains metadata about the instances
but it can also be used to control the settings of the cluster (pillars) and even upload custom salt states. This also allows to version control all the deployment of a cluster.

For a `bare` cluster this command will just create the required metadata.

### Initial setup

Everything in the DSB is based on [Salt](https://github.com/saltstack/salt) and there are two ways of bootstraping stuff into the nodes: salt master or salt ssh.

The recommended (and default) way is using salt via ZMQ which requires the salt master
and minion to be installed in the nodes. This is done by default with `dsb up` but
can be omitted with the `--no-salt` flag in case you want to just use salt-ssh
or just create the cloud instances.

If you want to use salt ssh only you need to add the `--ssh` flag to all the commands.
Note that this works well for some commands like `dsb cmd ...`, ` dsb install conda ...`
but might not works as expected for the distributed frameworks like zookeeper and mesos.

## General management

### Remote commands

```bash
$ dsb cmd <CMD>
$ # Example
$ dsb cmd 'date'
$ dsb cmd 'date' --ssh
```

### Install OS packages

```bash
$ dsb install pkg <PKG_NAME>
$ # Example
$ dsb install pkg build-essential
$ dsb install pkg build-essential --ssh
```

### General salt module

Note that the commands above (and basically all of them) is just an alias for a general salt command.

```bash
$ dsb salt '*' network.ipaddrs
$ # Example
$ dsb salt '*' network.ipaddrs
$ dsb salt '*' network.ipaddrs --ssh
```

## Conda management

First, you need to install miniconda in all the nodes:

```bash
$ dsb install miniconda
$ dsb install miniconda --shh
```

**Note**: This will install anaconda under: `/home/{{ USERNAME }}/anaconda`

Then you can install conda packages:

```bash
$ dsb install conda <PKG_NAME>
$ # Example
$ dsb install conda numpy
$ dsb install conda numpy --ssh
```

### Jupyter Notebook

```bash
$ dsb install notebook
$ dsb open notebook
```

## Cloudera

Install Cloudera Manager

```bash
$ dsb install cloudera-manager
$ dsb open cloudera-manager
```

Once on the Cloudera Manager UI just follow the instructions.

- In the "Specify hosts for your CDH cluster installation" section
just click on the "Currently Managed Hosts" tab and all the Nodes
in the cluster should be there already, select all of them and click "Continue"
- Select the frameworks that you want: Impala, Spark, etc.
- On the "Database Setup" section click "Test connection" and then "Continue"

Look at the example on for how to use Spark on YARN.

### HDFS

`deprecated`: Use Cloudera Manager

```bash
$ dsb install hdfs
$ dsb open hdfs
```

### Impala

`deprecated`: Use Cloudera Manager

Using Postgres as Hive Metastore. Impala shell is available in all the compute nodes (no head).

```bash
$ dsb install impala
```

## Mesos

```bash
$ dsb install mesos
$ dsb open mesos
```

### Spark

Spark using Mesos as scheduler

```bash
$ dsb install spark
```

To use Spark the easiest way is it to install the Jupyter notebook and use use spark there,
note that if you already installed the notebook you have to run `dsb install notebook`
again to include the spark env variables, see examples.

### Marathon

Marathon can be used to deploy any application or docker container in Mesos.

```bash
$ dsb install marathon
$ dsb open marathon
```
