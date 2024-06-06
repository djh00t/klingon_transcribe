import subprocess

# ANSI escape codes for colors
BOLD_GREEN = "\033[1;32m"
BOLD_RED = "\033[1;31m"
RESET = "\033[0m"

def install_klingon_logtools():
    # Print initial message without newline
    print("Running Klingon Tools Installer...", end='', flush=True)

    # Run the pip install command
    result = subprocess.run(['pip', 'install', '-U', '-q', 'klingon_tools'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Print OK or ERROR based on the return value
    if result.returncode == 0:
        print(f"\rRunning Klingon Tools Installer...                                      {BOLD_GREEN}OK{RESET}")
    else:
        print(f"\rRunning Klingon Tools Installer...                                        {BOLD_RED}ERROR{RESET}")

    # Import the installed package
    global LogTools
    from klingon_tools import LogTools

# Run the function on import
install_klingon_logtools()

# Release resources
@LogTools.method_state(name="Running garbage collection")
def garbage_collection():
    # Run a general garbage collection
    gc.collect()

@LogTools.method_state(name="Deleting model to free up memory")
def delete_model():
    # Delete the model
    del model

@LogTools.method_state(name="Clearing GPU cache")
def empty_cache():
    # Free up GPU memory
    torch.cuda.empty_cache()                                                                                                       

# Aggregate cleanup methods
def release_resources():
    garbage_collection()
    delete_model()
    empty_cache()
