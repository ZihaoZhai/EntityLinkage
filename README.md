# EntityLinkage
This repository focuses on grab topic words refereing to the same real life entity from input dataset and create edges between nodes with the output.

### EntityLinkage Download
Git clone the EntityLinkage package with the following command.
```
$ git clone https://github.com/ZihaoZhai/EntityLinkage.git
```

### rltk Download & Configuration
This code use similarity and distance fucntions from rltk package, so that we should download and configure rltk first. Here is the command.
```
$ git clone https://github.com/usc-isi-i2/rltk
```
You should add rely first. Run the following commands to go into the rltk folder where the file `requirements.txt` exist and add rely.
```
$ cd rltk
$ pip install -r requirements.txt
```
### Run code
Now you should be in the place where both EntityLinkage and rltk are, and then use the command to go into the EntityLinkage folder and run the code.
```
$ cd EntityLinkage
python [code-file-name] [input-path] [output-path]
```
If your EntityLinkage and rltk are in the same outer folder, the default rltk path should work. If not, please add the rltk path after your command and use space to separate like following.

```
python [code-file-name] [input-path] [output-path] [rltk-path]
```
Because of the different format of the Haiti and Nepal json elements, we have to run different codes to get the result. Here, we have created sample dataset similar to each of them to test. Thus, we can run them with comands as follows.
```
$ python HaitiClustering.py /sampleHaitiJsonInput/ /sampleHaitiJsonOutput/
$ python NepalClustering.py /sampleNepalJsonInput/ /sampleNepalJsonOutput/
```
or if your rltk is not in the default path
```
$ python HaitiClustering.py /sampleHaitiJsonInput/ /sampleHaitiJsonOutput/ ../rltk
$ python NepalClustering.py /sampleNepalJsonInput/ /sampleNepalJsonOutput/ ../rltk
```
