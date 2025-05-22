#!/usr/bin/python3

"""
This script is used to generate a list of releases for a target. The results are written
to a file at path `targets/<TARGET_NAME>/releases`. The releases file is used to point to
a specific target version while building it using the tools/captain/run.sh script.
"""

import os
import subprocess
import sys

from datetime import datetime

subprocess.check_call([sys.executable, "-m", "pip", "install", "gitpython"])

from git import Repo  # type: ignore # noqa: E402

links = {
    "libpng": "https://github.com/pnggroup/libpng.git",
    "libsndfile": "https://github.com/libsndfile/libsndfile.git",
    "libtiff": "https://gitlab.com/libtiff/libtiff.git",
    "libxml2": "https://gitlab.gnome.org/GNOME/libxml2.git",
    "lua": "https://github.com/lua/lua.git",
    "openssl": "https://github.com/openssl/openssl.git",
    "php": "https://github.com/php/php-src.git",
    "poppler": "https://gitlab.freedesktop.org/poppler/poppler.git",
    "sqlite3": "https://github.com/sqlite/sqlite",
}

repos = []


def clone_repo(repo_url):
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    local_path = os.path.join(os.getcwd(), repo_name)
    repos.append(local_path)

    repo = None
    if not os.path.exists(local_path):
        repo = Repo.clone_from(repo_url, local_path)
        print(f"Cloned {repo_url}")
    else:
        repo = Repo(local_path)

    return repo


def get_tags(repo):
    # get all tags available
    year_to_tag = {}
    for tag in repo.tags:
        tag_date = tag.tag.tagged_date if tag.tag else tag.commit.committed_date
        year = datetime.fromtimestamp(tag_date).year
        if year not in year_to_tag:
            year_to_tag[year] = tag.name

    year_to_tag_sorted = dict(sorted(year_to_tag.items()))
    min_year = list(year_to_tag_sorted.keys())[0]

    # fill the gaps
    last_tag = 0
    for i in range(min_year, 2025):
        if i in year_to_tag_sorted:
            last_tag = year_to_tag_sorted[i]
        else:
            year_to_tag_sorted[i] = last_tag

    year_to_tag_sorted = dict(sorted(year_to_tag_sorted.items()))
    return year_to_tag_sorted


def get_first_commit_of_year(repo, year):
    since = f"{year}-01-01"
    until = f"{year}-12-31"
    commits = list(repo.iter_commits(rev="HEAD", since=since, until=until))
    return commits[-1].hexsha


for target, link in links.items():
    path_to_releases = os.path.join("targets", target, "releases")

    if isinstance(link, str):  # git repo
        repo = clone_repo(link)
        year_to_tag = get_tags(repo)

        latest_year = max(year_to_tag.keys())
        stable_hash = get_first_commit_of_year(repo, latest_year)

        print(f"Got tags and latest commit of {target}")
        releases = [
            f'{target}_PIONEER="{link}"\n',
            f'{target}_PIONEER_STABLE_COMMIT="{stable_hash}"\n',
        ]
        for i in range(2022, 2025):
            releases.append(f'{target}_LEGACY_{i}="{link}"\n')
            releases.append(f'{target}_LEGACY_{i}_TAG="{year_to_tag[i]}"\n')
    else:  # predefined
        assert isinstance(link, dict)
        releases = [
            f'{target}_PIONEER="{link[2024]}"\n',
        ]
        for i in range(2020, 2025):
            if isinstance(link[i], str):
                releases.append(f'{target}_LEGACY_{i}="{link[i]}"\n')
            else:  # git repo, + tag or commit
                releases.append(f'{target}_LEGACY_{i}="{link[i][0]}"\n')
                releases.append(f'{target}_LEGACY_{i}_TAG="{link[i][1]}"\n')

    with open(path_to_releases, "w") as f:
        for line in releases:
            f.write(line)
    print(f"Wrote to {path_to_releases}")

# clean
all_repos = " ".join(repos)
print(f"rm -rf {all_repos}")
