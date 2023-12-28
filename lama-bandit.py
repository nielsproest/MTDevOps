import os, subprocess, datetime
from pathlib import Path

import git

Tdir = Path("__lama")

def scan(outfile):
    return subprocess.check_output([
        "bandit","-r",
        "--exit-zero",
        "-f","json",
        "-o",outfile,
        Tdir.resolve()
    ])

repo = git.Repo(Tdir) 

done = []
all_commits = list(repo.iter_commits("master"))
for commit in all_commits:
    date = datetime.datetime.fromtimestamp(commit.committed_date)

    uniq = f"{date.year}-{date.month}-{date.day}"
    if not uniq in done:
        done.append(uniq)
    else:
        continue

    commit_hash = commit.hexsha
    print(uniq, commit_hash)

    os.chdir(Tdir)
    subprocess.check_call([
        "git",
        "checkout",
        commit_hash
    ])
    os.chdir("../")

    scan(f"scans/scan-{uniq}-{commit_hash}.log")
    print("done!")