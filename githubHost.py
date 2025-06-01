import os
from xml.etree import ElementTree as ET
from datetime import datetime

# Config
EPISODE_DIR = "episodes"
FEED_PATH = "feed.xml"
BASE_URL = "https://suibicu.github.io/njo61u3sji4xjp61jp6"

# Load or create feed.xml
if os.path.exists(FEED_PATH):
    tree = ET.parse(FEED_PATH)
    root = tree.getroot()
    channel = root.find("channel")
else:
    root = ET.Element("rss", version="2.0")
    channel = ET.SubElement(root, "channel")
    ET.SubElement(channel, "title").text = "Suibi's Private Podcast"
    ET.SubElement(channel, "link").text = f"{BASE_URL}/feed.xml"
    ET.SubElement(channel, "description").text = "Auto-generated podcast feed"
    ET.SubElement(channel, "language").text = "en-us"
    tree = ET.ElementTree(root)

existing_guids = {item.find("guid").text for item in channel.findall("item")}
new_count = 0

# Scan /episodes directory for .mp3 and .wav files
for filename in sorted(os.listdir(EPISODE_DIR)):
    if not filename.endswith((".mp3", ".wav")):
        continue
    guid = filename
    if guid in existing_guids:
        continue

    file_path = os.path.join(EPISODE_DIR, filename)
    file_size = os.path.getsize(file_path)
    mime_type = "audio/mpeg" if filename.endswith(".mp3") else "audio/wav"

    title = filename.replace("_", " ").replace(".mp3", "").replace(".wav", "").strip()
    pub_date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    file_url = f"{BASE_URL}/{EPISODE_DIR}/{filename}"

    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = title
    ET.SubElement(item, "description").text = "Auto-added from local folder"
    ET.SubElement(item, "enclosure", {
        "url": file_url,
        "type": mime_type,
        "length": str(file_size)
    })
    ET.SubElement(item, "pubDate").text = pub_date
    ET.SubElement(item, "guid").text = guid
    new_count += 1
    print(f"✅ Added: {title}")

# Save updated feed.xml
if new_count:
    tree.write(FEED_PATH, encoding="utf-8", xml_declaration=True)
    print(f"\n🎉 Added {new_count} new episode(s) to feed.xml")
else:
    print("✅ No new audio files to add.")
