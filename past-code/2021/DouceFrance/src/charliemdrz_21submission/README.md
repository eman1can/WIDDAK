# Welcome to our repo for the 2021 [GDMC competition](https://gendesignmc.engineering.nyu.edu/)

Our submission works on the GDMC HTTP interface by [nilsgawlik](https://github.com/nilsgawlik/gdmc_http_interface) and is based on the [Python client](https://github.com/nilsgawlik/gdmc_http_client_python) associated with it.

To get our submission working, make sure to install all the Python dependencies linked in the requirements.txt via
```
$ pip install -r requirements.txt
```

When the build area has been set, just run the `main.py` script.

## TODO: rewrite this readme -> deprecated version dating back to our 2020 submission

This repo is duplicated from [this repo](http://github.com/mcgreentn/MCAI) to make it ours and private

First things first: here is the initial wiki of the duplicated repo [VISIT THE WIKI PAGE](http://github.com/mcgreentn/MCAI/wiki)

Next is 'how to set up a common dev environment'.

## Info on the repo

There are examples of filters in the stock_filters folder, but all are disabled to simplify testing (only one filter : ours) (`perform()`=>`performed()`).

## How to set up a common dev environment

First, clone the repo : `git clone --recursive git@github.com:Lasbleic/GDMC.git`

**Note :** *The whole project is made under **_python 2.7_** (MCEdit is kinda old..)*

Then, make sure you have Anaconda for python 2.7 installed ([How to install Anaconda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)), and then PyCharm. I've used PyCharm Professional as we have access with our grenoble-inp.org email adresses.

### Set up the python env

Run all the following commands. It will create an Anaconda environment, and install all necessary packages for MCEdit to run

```
conda create -n minecraftGDMC python=2.7 anaconda

conda activate minecraftGDMC

pip install PyOpenGL

pip install numpy

pip install pygame

pip install pyyaml

pip install pillow

pip install ftputil
```

_Note : (for ~~losers~~ Windows users, also execute_ `pip install pypiwin32` _)_

After this step, you should be able to run `python MCEdit/mcedit.py`



### Set up the PyCharm env

These steps are made to simplify your life.

First, open the folder you've cloned with PyCharm (Right click then 'Open Folder as a PyCharm Project', or directly from PyCharm).

Make sure the Python Interpreter is correctly set (File->Settings->Project:[your_dir]->Python Interpreter and choose Anaconda Python 2.7)

In the 'Run' menu, click on 'Edit Configuration'. Click on the '+' in the top left corner, then select 'Python'.
Name your config as you want (for example "Publish"), and in the 'Script paths' field, search for **'./publish.py'**. If it is not yet field, select the Interpreter (Anaconda Python 2.7).

Recreate another configuration (same steps than before) : 
Click on the '+' in the top left corner, then select 'Python'.
Name your config as you want (for example "Run MCEdit"), and in the 'Script paths' field, search for **'./MCEdit/mcedit.py'**. If it is not yet field, select the Interpreter (Anaconda Python 2.7).

In this config: 
Go to the 'Before launch' section, click on the '+' button on the right.
Then, click on 'Run another configuration', and select 'Publish'.

Explanation :
The src folder should actually be in the stock-filters folder of MCEdit, but it's a dirty place to work. 
There is a script to copy paste src into stock-filters, and this script will be executed by the 'Publish' configuration. So, before executing MCEdit, the filter will be copy-pasted in the right folder.
To be sure there's no mistake, and to facilitate testing, the previous published we'll be saved.


### Visualization tool

If you intend to use the visualization tool, please run

```
conda install kivy -c conda-forge
```