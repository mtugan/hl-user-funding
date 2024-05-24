# Data conversion
import json
import requests

# Unix timestamp converts
from datetime import datetime

# Environment
import os
from dotenv import load_dotenv

# Plotting
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

# Environment
load_dotenv()
addr = os.getenv("ADDRESS")


# Request data from Hyperliquid servers
def fetch_hyperliquid_funding():
    url = "https://api-ui.hyperliquid.xyz/info"
    request_data = {
        "type": "userFunding",
        "user": addr,
        "startTime": 0,
    }
    headers = {"Content-Type": "application/json"}
    return requests.post(url, headers=headers, json=request_data)


# Grab only the key values we need
def populate_funding_data(hl_funding_response, keys, assets=[]):
    data = {}

    for item in json.loads(hl_funding_response.text):

        asset = item["delta"]["coin"]

        if len(assets) == 0 or asset in assets:
            timestamp = datetime.fromtimestamp(item["time"] / 1000)

            if asset not in data:
                data[asset] = {"timestamp": [timestamp]}
            else:
                data[asset]["timestamp"].append(timestamp)

            for key in keys:
                key_value = item["delta"][key]

                if key == "usdc":
                    key_value = -float(key_value)

                if key not in data[asset]:
                    data[asset].update({key: [key_value]})
                else:
                    data[asset][key].append(key_value)
    return data


funding_data = populate_funding_data(fetch_hyperliquid_funding(), ["usdc"])

# Create the chart
fig, ax = plt.subplots(figsize=(12, 6))

# Plot the funding data for each asset
for asset, asset_data in funding_data.items():
    ax.plot(asset_data["timestamp"], asset_data["usdc"], label=asset)

# Set the chart title and labels
ax.set_title("Funding Data")
ax.set_xlabel("Time")
ax.set_ylabel("Dollar Amount Paid")

# Format the x-axis to display dates
date_format = mdates.DateFormatter("%m/%d %H:%M")
ax.xaxis.set_major_formatter(date_format)
plt.xticks(rotation=45)

# Add a legend
ax.legend()

# Adjust the layout and display the chart
plt.tight_layout()
plt.show()
