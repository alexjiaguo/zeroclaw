import paramiko
import sys

try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('45.32.40.33', username='root', password='u4C=Evnr_4ajj4Vo', timeout=10)

    # 1. First, check if cargo is stuck on a specific build
    stdin, stdout, stderr = client.exec_command("ps -eo pid,etimes,command | grep rustc | grep -v grep")
    print("Running rustc instances:")
    print(stdout.read().decode())
    
    # 2. Kill the hanging processes if they exist and are over 10 minutes (600 seconds)
    stdin, stdout, stderr = client.exec_command("awk '$2 > 600 {print $1}' <(ps -eo pid,etimes,command | grep rustc | grep -v grep) | xargs -r kill -9")
    
    client.close()
    sys.exit(0)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
