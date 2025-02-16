import os
import consul
import hvac
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
app.secret_key = "some_random_secret_for_demo"  # For flashing messages or session usage

# Environment variables from docker-compose
CONSUL_HOST = os.getenv("CONSUL_HOST", "consul")
VAULT_HOST = os.getenv("VAULT_HOST", "vault")
VAULT_TOKEN = os.getenv("VAULT_TOKEN", "root")  # Dev mode token, not for production

# Consul & Vault clients
def get_consul_client():
    return consul.Consul(host=CONSUL_HOST, port=8500)

def get_vault_client():
    return hvac.Client(url=f"http://{VAULT_HOST}:8200", token=VAULT_TOKEN)

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Show a web page with forms to:
      - Set a Consul key
      - Get a Consul key
      - Set a Vault secret
      - Get a Vault secret
    Handle form submissions and display results.
    """
    result_message = None

    # Check which form was submitted (if any)
    if request.method == "POST":
        form_type = request.form.get("form_type")
        
        if form_type == "set_consul":
            key = request.form.get("consul_key")
            value = request.form.get("consul_value")
            if key and value is not None:
                c = get_consul_client()
                c.kv.put(key, value)
                result_message = f"Set Consul key '{key}' with value '{value}'"
        
        elif form_type == "get_consul":
            key = request.form.get("consul_key_get")
            if key:
                c = get_consul_client()
                index, data = c.kv.get(key)
                if data and data.get("Value"):
                    value = data["Value"].decode()
                    result_message = f"Consul key '{key}' => '{value}'"
                else:
                    result_message = f"Consul key '{key}' not found."
        
        elif form_type == "set_vault":
            secret_path = request.form.get("vault_path")
            secret_key = request.form.get("vault_secret_key")
            secret_value = request.form.get("vault_secret_value")
            if secret_path and secret_key and secret_value is not None:
                client = get_vault_client()
                # Store as JSON dict
                client.secrets.kv.v2.create_or_update_secret(
                    path=secret_path,
                    secret={secret_key: secret_value}
                )
                result_message = f"Stored in Vault: path='{secret_path}' => {{'{secret_key}': '{secret_value}'}}"
        
        elif form_type == "get_vault":
            secret_path = request.form.get("vault_path_get")
            if secret_path:
                client = get_vault_client()
                try:
                    read_response = client.secrets.kv.v2.read_secret_version(path=secret_path)
                    secret_data = read_response["data"]["data"]  # dictionary
                    result_message = f"Vault path '{secret_path}' => {secret_data}"
                except Exception as e:
                    result_message = f"Error reading '{secret_path}' from Vault: {str(e)}"
        
    return render_template("index.html", result_message=result_message)

if __name__ == "__main__":
    # Run Flask on port 5010, accessible on all interfaces
    app.run(host="0.0.0.0", port=5010, debug=True)
