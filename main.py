import subprocess
from checker import check_cfgs_from_tmp
from cfg_downloader import download
import sys

def main():
    if "--no-download" not in sys.argv:
        download()
        pass
    if "--speedtest" in sys.argv:
        print("Speedtest enabled")
        if "--speedtest-threshold" in sys.argv:
            threshold = float(sys.argv[sys.argv.index("--speedtest-threshold")+1])
            print(f"Speedtest threshold: {threshold}")
            check_cfgs_from_tmp(speedtest=True, speedtest_threshold=threshold)
        else:        
            check_cfgs_from_tmp(speedtest=True)
    else:
        check_cfgs_from_tmp()

if __name__ == "__main__":
    main()
    