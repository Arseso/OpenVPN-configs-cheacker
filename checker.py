import os
import subprocess
import tqdm

def _check(vpn_name) -> int:
    try:
        
        subprocess.run(
            ["nmcli", "connection", "up", "id", vpn_name],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10.0
            
        )
        
        subprocess.run(
            ["nmcli", "connection", "down", "id", vpn_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        return 0

    except subprocess.CalledProcessError as e:
        print(f"INTERNAL ERROR: {e.stderr}")
        
        subprocess.run(
            ["nmcli", "connection", "delete", "id", vpn_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return 2
    
    except subprocess.TimeoutExpired:
        subprocess.run(
            ["nmcli", "connection", "down", "id", vpn_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        subprocess.run(
            ["nmcli", "connection", "delete", "id", vpn_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return 1
    
def _send_to_nmcli() -> list[str]:
    
    vpn_names = []
    
    for filename in sorted(os.listdir("./tmp")):
        subprocess.run(
            ["nmcli", "connection", "import", "type", "openvpn", "file",  f"./tmp/{filename}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        vpn_names.append(filename.split(".")[0])
    return vpn_names

def _clear_vpn_connections():
    subprocess.run(
            ["chmod", "+x", "./clear_vpn_connections.sh"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    
    subprocess.run(
            ["./clear_vpn_connections.sh"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

def check_cfgs_from_tmp():
    _clear_vpn_connections()
    names = _send_to_nmcli()
    for i in tqdm.trange(len(names), desc='CHECKING'):
        _check(names[i])
    
    


