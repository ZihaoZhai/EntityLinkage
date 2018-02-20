# EntityLinkage
This repository focuses on grab topic words refereing to the same real life entity from input dataset and create a graph with the output.

### rltk Download & Configuration
This code use similarity and distance fucntions from rltk package, so that we should configure rltk first. Here is the Github link.
```
https://github.com/usc-isi-i2/rltk
```
##### Pycharm
Just add the rltk package to the root path.
##### Sublime
You should install rely first. Go in to the rltk folder where the file `requirements.txt` exist and run the following command.
```
pip install -r requirements.txt
```

### One last thing before running
Before running the code, you should change the variable `packagePath` to the path of your rltk package. Besides, there is another way for Pycharm, you can just directly delete the two lines.
```
packagePath='/Users/abc/Desktop/rltk'
```
```
sys.path.append(packagePath)
```
After that, you can run the code.
