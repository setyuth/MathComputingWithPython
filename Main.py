import pandas as pd
import os
from git import Repo
from git.exc import GitCommandError
import subprocess

# Define folder and print for debugging
covidfolder = 'data_external/covid19'

# Check if folder exists and handle Git operations
if os.path.isdir(covidfolder):
    print(f"{covidfolder} exists, attempting to pull updates...")
    try:
        repo = Repo(covidfolder)
        print(f"Repository found at: {repo.working_dir}")
        # Attempt pull with a timeout (Windows workaround)
        try:
            # Use subprocess to enforce a timeout since gitpython doesn't natively support it
            result = subprocess.run(
                ['git', 'pull', 'origin', 'master'],
                cwd=repo.working_dir,
                timeout=30,  # Timeout after 30 seconds
                capture_output=True,
                text=True
            )
            print(f"Pull output: {result.stdout}")
            if result.stderr:
                print(f"Pull errors: {result.stderr}")
        except subprocess.TimeoutExpired:
            print("Git pull timed out after 30 seconds")
            exit()
        except subprocess.CalledProcessError as e:
            print(f"Subprocess error during pull: {e}")
            exit()
        print("Successfully pulled updates from Git repository")
    except GitCommandError as e:
        print(f"Error pulling from Git: {e}")
        exit()
    except Exception as e:
        print(f"Unexpected error with repository: {e}")
        exit()
else:
    print(f"{covidfolder} does not exist, cloning repository...")
    try:
        repo = Repo.clone_from('https://github.com/CSSEGISandData/COVID-19.git', covidfolder)
        print("Successfully cloned repository from GitHub")
    except GitCommandError as e:
        print(f"Error cloning Git repository: {e}")
        exit()

# Construct data directory path
datadir = os.path.join(repo.working_dir, 'csse_covid_19_data', 'csse_covid_19_daily_reports')
print(f"datadir: {datadir}")

# Verify directory exists
if not os.path.isdir(datadir):
    print(f"Error: Directory {datadir} does not exist")
    exit()

# Try to read the CSV file
file_path = os.path.join(datadir, '03-27-2020.csv')
print(f"Attempting to read file: {file_path}")
try:
    c = pd.read_csv(file_path)
    print("File loaded successfully. First 5 rows:")
    print(c.head())
except FileNotFoundError:
    print(f"Error: File 03-27-2020.csv not found in {datadir}")
    print(f"Check if the file exists in the repository or if the clone/pull was successful")
except pd.errors.EmptyDataError:
    print(f"Error: File 03-27-2020.csv is empty")
except Exception as e:
    print(f"An unexpected error occurred: {e}")