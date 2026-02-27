import paramiko
import sys
import time

try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("Connecting...")
    client.connect('45.32.40.33', username='root', password='u4C=Evnr_4ajj4Vo', timeout=10)
    print("Connected! Running commands...")
    
    commands = """
    set -x
    export DEBIAN_FRONTEND=noninteractive
    
    cd /root/zeroclaw_src
    export PATH="$HOME/.cargo/bin:$PATH"
    
    rm -f Cargo.lock
    rm -rf target 2>/dev/null
    
    cargo build --release
    
    # Replace Binary
    systemctl --user stop zeroclaw || systemctl stop zeroclaw
    cp target/release/zeroclaw /usr/local/bin/zeroclaw
    chmod +x /usr/local/bin/zeroclaw
    systemctl --user start zeroclaw || systemctl start zeroclaw
    systemctl --user status zeroclaw || systemctl status zeroclaw
    """
    
    stdin, stdout, stderr = client.exec_command(commands)
    
    # Read output line by line to prevent hanging
    while True:
        line = stdout.readline()
        if not line:
            break
        print(line, end="")
        
    exit_status = stdout.channel.recv_exit_status()
    print("STDERR:")
    print(stderr.read().decode())
    
    client.close()
    sys.exit(exit_status)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
