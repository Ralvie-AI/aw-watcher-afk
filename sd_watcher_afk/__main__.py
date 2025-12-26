import os 
import sys 
import logging 

import psutil

from sd_core.log import setup_logging
from sd_watcher_afk.afk import AFKWatcher
from sd_watcher_afk.config import parse_args

logger = logging.getLogger(__name__)

def is_already_running() -> bool:
    """Checks for another instance of the bundled .exe or script."""
    current_pid = os.getpid()
    
    # If bundled by PyInstaller, sys.executable is the .exe path
    # If running as script, sys.executable is python.exe (we use __file__ instead)
    if getattr(sys, 'frozen', False):
        current_name = os.path.basename(sys.executable)
    else:
        current_name = os.path.basename(__file__)
    
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            # We filter for the name and ensure it's not THIS specific process
            if proc.info['name'] and proc.info['name'].lower() == current_name.lower():
                if proc.info['pid'] != current_pid:
                    return True
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
    return False


def main() -> None:
    """
     Entry point for AFK watcher. Sets up logging starts the watcher and waits for it to finish.
     
     
     @return A tuple containing exit code and error message if there was an error or None otherwise. This is called from sys. exit
    """
    args = parse_args()

    # Set up logging
    setup_logging(
        "sd-watcher-afk",
        testing=args.testing,
        verbose=args.verbose,
        log_stderr=True,
        log_file=True,
    )

    # Check before initializing the watcher or logs
    current_pid = os.getpid()
    logger.info(f"current_pid = > {current_pid}")
    if getattr(sys, 'frozen', False):
        current_name = os.path.basename(sys.executable)
    else:
        current_name = os.path.basename(__file__)

    logger.info(f"current_name = > {current_name}")
    if is_already_running():
        # Using stdout because logs aren't initialized yet
        logger.info("Another instance is already running. Closing this one.")
        sys.exit(0)

    # Start watcher
    watcher = AFKWatcher(args, testing=args.testing)
    watcher.run()


# main function for the main module
if __name__ == "__main__":
    main()
