import os
from subprocess import Popen, PIPE


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

if __name__ == "__main__":
    run_markov()


