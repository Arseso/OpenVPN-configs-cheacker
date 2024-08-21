import subprocess
from checker import check_cfgs_from_tmp
from cfg_downloader import download

def main():
    download()
    check_cfgs_from_tmp()

if __name__ == "__main__":
    main()
    