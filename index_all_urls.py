#!/usr/bin/env python3
"""
Google Indexing API で新規URLのみインデックス登録をリクエストするスクリプト
使い方: python3 index_all_urls.py --credentials /path/to/client_secret.json
"""

import argparse
import json
import time
import xml.etree.ElementTree as ET
import requests
import os
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/indexing']
SITEMAP_URL = 'https://open-tensaku.com/sitemap-0.xml'
TOKEN_FILE = 'token.json'
SENT_URLS_FILE = 'sent_urls.json'


def get_credentials(credentials_file):
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return creds


def get_urls_from_sitemap(sitemap_url):
    response = requests.get(sitemap_url)
    response.raise_for_status()
    root = ET.fromstring(response.content)
    ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    return [loc.text for loc in root.findall('.//sm:loc', ns)]


def load_sent_urls():
    if os.path.exists(SENT_URLS_FILE):
        with open(SENT_URLS_FILE) as f:
            return json.load(f)
    return {}


def save_sent_urls(sent):
    with open(SENT_URLS_FILE, 'w') as f:
        json.dump(sent, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--credentials', required=True, help='OAuthクライアントIDのJSONファイルパス')
    parser.add_argument('--force', action='store_true', help='送信済みを無視して全URL再送信')
    args = parser.parse_args()

    all_urls = get_urls_from_sitemap(SITEMAP_URL)
    sent = load_sent_urls()

    if args.force:
        new_urls = all_urls
    else:
        new_urls = [u for u in all_urls if u not in sent]

    if not new_urls:
        print(f'新規URLなし（全{len(all_urls)}件は送信済み）。スキップします。')
        return

    print(f'新規URL: {len(new_urls)}件 / 全体: {len(all_urls)}件')

    print('認証中...')
    creds = get_credentials(args.credentials)
    service = build('indexing', 'v3', credentials=creds)

    success, failed = 0, 0
    for i, url in enumerate(new_urls, 1):
        try:
            service.urlNotifications().publish(body={'url': url, 'type': 'URL_UPDATED'}).execute()
            print(f'[{i}/{len(new_urls)}] ✓ {url}')
            sent[url] = datetime.now().isoformat()
            success += 1
        except Exception as e:
            print(f'[{i}/{len(new_urls)}] ✗ {url} - {e}')
            failed += 1
        time.sleep(0.5)

    save_sent_urls(sent)
    print(f'\n完了: 成功 {success}件 / 失敗 {failed}件')


if __name__ == '__main__':
    main()
