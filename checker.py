import os
import subprocess
import tqdm

import commands

def _check(vpn_name) -> int:
    try:
        
        commands.connection_up(vpn_name)
        
        commands.connection_down(vpn_name)
        
        return 0

    except subprocess.CalledProcessError as e:
        print(f"INTERNAL ERROR: {e.stderr}")
        
        commands.connection_delete(vpn_name)
        return 2
    
    except subprocess.TimeoutExpired:
        commands.connection_down(vpn_name)
        commands.connection_delete(vpn_name)
        return 1
    
def _send_to_nmcli() -> list[str]:
    
    vpn_names = []
    
    for filename in sorted(os.listdir("./tmp")):
        commands.connection_import(filename)
        
        vpn_names.append(filename.split(".")[0])
    return vpn_names

def _clear_vpn_connections():
    commands.clear_connections_pipeline()

def check_cfgs_from_tmp():
    _clear_vpn_connections()
    names = _send_to_nmcli()
    for i in tqdm.trange(len(names), desc='CHECKING'):
        _check(names[i])
    
    


