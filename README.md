# Sky Generator
This is a sky generator that calculates a physically based sky which is based on an improved version of [Nishita](https://www.scratchapixel.com/lessons/procedural-generation-virtual-worlds/simulating-sky/simulating-colors-of-the-sky) 1993 single scattering model.

![Sky](https://lh3.googleusercontent.com/pw/ACtC-3dvQTeRSLtduEXAtJ3GmZpDoqHydyYjoURkHCscSNFMtOLUcSQJPoSJOQ6As8aWnZkym-DsuMhXVtjlaAAnTSAP3pV0-KYMYWW33-hjsv-0HFCZUZlBoVyWMOXZ7LCWejSUII5RAb--_8kdhFEwIzBmGw=w1024-h256-no?authuser=0)

### Install
* Install **Python 3.8** or a later version
* Install pip library
```
sudo apt install python3-pip
```
* Install numpy library
```
pip3 install numpy
```
* Install pillow library
```
pip3 install pillow
```

### Run
To run the code, enter:
```
python3 main.py
```

### How it works
When finishing, the program will show the rendered sky image with the OS image visualizer.
To change the sky parameters, just change them in the `properties.py` file, there you will find the sun rotation, camera position altitude along with other settings.
