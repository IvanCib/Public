
import tkinter as tk
from tkinter import messagebox
import requests

def fetch_channels(portal_url, mac_address):
    headers = {
        'User-Agent': 'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/533.3',
        'Referer': portal_url
    }
    params = {
        'type': 'stb',
        'action': 'get_all_channels',
        'mac': mac_address
    }
    response = requests.get(f"{portal_url}/portal.php", headers=headers, params=params)
    return response.json()

def convert_to_m3u(channels):
    m3u_content = "#EXTM3U\n"
    for channel in channels.get('js', []):
        name = channel.get('name', 'Unknown')
        cmd = channel.get('cmd', '')
        # Example grouping logic (can be expanded)
        if 'USA' in name:
            group = 'USA'
        elif 'UK' in name:
            group = 'UK'
        elif 'Sports' in name:
            group = 'Sports'
        elif 'Movies' in name:
            group = 'Movies'
        else:
            group = 'Other'
        m3u_content += f"#EXTINF:-1,{name} [{group}]\n{cmd}\n"
    with open("channels.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    messagebox.showinfo("Success", "M3U file saved as channels.m3u")
    return "channels.m3u"

def upload_to_catbox(file_path):
    with open(file_path, 'rb') as f:
        files = {'fileToUpload': f}
        response = requests.post('https://catbox.moe/user/api.php', files=files, data={'reqtype': 'fileupload'})
    return response.text

def on_fetch_channels():
    portal_url = url_entry.get()
    mac_address = mac_entry.get()
    hosting_link = hosting_entry.get()
    try:
        channels = fetch_channels(portal_url, mac_address)
        if 'js' in channels:
            m3u_file = convert_to_m3u(channels)
            catbox_link = upload_to_catbox(m3u_file)
            messagebox.showinfo("Upload Success", f"M3U file uploaded to Catbox: {catbox_link}\nHosting link: {hosting_link}")
        else:
            messagebox.showerror("Error", "No channels available or incorrect MAC address.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

root = tk.Tk()
root.title("IPTV M3U Converter")

tk.Label(root, text="Stalker Portal URL:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)
url_entry.insert(0, 'http://egaletv.cc/c')

tk.Label(root, text="MAC Address:").pack(pady=5)
mac_entry = tk.Entry(root, width=50)
mac_entry.pack(pady=5)
mac_entry.insert(0, '00:1A:79:5D:4C:E6')

tk.Label(root, text="Hosting Link:").pack(pady=5)
hosting_entry = tk.Entry(root, width=50)
hosting_entry.pack(pady=5)

tk.Button(root, text="Fetch Channels and Convert to M3U", command=on_fetch_channels).pack(pady=10)

root.mainloop()
