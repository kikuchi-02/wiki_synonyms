import os
import sqlite3
import subprocess
import sys
import urllib.request as urllib

url = "http://compling.hss.ntu.edu.sg/wnja/data/1.1/wnjpn.db.gz"


def download():
    file_name = os.path.basename(url)
    print('download: %s' % url)
    urllib.urlretrieve(url, file_name)
    subprocess.run(['gunzip', file_name])


def search(word):
    file_name = os.path.basename(url).replace('.gz', '')
    if not os.path.isfile(file_name):
        download()

    conn = sqlite3.connect(file_name)
    sql = f"""
    select lemma from word where wordid in (
        select wordid from sense where synset in (
            select synset from sense where wordid in (
                select wordid from word where lemma='{word}'
            )
        )
    )
    """
    words = list(map(lambda x: x[0], conn.execute(sql)))
    return words


if __name__ == "__main__":
    word = sys.argv[1]
    try:
        res = search(word)
        print(res)
    except sqlite3.OperationalError as e:
        print(e)
