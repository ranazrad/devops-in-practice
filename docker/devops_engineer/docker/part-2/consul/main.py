import os
import time

import consul
import hvac

def main():
    # Get environment variables (set in docker-compose.yml)
    consul_host = os.getenv("CONSUL_HOST", "localhost")
    vault_host = os.getenv("VAULT_HOST", "localhost")

    print(f"[*] Using Consul host: {consul_host}")
    print(f"[*] Using Vault host: {vault_host}")

    # 1. Connect to Consul
    c = consul.Consul(host=consul_host, port=8500)

    # 2. Connect to Vault
    #    The root token is 'root' (set in the Vault container environment).
    client = hvac.Client(url=f"http://{vault_host}:8200", token="root")

    # Let's wait a little bit for Vault and Consul to fully initialize
    # (especially helpful if you see "Connection refused" on the first attempt).
    time.sleep(5)

    # Verify connections
    try:
        consul_leader = c.status.leader()
        if consul_leader:
            print(f"[+] Consul is connected. Leader: {consul_leader}")
        else:
            print("[-] Could not determine Consul leader. Check Consul logs.")

        is_vault_sealed = client.sys.is_sealed()
        print(f"[+] Vault sealed?: {is_vault_sealed}")

    except Exception as e:
        print(f"[-] Error checking Consul or Vault status: {e}")
        return

    # 3. Store a key-value pair in Consul
    key_path = "myapp/config/variable"
    consul_value = "Hello from Consul!"
    print(f"[*] Putting key '{key_path}' in Consul with value: {consul_value}")
    c.kv.put(key_path, consul_value)

    # 4. Retrieve the key from Consul
    index, data = c.kv.get(key_path)
    if data and "Value" in data and data["Value"]:
        retrieved_value = data["Value"].decode()
        print(f"[+] Retrieved from Consul: {retrieved_value}")
    else:
        print(f"[-] Failed to retrieve '{key_path}' from Consul")

    # 5. Store a secret in Vault (KV v2 path "myapp/secret")
    vault_secret_path = "myapp/secret"
    secret_data = {"password": "vaultPass123"}
    print(f"[*] Writing secret to Vault at '{vault_secret_path}' with data: {secret_data}")
    client.secrets.kv.v2.create_or_update_secret(
        path=vault_secret_path,
        secret=secret_data
    )

    # 6. Retrieve the secret from Vault
    try:
        read_response = client.secrets.kv.v2.read_secret_version(path=vault_secret_path)
        vault_password = read_response["data"]["data"]["password"]
        print(f"[+] Retrieved from Vault: {vault_password}")
    except Exception as e:
        print(f"[-] Error reading from Vault: {e}")

    print("[*] Demo completed successfully.")

if __name__ == "__main__":
    main()
