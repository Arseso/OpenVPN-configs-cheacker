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
    subprocess.Popen(
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
        )

def connection_delete(vpn_name):
    subprocess.run(
            ["nmcli", "connection", "delete", "id", vpn_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

def speedtest_as_csv():
    result = subprocess.run(
            ["speedtest-cli","--csv"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    return result

def connection_speed_modify(vpn_name: str, speed: float):
    subprocess.Popen(
        ["nmcli", "connection", "modify", f"{vpn_name}", "connection.id", f"{vpn_name} {speed:.2f}MB/s"]
    )