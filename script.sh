#!/bin/bash

echo "Starting scraping..."
python scripts/scrape.py

if [ $? -eq 0 ]; then
  echo "Scraping successful! Filtering data..."
  python scripts/filter.py
else
  echo "Scraping failed. Filtering not run."
fi
