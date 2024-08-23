import subprocess
from checker import check_cfgs_from_tmp
from cfg_downloader import download
import sys

def main():
    download()
    if "--speedtest" in sys.argv:
        print("Speedtest enabled")
        check_cfgs_from_tmp(speedtest=True)
    else:
        check_cfgs_from_tmp()

if __name__ == "__main__":
    main()
    