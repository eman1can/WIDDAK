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
#### MarkovJunior/
Utilizing the C# MarkovJunior programming language to load and programmatically modify building templates in a novel way
#### Wave Function Collapse/
A custom wave function collapse algorithm for parceling town centers from environment data and town patterns
#### SMCA/ "Slime Mold Cellular Automata"
Building roads and calculating city centers based off of environmental data utilizing cellular automata
#### Environmental Detection/
Getting environmental data from gdpc and formatting it in a way that is understood by the rest of our code. Also includes things such as resource location, hazard detection, existing structure integration, and more.
#### Blueprints/
Getting blueprint data from third-party sources or hand-build templates for feeding into our markov junior algorithm

Sources:
* [the minecraft wiki blueprints page](https://minecraft.fandom.com/wiki/Village/Structure/Blueprints)
#### Voxel Renderer/
A custom from scratch OpenGL 4.0 voxel renderer streamlined for minecraft texture display for viewing buildings and world slices
### scripts/
This is where tool scripts, such as run markov to render, or sym link live
### examples/
These are minimal examples to showcase a particular functionally, e.x. visualize map
### runner/
This is where the final script for loading a world and utilizing all of our sections will live
### local/
This contains local objects that are NOT pushed to git
