# Chaotic Future Building Complex - Submission for GDMC 2021

## How To Run ##

1. Install dependencies in requirements.txt  (exact version numbers don't matter)
2. (Assuming Minecraft and the http interface are running, and a build area is set)
3. run main.py -> `python main.py` (python version >= 3.7)
4. the colorful windows that pop up are just some debug visualisations that I left in for fun and to show that progress is being made

## Info ##

### credits / license ###

This submission is based on the open source code in https://github.com/nilsgawlik/gdmc_http_client_python

All additional work and modifiations were done by Nils Gawlik. 

This code is licensed under the MIT license.

### concept

With this generator my goal was to create something that makes use of image processing algorithms and explores to which extent they can be used for this competition. There are different steps to the generation process, but ultimately they are all variations of the same concept: Interpret the build area as a 2d image and then use image processing algorithms to transform it into something new. Basically all operations in this generator are done in this pixel representation, including operations which you might normally think of as generating discrete objects - like placing doors or building staircases. 

This approach led to a cityscape which is more dynamic and chaotic then other methods which make use of a rigid structure or hierarchy. I made sure that the algorithm allows for 'happy accidents' like narrow gaps, walkways, overhangs and buildings that connect to each other, which are resolved by later image processing steps to their best ability, often creating interesting emergent outcomes.

As the generator stands right now, it should be seen as a proof-of-concept, showcasing the viability of this method. The code is experimental and cobbled together, and lacks much of the attention to detail that would make the settlement feel more alive.

### tech
The generator is written in Python and makes heavy use of numpy and OpenCV to calculate the image processing steps.

It is made for use with the GDMC Http Interface Mod, which can place blocks in Minecraft while the game is running. To make good use of this foundation the generator places blocks as changes are calculated, and sometimes places structures to hint at the rough shape of the settlement as it's being generated.

If you look at the generation in Minecraft you can see the rough approach of the generator:

1. flatten the ground, lay out the rough footprint of the city and cut down the trees in the build area
2. place a large amount of boxes in the world, according to a heuristic based on height and proximity to other boxes. These determine the shape of the buildings
3. iterate horizontal slices bottom to top and generate platforms using a combination of morphological image operations
4. iterate horizontal slices top to bottom generating staircases, which try to stick close to existing structures and connect the platforms to other platforms or the ground
5. iterate horizontal slices bottom to top filling in most of the blocks making up the settlement according to an assortment of simple filters
6. iterate horizontal slices bottom to top, placing a door for every building and furniture within the buildings

### what can be improved

The next big step would be to look into how the space might be used and inhabited. The generator right now mostly creates interesting shapes, with some understanding of usage in terms of traversibility and basic categories (staircase, platform, indoors, outdoors, roof, etc.). It would be very interesting to analyze the created space with a pathfinding algorithm and agent simulations to find high traffic areas, dead ends, inaccesible areas, and so on. Then a much more interesting zoning could be generated (residential/commerical, poor/wealthy, high/low traffic, polluted/clean, etc.). Combined with other heuristics like vertical height or proximity to water sources, it would be a good foundation to add a lot more details to tell a narrative and make the world feel more alive.

There is also space for improvement in terms of adaptability. This approach is very suited to adapt to existing terrain, because the original block data of the world and the heightmaps can be fed into the image processing algorithms with very little translation effort. Yet, this generator only does the bare minimum because adaptability was not the main focus.

On the tech side, it would be useful to look through the code, find commonly used approaches and see if they could be abstracted into an external module. This should clean up the script and make it more readable. It would also be useful to save the intermediate state of the algorithm between steps. This way individual steps could iterated on without restarting the entire generator (One way to do this would be through a Jupyter notebook, but other methods exist as well).
