import sys
from os import sep
import warnings
warnings.filterwarnings("ignore")

# Managing dependencies and Python path
this_path = str(__file__)  # path to this file
this_path = sep.join(this_path.split(sep)[:-1])  # path to the directory where
sys.path.insert(0, this_path + sep + 'gdmc_http_client_python')  # local dependency to gdmc_http
sys.path.insert(0, this_path + sep + 'src')  # path to our code

from time import time

from settlement import Settlement
from terrain import TerrainMaps

time_opt = "time_opt"  # "10' limit"
debug_opt = "debug_opt"  # "Debug mode: does not catch exceptions in generation"
visu_opt = "visu_opt"  # "Visualization tool: plots iterations of building placement"


def main(**options):
    # Get options
    time_lim: int = options.get(time_opt, None)  # time limit in seconds
    do_debug: bool = options.get(debug_opt, False)
    do_visu: bool = options.get(visu_opt, False)

    t0 = time()
    print("Hello Settlers!")
    # get & parse building zone
    terrain: TerrainMaps = TerrainMaps.request()

    settlement = Settlement(terrain)
    settlement.build_districts(visualize=do_visu)
    t2 = time()
    settlement.build_skeleton(time_lim, do_visu)  # define buildings list and seed them
    print(" computing village skeleton", time() - t2)
    settlement.clean_road_network()
    settlement.define_parcels()  # define parcels around seeds
    # return
    settlement.terraform()
    settlement.generate(terrain, options.get(debug_opt, False))      # build buildings on parcels
    print('{} seconds of execution'.format(time() - t0))

    # Optional erasing of the generated settlement
    if do_debug:
        do_undo = input("Undo ? [y]/n").lower()
        if do_undo in {"", "y"}:
            terrain.undo()


if __name__ == '__main__':
    do_profile = False
    if do_profile:
        # code profiler
        from pstats import Stats, SortKey
        import cProfile
        stats: Stats = cProfile.run(f"main({time_opt}=900)", sort=SortKey.CUMULATIVE)
    else:
        main(debug_opt=False, time_opt=900)

