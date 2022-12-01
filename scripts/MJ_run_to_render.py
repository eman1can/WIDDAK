import os
import subprocess
from subprocess import Popen, PIPE
import shutil
from time import perf_counter

# Path Fixing Code - Must Be First
import sys
from os import getcwd, environ, chdir
from os.path import split

script_path = getcwd()
sys.path.append(script_path)
while not script_path.endswith('WIDDAK'):
    script_path = split(script_path)[0]
    chdir(script_path)
if 'PYTHONPATH' in environ:
    if script_path + ';' not in environ['PYTHONPATH']:
        environ['PYTHONPATH'] += script_path + ';'
else:
    environ['PYTHONPATH'] = script_path
# End Path Fixing Code

import vox_to_minecraft as vm

def run_markov():
    # Get current working directory
    s_cwd = os.getcwd()

    # Enter the MarkovJunior directory
    os.chdir("MarkovJunior")

    # Run the executable
    print("MarkovJunior start runnning.")
    p = Popen('MarkovJunior.exe', stdin=PIPE)  # NOTE: no shell=True
    # Read the models.xml file when running the executable. Wait to finish.
    p.communicate(bytes("models.xml", "utf-8"))
    print("MarkovJunior end runnning.")

    # Reset working directory to directory at the beginning
    os.chdir(s_cwd)
    # TODO: Utilize 3D Renderer to show VOX Output

def run_multiple_markov(num: int):

    folder_name = "modelsT1_2"

    # Get current working directory
    s_cwd = os.getcwd()

    # Enter the MarkovJunior directory
    os.chdir("MarkovJunior")

    # Clear files in multiple_outputs
    os.chdir("multiple_outputs")
    fns = os.listdir()
    for fn in fns:
        os.remove(fn)
    os.chdir("..")

    # Start Timer
    t1_start = perf_counter()

    for i in range(num):

        success = False

        while not success:
            # Note - if this keeps running, you may have a typo in your .xml file of the rules

            # Run the executable
            print("MarkovJunior start runnning.")
            p1 = subprocess.Popen(["MarkovJunior.exe", "modelsT1_1.xml"])

            p1.wait()
            print("MarkovJunior end runnning.")


            os.chdir("output")
            fns = os.listdir()
            vox_fn = fns[0]
            shutil.copy2(vox_fn, "../resources/rules/" + folder_name + "/ModernHouseOutput.vox")

            # Enter the MarkovJunior directory
            os.chdir("..")

            # Run the executable
            print("MarkovJunior start runnning.")
            p1 = subprocess.Popen(["MarkovJunior.exe", "modelsT1_2.xml"])
            # Popen()
            # p.communicate(bytes("modelsT1_1.xml", "utf-8"))
            p1.wait()
            print("MarkovJunior end runnning.")

            # Check if successful change by seeing if ModernHouseT1 was able to run
            os.chdir("output")
            fns = os.listdir()
            if len(fns) > 0:
                success = True
            os.chdir("..")
        # End of success loop checker.

        # Copy to multiple outputs
        m_folder = "multiple_outputs"
        os.chdir("output")
        fns = os.listdir()
        vox_fn = fns[0]
        shutil.copy2(vox_fn, "../" + m_folder + "/ModernHouseOutput" + str(i) + ".vox")

        # Reset directory to MarkovJunior folder
        os.chdir("..")
    # End of number-of-buildings loop
    t1_stop = perf_counter()
    print("Elapsed time for " + str(num) + " outputs: " + str(t1_stop-t1_start))

    os.chdir(s_cwd)

def run_to_minecraft():
    # run_multiple_markov(1)

    filepath5 = 'MarkovJunior/output/ModernHouse.vox'
    filepath6 = 'MarkovJunior/resources/SavedVoxels/ApartemazementsTiny_1481160288.vox'

    # vm.clear_build_area()
    # template = vm.create_template_from_vox(filepath5, 'Modern House',
    #                                     'modern_house', 'jungle')
    template = vm.create_template_from_vox(filepath6, 'Adobe Village',
                                        'apartemazements', 'forest')
    location = [70, 130, 70]
    vm.visualize_vox_template(template, location)


if __name__ == "__main__":
    run_to_minecraft()

