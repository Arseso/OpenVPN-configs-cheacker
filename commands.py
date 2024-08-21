import subprocess

def clear_connections_pipeline():
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

def rmdir_tmp():
    subprocess.run(
        ["rm", "-rf", "./tmp"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
def mkdir_tmp():
    subprocess.run(
        ["mkdir", "tmp"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
def connection_import(filename):
    subprocess.run(
            ["nmcli", "connection", "import", "type", "openvpn", "file",  f"./tmp/{filename}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    
def connection_up(vpn_name):
    subprocess.run(
            ["nmcli", "connection", "up", "id", vpn_name],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10.0
            
        )
    
def connection_down(vpn_name):
    subprocess.run(
            ["nmcli", "connection", "down", "id", vpn_name],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10.0
            
        )

def connection_delete(vpn_name):
    subprocess.run(
            ["nmcli", "connection", "delete", "id", vpn_name],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10.0
            
        )