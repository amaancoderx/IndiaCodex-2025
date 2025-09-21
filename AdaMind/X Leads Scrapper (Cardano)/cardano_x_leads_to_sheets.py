#!/usr/bin/env python3
"""
cardano_x_leads_to_sheets.py

Searches X (x.com) for Cardano-related accounts for a given topic and saves leads to Google Sheets.

Requirements:
  pip install requests gspread google-auth python-dotenv

Setup:
  - Create a Google service account key (JSON) and share the target sheet with the service account email.
  - Put path to JSON in env var SHEET_CREDENTIALS or in .env
  - Put Sheet ID in env var SHEET_ID
  - Put your APIFY token in env var APIFY_TOKEN
  - Optionally set SHEET_TAB (sheet/tab name), RESULTS_PER_REQUEST (int)

Usage:
  python cardano_x_leads_to_sheets.py --topic "cardano nft artists"
"""

import os
import time
import json
import argparse
import re
from typing import List, Dict, Optional
from datetime import datetime

import requests
from dotenv import load_dotenv

# Google Sheets
import gspread
from google.oauth2.service_account import Credentials

# ---------------------------
# Load config
# ---------------------------
load_dotenv()

APIFY_TOKEN = os.getenv("APIFY_TOKEN")
SHEET_CREDENTIALS = os.getenv("SHEET_CREDENTIALS")  # path to service account json
SHEET_ID = os.getenv("SHEET_ID")
SHEET_TAB = os.getenv("SHEET_TAB", "Leads")
RESULTS_PER_REQUEST = int(os.getenv("RESULTS_PER_REQUEST", "100"))

APIFY_RUN_SYNC_URL = "https://api.apify.com/v2/acts/apify~google-search-scraper/run-sync-get-dataset-items"

# Basic validation
missing = []
if not APIFY_TOKEN:
    missing.append("APIFY_TOKEN")
if not SHEET_CREDENTIALS:
    missing.append("SHEET_CREDENTIALS")
if not SHEET_ID:
    missing.append("SHEET_ID")
if missing:
    raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}. Put them in a .env file or export them.")

# ---------------------------
# Helpers
# ---------------------------
def parse_followers(text: Optional[str]) -> Optional[int]:
    """ Convert follower strings like "12.3K", "1.2M", "1234" into integer """
    if text is None:
        return None
    text = str(text).strip()
    m = re.search(r'([\d,.]+)\s*([KkMm])?', text)
    if not m:
        digits = re.sub(r'\D', '', text)
        try:
            return int(digits) if digits else None
        except ValueError:
            return None
    num_str, suffix = m.group(1), m.group(2)
    num = float(num_str.replace(",", ""))
    if suffix:
        s = suffix.lower()
        if s == 'k':
            num *= 1_000
        elif s == 'm':
            num *= 1_000_000
    return int(round(num))

def extract_username_from_url(url: str) -> str:
    if not url:
        return ""
    m = re.search(r'x\.com\/([^\/\?\#]+)', url, re.IGNORECASE)
    return m.group(1) if m else ""

# ---------------------------
# Apify search
# ---------------------------
def run_apify_search(topic: str, apify_token: str, max_pages_per_query: int = 1) -> List[Dict]:
    """
    Calls Apify google-search-scraper run-sync API and returns dataset items list.
    The query searches site:x.com for <topic> + cardano to bias results toward Cardano-related accounts.
    """
    headers = {"Content-Type": "application/json"}
    params = {"token": apify_token}
    # Query: site:x.com <topic> cardano
    queries_field = f"site:x.com {topic} cardano"
    payload = {
        "focusOnPaidAds": False,
        "forceExactMatch": False, 
        "includeIcons": False,
        "includeUnfilteredResults": False,
        "maxPagesPerQuery": max_pages_per_query,
        "mobileResults": False,
        "queries": queries_field,
        "resultsPerPage": RESULTS_PER_REQUEST,
        "saveHtml": False,
        "saveHtmlToKeyValueStore": True,
    }

    resp = requests.post(APIFY_RUN_SYNC_URL, params=params, json=payload, headers=headers, timeout=120)
    resp.raise_for_status()
    data = resp.json()
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        if "items" in data and isinstance(data["items"], list):
            return data["items"]
    return []

def parse_apify_items(items: List[Dict]) -> List[Dict]:
    """
    Normalize Apify items into leads:
      { "Name", "Username", "Handle", "Description", "Followers", "SourceQuery" }
    """
    leads = []
    for item in items:
        json_obj = item.get("json") if isinstance(item, dict) and "json" in item else item
        organic = []
        if isinstance(json_obj, dict):
            if "organicResults" in json_obj and isinstance(json_obj["organicResults"], list):
                organic = json_obj["organicResults"]
            elif "results" in json_obj and isinstance(json_obj["results"], list):
                organic = json_obj["results"]
        if not organic:
            continue
        for r in organic:
            name = r.get("title") or ""
            url = r.get("url") or r.get("link") or ""
            username = extract_username_from_url(url)
            description = r.get("description") or r.get("snippet") or ""
            followers_raw = r.get("followersAmount") or r.get("followers") or ""
            followers = parse_followers(followers_raw)
            leads.append({
                "Name": name,
                "Username": username,
                "Handle": url,
                "Description": description,
                "Followers": followers
            })
    return leads

# ---------------------------
# Google Sheets writing
# ---------------------------
def authorize_gsheets(creds_path: str):
    """
    Authorize and return a gspread client using service account json file at creds_path.
    """
    if not os.path.exists(creds_path):
        raise FileNotFoundError(f"Service account JSON not found at: {creds_path}")
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
    client = gspread.authorize(creds)
    return client

def ensure_sheet_tab(sheet, tab_name: str):
    """
    Returns worksheet object for tab_name; creates tab if not exists.
    Ensures header row exists.
    """
    try:
        ws = sheet.worksheet(tab_name)
    except gspread.WorksheetNotFound:
        ws = sheet.add_worksheet(title=tab_name, rows="1000", cols="20")
    # Ensure header row
    headers = ["Timestamp", "Topic", "Name", "Username", "Handle", "Description", "Followers"]
    existing = ws.row_values(1)
    if not existing or existing[:len(headers)] != headers:
        ws.update("A1:G1", [headers])
    return ws

def append_leads_to_sheet(ws, topic: str, leads: List[Dict]):
    """
    Append leads rows to the worksheet. Each row:
      Timestamp, Topic, Name, Username, Handle, Description, Followers
    """
    if not leads:
        return 0
    now = datetime.utcnow().isoformat(sep=" ", timespec="seconds") + " UTC"
    rows = []
    for lead in leads:
        rows.append([
            now,
            topic,
            lead.get("Name", ""),
            lead.get("Username", ""),
            lead.get("Handle", ""),
            lead.get("Description", ""),
            str(lead.get("Followers", "") or "")
        ])
    # gspread accepts list of rows to append
    # Use append_rows for batch append
    ws.append_rows(rows, value_input_option="USER_ENTERED")
    return len(rows)

# ---------------------------
# CLI & main
# ---------------------------
def main():
    parser = argparse.ArgumentParser(description="Cardano X Leads Scraper -> Google Sheets (no web3, no wallet)")
    parser.add_argument("--topic", "-t", type=str, help="Topic / niche to search for (e.g., 'nft artists')")
    parser.add_argument("--sheet-tab", type=str, default=SHEET_TAB, help="Google Sheet tab name to store results")
    parser.add_argument("--max-pages", type=int, default=1, help="Max pages per query for Apify")
    args = parser.parse_args()

    topic = args.topic
    if not topic:
        topic = input("Enter topic/niche to search for (e.g., 'nft artists'): ").strip()
    if not topic:
        print("No topic supplied. Exiting.")
        return

    print(f"Searching X.com for Cardano-related accounts about: '{topic}'")
    # run Apify
    try:
        items = run_apify_search(topic, APIFY_TOKEN, max_pages_per_query=args.max_pages)
    except Exception as e:
        print(f"Error calling Apify: {e}")
        return

    leads = parse_apify_items(items)
    print(f"Found {len(leads)} leads (parsed).")

    # Authorize Google Sheets
    try:
        gc = authorize_gsheets(SHEET_CREDENTIALS)
        sheet = gc.open_by_key(SHEET_ID)
        ws = ensure_sheet_tab(sheet, args.sheet_tab)
    except Exception as e:
        print(f"Error authorizing or opening Google Sheet: {e}")
        return

    # Append to sheet
    try:
        appended = append_leads_to_sheet(ws, topic, leads)
        print(f"Appended {appended} rows to sheet '{args.sheet_tab}'.")
    except Exception as e:
        print(f"Error appending to sheet: {e}")
        return

    print("Done. Tip: open the Google Sheet to review and remove duplicates if needed.")

if __name__ == "__main__":
    main()
