import requests
import subprocess
import threading

def send_to_discord_webhook(message, webhook_url):
    data = {
        'content': message
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(webhook_url, json=data, headers=headers)

    if response.status_code == 200:
        print("Message sent successfully to Discord!")
    else:
        print(f"Failed to send message to Discord. Status code: {response.status_code}")

def capture_app_logs(command, webhook_url):
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

        while True:
            output = process.stdout.readline()
            if not output and process.poll() is not None:
                break
            if output:
                # Print the output to the terminal (optional)
                print(output.strip())
                # Send the output to Discord
                send_to_discord_webhook(output.strip(), webhook_url)

    except Exception as e:
        print(f"Error capturing logs: {e}")

# Replace 'YOUR_DISCORD_WEBHOOK_URL' with the actual URL of your Discord webhook
discord_webhook_url = 'https://discord.comEioTq9X-QrnJW1CrsJv7MsO_mnAr3XOsTddDOHp0gXCFxmkAhGDYy8lUxcOlM2JPMnZ7'

# Replace 'YOUR_COMMAND' with the command that starts your application
command_to_run = 'python3 ex.py'

# Create a thread to capture and send logs
log_thread = threading.Thread(target=capture_app_logs, args=(command_to_run, discord_webhook_url))

# Start the thread
log_thread.start()

# Wait for the thread to finish (this is optional and depends on your application's lifecycle)
log_thread.join()
