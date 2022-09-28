This code creates a procedurally generated city based on Eixample, Barcelona.

The program is written to work for Python 3.6 or newer. The required modules are listed in requirements.txt

This script works combined with the [Minecraft HTTP Interface Mod](https://github.com/nilsgawlik/gdmc_http_interface).
Follow the installation instructions in the above github file to install the mod and the Forge Mod launcher which are required to run our code.

After a succesful installation the city can be spawned by running the main.py file, no arguments required. By default it places structures at origin 0,0,0 within a 128 by 128 horizontal space. This can be changed by setting the current buildarea with the `/setbuiltarea fromX fromY fromZ toX toY toZ` command in Minecraft.

In `main.py`, the variable `USE_THREADING` can be set to `True`. This will enable multi-threading, which somewhat speeds up the generation process. Due keep in mind that in very large building areas (eg. larger than ~200x200) this may slow down the process instead of speeding it up, and can even crash the Forge Minecraft server due to it being overwhelmed by requests. 
