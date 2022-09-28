from Beautiful_meta_analysis import get_height_map, get_surface_type_map, get_biome_map
import Beautiful_settings as settings
from scipy.ndimage import gaussian_filter
import itertools
import numpy as np
import utilityFunctions as utilityFunctions



inputs = (
	("Function to smooth edges of Beautiful Settlement", "label"),
	("Creators: Tim", "label")
	)


def smoothen_edges(level, box, height_map, surface_type_map, domain, x_center, z_center):
	#define subset of box to smoothen
	smooth_min_x = x_center-settings.MAX_OUTER-settings.SMOOTH_AREA
	smooth_max_x = x_center+settings.MAX_OUTER+settings.SMOOTH_AREA
	smooth_min_z = z_center-settings.MAX_OUTER-settings.SMOOTH_AREA
	smooth_max_z = z_center+settings.MAX_OUTER+settings.SMOOTH_AREA

	#reduce maps to subset
	height_map = height_map[smooth_min_x:smooth_max_x, smooth_min_z:smooth_max_z]
	domain = domain[smooth_min_x:smooth_max_x, smooth_min_z:smooth_max_z]
	surface_type_map = surface_type_map[smooth_min_x:smooth_max_x, smooth_min_z:smooth_max_z]

	#apply gaussian filter to height map subset
	smoothened_map = gaussian_filter(height_map, settings.SIGMA)

	#iterate over subset of box and change to smoothened height for all coordinates outside settlement
	pos_top_layer = itertools.product(xrange(smooth_min_x, smooth_max_x),
									  xrange(smooth_min_z, smooth_max_z)
									  )
	for pos in pos_top_layer:

		#transform from level to box coords
		pos_x_map = pos[0] - smooth_min_x
		pos_z_map = pos[1] - smooth_min_z
		block_on_top = False

		#only change if it doesnt belong to settlement domain
		if domain[pos_x_map, pos_z_map] == False:

			height = height_map[pos_x_map, pos_z_map]
			smoothend_height = smoothened_map[pos_x_map, pos_z_map]
			block_type = surface_type_map[pos_x_map, pos_z_map]

			#if block type is non standard (bushes, trees etc., place it on top instead)
			if block_type in (31, 32):
			#	block_on_top = block_type
				block_type = 2

			if block_type == 109:
				block_type = 2

			#lower terrain
			if height >= smoothend_height:

				for y in xrange((box.miny + height), (box.miny + smoothend_height) - 1, -1):
					utilityFunctions.setBlock(level, (0, 0), pos[0] + box.minx, y,
											  pos[1] + box.minz)
					if y == (box.miny + smoothend_height):
						utilityFunctions.setBlock(level, (block_type, 0), pos[0] + box.minx, y,
												  pos[1] + box.minz)

			#elevate terrain
			if height < smoothend_height:

				for y in xrange((box.miny + height), (box.miny + smoothend_height), 1):
					utilityFunctions.setBlock(level, (block_type, 0), pos[0] + box.minx, y,
											  pos[1] + box.minz)

			#place special blocks on top
			if block_type == 2:#
				flower_int = np.random.randint(1, 5)

				if flower_int == 1:
					utilityFunctions.setBlock(level, (np.random.randint(31,33), np.random.randint(0,2)), pos[0] + box.minx,
											  box.miny + smoothend_height + 1,
											  pos[1] + box.minz)



def perform(level,box,options):

	print('nothing was done')


