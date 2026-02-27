import paramiko
import sys

try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('45.32.40.33', username='root', password='u4C=Evnr_4ajj4Vo', timeout=10)

    commands = """
    set -x
    
    # 1. Kill stale cargo processes
    pkill cargo || true
    pkill rustc || true
    
    # 2. Add 2GB Swap if it doesn't exist
    if [ $(swapon --show | wc -l) -eq 0 ]; then
        fallocate -l 2G /swapfile || dd if=/dev/zero of=/swapfile bs=1M count=2048
        chmod 600 /swapfile
        mkswap /swapfile
        swapon /swapfile
    fi
    free -m
    
    # 3. Build again
    cd /root/zeroclaw_src
    export PATH="$HOME/.cargo/bin:$PATH"
    rm -rf target/release/.fingerprint/* 2>/dev/null
    
    # Run build inline
    cargo build --release
    
    # Replace Binary
    systemctl stop zeroclaw || systemctl --user stop zeroclaw
    cp target/release/zeroclaw /usr/local/bin/zeroclaw
    chmod +x /usr/local/bin/zeroclaw
    systemctl start zeroclaw || systemctl --user start zeroclaw
    systemctl status zeroclaw || systemctl --user status zeroclaw
    """
    
    stdin, stdout, stderr = client.exec_command(commands)
    
    while True:
        line = stdout.readline()
        if not line:
            break
        print(line, end="")

    client.close()
    sys.exit(0)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
