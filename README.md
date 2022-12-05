# When In Doubt, Destroy All Kelp
The team for the When In Doubt, Only Build Trees GDMC generator for Cal Poly CSC 580

## Team Members

[Ethan Wolfe](https://github.com/eman1can)

[Emily Gavrilenko](https://github.com/EmilyGavrilenko)

[Adam Albanese](https://github.com/Kormaican)

[elconway](https://github.com/elconway)

[Jose Mierzejewski](https://github.com/Jose-Mierzejewski)

[Aidan Barbieux](https://github.com/abarbieu)

# Directory Structure

### requirements.txt - 1
The requirements for ALL parts of WIDDAK

You need to install requirements prior to running setup.py

To do so, run `pip install -r requirements.txt`

### setup.py - 2
Run setup.py to initialize the environment

Make sure that you are running with the project directory as the WIDDAK root. It should auto-correct if you run incorrectly, but it's better to be safe


### gdpc/
This contains all code directly pertaining towards interacting with minecraft

### src/
This is where common code, like vox load / save, and rendering live - Do not put running code here!
### sections/
This is where code for the individual sections of the project live, each section tackling a different part of AI generation.
1. #### MarkovJunior/
    Utilizing the C# MarkovJunior programming language to load and programmatically modify building templates in a novel way

   1. Follow these linked instructions in the "Getting Started" section for setting up your computer to use the GDMC https client server for editing minecraft worlds with python. https://gendesignmc.wikidot.com/wiki:submission-httpserver
   2. Open the forge mod version of minecraft that you setup in the first step. 
   3. Create a new minecraft world. Set mode to Creative. A Flat world will be easier to see the generation, but it works in any minecraft terrain. 
   4. Use command `/setbuildarea x0 y0 z0 x1 y1 z1`to set the build area to be cleared for python generation. In a minecraft world, X and Z are horizontal, Y is vertical. Here is an example value: `/setbuildarea 39 163 385 90 184 436`
   5. Open MJ_run_to_render.py and run the definition run_to_minecraft()

2. #### Wave Function Collapse/
    A custom wave function collapse algorithm for parceling town centers from environment data and town patterns
3. #### nca/encasm "Evolved Neural Cellular Automata Slime Mold"
    Building roads and calculating city centers based off of environmental data utilizing cellular automata
4. #### Environmental Detection/
    Getting environmental data from gdpc and formatting it in a way that is understood by the rest of our code. Also includes things such as resource location, hazard detection, existing structure integration, and more.
5. #### Blueprints/
    Getting blueprint data from third-party sources or hand-build templates for feeding into our markov junior algorithm.  
    - Sources: [the minecraft wiki blueprints page](https://minecraft.fandom.com/wiki/Village/Structure/Blueprints)
6. #### Voxel Renderer/
    A custom from scratch OpenGL 4.0 voxel renderer streamlined for minecraft texture display for viewing buildings and world slices

### scripts/
This is where tool scripts, such as run markov to render, or sym link live
### examples/
These are minimal examples to showcase a particular functionally, e.x. visualize map
### runner/
This is where the final script for loading a world and utilizing all of our sections will live
### local/
This contains local objects that are NOT pushed to git
