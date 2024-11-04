"""Backfill database."""
import json
import requests

with open('corpora/documents.json', encoding='utf-8') as f:
    documents = json.load(f)

for document in documents:
    response = requests.post(
        'http://localhost:3050/document/create',
        json={'content': document},
        timeout=30
        )

    response.raise_for_status()
