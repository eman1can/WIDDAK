import numpy as np
import ca_environment as caenv
import math
from bcolors import bcolors

'''
env = caenv.CAEnvironment("slime_eg")
env.gen_padded_food()
env.innoculate()
env.display()

ag = caag.CAAgent("Lame Agent")
def lame_rules(chunk, env):
    return [1] * env.n_channels

ag.set_rule_func(lame_rules)

rag = caag.CAAgent("Random Agent")
def rand_rules(chunk, env):
    return np.random.random(env.n_channels)
rag.set_rule_func(rand_rules)
print(ag.display())
print(rag.display())


env.start_new_video(channels=(env.food_i, env.life_i), cmaps = (cm.copper,cm.gray))
for _ in range(30):
    # ag.apply_to_env(env, log=True, vid_speed=3)
    rag.apply_to_env(env, log=True, vid_speed=5)
env.display()
Video(env.save_video())
'''


class CAAgent:

    # For slime mold/traditional agenst
    apply_rules = None

    # For random walk agents
    apply_walk = None
    foveal_size = 1  # arbitrary for now
    n_spatial_chs = 2  # arbitrary for now

    # apply_rules must be in the form f()

    def __init__(self, id, kernel="von_n"):
        self.id = id
        self.kernelid = kernel
        # ----- Neighborhood/Channel Parameters -----
        moore = (np.array([1,  1,  1,  0,  0,  -1, -1, -1]),
                 np.array([-1,  0,  1, -1,  1,  -1,  0,  1]))  # Moore neigh indices

        von_n = (np.array([-1,  0,  0, 1]),
                 np.array([0, -1,  1,  0]))  # Von Neumann neighborhood indices

        moore_f = (np.array([1,  1,  1,  0,  0,  0,  -1, -1, -1]),
                   np.array([-1,  0,  1, -1,  0,  1,  -1,  0,  1]))  # Includes center

        von_n_f = (np.array([-1,  0,  0,  0, 1]),
                   np.array([0, -1,  0,  1,  0]))  # Includes center

        if kernel == "moore":
            self.kernel = moore
            self.kernel_full = moore_f  # Incliudes center
        else:
            self.kernel = von_n
            self.kernel_full = von_n_f  # Incliudes center

        self.n_neighs = len(self.kernel[0])

    def display(self):
        return ("CAAgent ID: {0}" +
                "\n\tKERNEL: {1}" +
                "\n\tAGENT_TYPE: {2}" +
                "{3}").format(self.id, self.kernelid,
                              'foveal_walk' if self.apply_walk is not None else 'slime mold',
                              "\n\t\tFOVEAL_CHs: {0}\n\t\tSPATIAL_CHs: {1}".format(self.foveal_size, self.n_spatial_chs) if self.apply_walk is not None else "")
        # (f"CAAgent, ID: {self.id}" +
        #  "\n\tAGENT TYPE: " +
        #  f"{'foveal walk' if self.apply_rules is None else('slime_mold' if self.apply_walk is None else 'no ruleset')}" +
        #  f"{f'\n\t\tfoveal_size: {self.foveal_size}\n\t\tn_spatial_channels: {self.n_spatial_chs}' if self.apply_walk is not None else ''}"
        #  "\n\tKERNEL: {self.kernelid}\n\t")

    def set_rule_func(self, func):
        self.apply_rules = func

    def set_walk_func(self, func):
        self.apply_walk = func

    def n_walk_inputs(self):
        return len(self.kernel_full[0]) * (self.n_spatial_chs + 1) + self.foveal_size

    def n_walk_outputs(self):
        return 2 + self.n_spatial_chs + self.foveal_size

    # Stochastically applies agent to every alive cell
    # !! Rules must be independent, ie. application order doesn't matter
    def apply_to_env(self, env: caenv.CAEnvironment, log=False, vid_speed=10, dropout=0.5):
        if self.apply_rules is None:
            print(bcolors.WARNING +
                  "ca_agent.py:apply_to_env: Must set rule function before applying to an environment" + bcolors.ENDC)
            return

        if dropout <= 1:
            inds = np.random.choice(
                (env.cutsize)*(env.cutsize), (int)((env.cutsize)*(env.cutsize)*dropout))
        else:
            inds = np.arange(0, env.cutsize*env.cutsize)
        coords = np.unravel_index(inds, (env.cutsize, env.cutsize))

        total_steps = 0
        for i, j in zip(coords[0]+1, coords[1]+1):
            input = env.channels[:, self.kernel_full[0] + i,
                                 self.kernel_full[1]+j]
            if input[env.life_i].sum() > 0:
                desires = self.apply_rules(input.flatten(), env)
                env.update_chunk(i, j, desires)

                if log and vid_speed < 10 and total_steps % (math.pow(2, vid_speed)) == 0:
                    env.add_state_to_video()

                total_steps += 1
        if log:
            env.add_state_to_video()
