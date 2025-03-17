import pandas as pd
import os
from git import Repo
from git.exc import GitCommandError

covidfolder = 'data_external/covid19'
print(f"covidfolder: {covidfolder}")

if os.path.isdir(covidfolder):
    try:
        repo = Repo(covidfolder)
        repo.remotes.origin.pull()
    except GitCommandError as e:
        print(f"Error pulling from Git: {e}")
        exit()  # Stop execution if Git pull fails
else:
    try:
        repo = Repo.clone_from('https://github.com/CSSEGISandData/COVID-19.git', covidfolder)
    except GitCommandError as e:
        print(f"Error cloning Git repository: {e}")
        exit()  # Stop execution if Git clone fails

datadir = os.path.join(repo.working_dir, 'csse_covid_19_data', 'csse_covid_19_daily_reports')
print(f"datadir: {datadir}")

try:
    c = pd.read_csv(os.path.join(datadir, '11-13-2022.csv'))
    print(c)
except FileNotFoundError:
  print(f"Error: File 11-13-2022.csv not found in {datadir}")
except pd.errors.EmptyDataError:
  print(f"Error: File 11-13-2022.csv is empty")
except Exception as e:
  print(f"An unexpected error occured: {e}")