import os
import subprocess
import tqdm
import speedtest as st
import commands

def _check_workable(vpn_name: str, speedtest: bool, speedtest_threshold: float) -> int:
    try:
        
        commands.connection_up(vpn_name)
        
        if speedtest:
            speed = st.Speedtest()
            speed.get_best_server()
            speed = speed.download() / 2**23
            if speed >= speedtest_threshold:
                commands.connection_speed_modify(vpn_name, speed)
                commands.connection_down(vpn_name)
            else:
                commands.connection_delete(vpn_name)
        return 0
    
    except st.SpeedtestBestServerFailure:
        commands.connection_delete(vpn_name)
        return 2
    
    except st.ConfigRetrievalError:
        commands.connection_delete(vpn_name)
        return 2

    except subprocess.CalledProcessError as e:
        commands.connection_delete(vpn_name)
        print(e.stderr)
        return 2
    
    except subprocess.TimeoutExpired:
        commands.connection_delete(vpn_name)
        return 1
    
def _send_to_nmcli() -> list[str]:
    
    vpn_names = []
    
    for filename in sorted(os.listdir("./tmp")):
        commands.connection_import(filename)
        
        vpn_names.append(filename.split(".")[0])
    return vpn_names

def _clear_vpn_connections():
    print("Cleaning ovpn configs")
    commands.clear_connections_pipeline()

def check_cfgs_from_tmp(speedtest: bool = False, speedtest_threshold: float = 0):
    _clear_vpn_connections()
    names = _send_to_nmcli()
    for i in tqdm.trange(len(names), desc='CHECKING'):
        _check_workable(names[i], speedtest, speedtest_threshold)
        
