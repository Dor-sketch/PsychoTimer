"""
This is the main file for the program. It loads the configuration file, sets up
the program, and manages the threads and the timer.
"""

import configparser
import sys
from my_setup import SetupManager
from thread_manager import ThreadManager
from io_util import screen


config = configparser.ConfigParser()
config.read('config.ini')
five_min = config.getint('Timer', 'warning_time', fallback=300)
twenty_min = config.getint('Timer', 'chapter_time', fallback=1200)


if __name__ == "__main__":
    print("Welcome to the Audiobook Synthesizer!")
    try:
        with SetupManager() as setup_manager:
            synthesizer, chapters, extra_essay = setup_manager.get_setup()
            print("Setup complete. Press any key to begin.")
        with ThreadManager(synthesizer, chapters, extra_essay) as thread_manager:
            for chapter in range(thread_manager.chapters):
                thread_manager.run_threads(chapter)
                print(f"Chapter {chapter + 1} complete.")
            thread_manager.exit_flag.set()
    except KeyboardInterrupt:
        print("Interrupted! Exiting...")
        screen.clear()
        screen.addstr(0, 0, "Interrupted! Exiting...")
        screen.refresh()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        sys.exit()
