#https://files.lighthouse.storage/dashboard
import requests
def upload_to_lighthouse(filepath, api_key):
    url = "https://node.lighthouse.storage/api/v0/add"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    with open(filepath, 'rb') as f:
        files = {'file': (filepath, f)}
        response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        data = response.json()
        print("CID:", data['Hash'])
        return data['Hash']
    else:
        print("Error:", response.text)
        return None

