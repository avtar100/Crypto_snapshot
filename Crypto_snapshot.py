"""
Crypto Snapshot CLI Tool
Author: Avtar Mohan Raj
Description: Fetches real-time cryptocurrency price data and exports to CSV.
"""

import argparse
import csv
import requests
from datetime import datetime

API_URL = "https://api.coingecko.com/api/v3/simple/price"


def fetch_crypto_data(coin="bitcoin", currency="usd"):
    params = {
        "ids": coin,
        "vs_currencies": currency
    }

    headers = {
        "User-Agent": "CryptoSnapshotTool/1.0"
    }

    response = requests.get(API_URL, params=params, headers=headers, timeout=10)
    response.raise_for_status()

    data = response.json()

    if coin not in data:
        raise ValueError(f"Invalid coin name: {coin}")

    return data[coin][currency]


def save_to_csv(coin, currency, price, output_file):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["coin", "currency", "price", "timestamp"])
        writer.writerow([coin, currency, price, timestamp])


def main():
    parser = argparse.ArgumentParser(
        description="Fetch real-time cryptocurrency price and save to CSV."
    )

    parser.add_argument(
        "--coin",
        default="bitcoin",
        help="Cryptocurrency name (default: bitcoin)"
    )

    parser.add_argument(
        "--currency",
        default="usd",
        help="Currency type (default: usd)"
    )

    parser.add_argument(
        "--out",
        default="crypto_data.csv",
        help="Output CSV filename"
    )

    args = parser.parse_args()

    try:
        print(f"[+] Fetching {args.coin} price in {args.currency}...")
        price = fetch_crypto_data(args.coin, args.currency)
        save_to_csv(args.coin, args.currency, price, args.out)
        print(f"[+] Saved data to {args.out}")
    except Exception as e:
        print(f"[!] Error: {e}")


if __name__ == "__main__":
    main()
