# Generative Design in Minecraft

This repository is an entry for the GDMC competition. It challenges competitors to create a settlement generator for Minecraft.

More information available at the [official website](http://gendesignmc.engineering.nyu.edu).

# How to run?

Move the whole repository folder into the MCEdit's filters folder, select a section of the map and call the SettlementGenerator file.

# How can we improve the generator :

- The "wood" adaptability can be improved. I would be interesting if all the buildings which have wood were using the result of my function. Also, the wood selected to build is currently random (between the existing one). It would be better if the random was in proportion of the quantity of each type of wood (like if I have 500 oak and 100 dark oak it would be 1/6 for dark oak and 5/6 for oak). And to finish, the generator need a behavior if he can't find any tree in the area.

- The city is always generated the same way without any consideration for the biome. It could be interesting if the biome influences the blocks used to build the building (the houses would be made of sandstone in the desert, the greenhouse would use yellow glass to represent the sand,...). Also, the Biome could influence the apparition of some building. For example in a desert the park (possible future feature) would be replaced by a well (since the city need water).

- In the review of the judges one of them explain that the city was invaded by lava in one of the map. It would be interesting to add a function that analyze the ground and if it found lava/watern, would build a wall or a dike (will do research on the subject) in order to stop the lava/water.

- Another problem that the judges highlighted is the lack of lighting. Mob were able to spawn and it's a problem (Adrien already correct this issue in his version of the generator)

- The sky scrapers are currently lacking of details and variation. Since they are the thing that give a personality to the city I think we should improve them by adding some balcony, different type of floor (a floor with two little apartment instead of one large) and a first floor which look like an entrance (will work on the design in my mc).

- One of the point of the competition is to have a settlement that look like a real city. One way to do this is to have a lot of different building. Currently the city need office for work (which would be spawn instead of one skyscraper when there is enough population to work inside), grocery store since it's a modern style city and a building for entertainment (a cinema, a park or another thing) 

- A simple thing is the elimination of the tree. Sometime when the city is generated tree are left with half their leaf missing (because they were on the plot during the construction of the house). If a tree is found during the cleaning of the lot, the whole tree is going to be eliminated (by following the leaves and the wood block). (Adrien already correct this issue in his version of the generator)
