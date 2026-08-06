from gradio_client import Client

print("Connecting to local Fooocus server on port 7865...")
try:
    client = Client("http://127.0.0.1:7865/")
    print("Successfully connected to Fooocus API!")
    print("API Endpoints:", client.view_api(return_format="dict"))
except Exception as e:
    print("Error connecting to Fooocus API:", e)
