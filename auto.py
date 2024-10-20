import subprocess
import time

def run_script():
    while True:
        try:
            result = subprocess.run(['python', 'song.py'], check=True)
            print("song.py ran successfully.")
            break  # Exit the loop if the script runs successfully
        except subprocess.CalledProcessError:
            print("song.py failed. Restarting...")
            time.sleep(5)  # Wait for 5 seconds before restarting

if __name__ == "__main__":
    run_script()
