import os
import csv
from bs4 import BeautifulSoup

def find_html_files(directory):
    matches = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html') or '.html' in file:
                matches.append(os.path.join(root, file))
    return matches

def extract_canonical_url(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        link_tag = soup.find('link', {'rel': 'canonical'})
        if link_tag and 'href' in link_tag.attrs:
            return link_tag['href']
    return None

def create_csv(mapping, output_csv):
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['File Name', 'Canonical URL']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for file_name, canonical_url in mapping.items():
            writer.writerow({'File Name': file_name, 'Canonical URL': canonical_url})

def main(directory, output_csv):
    files = find_html_files(directory)
    
    mapping = {}
    for file_path in files:
        canonical_url = extract_canonical_url(file_path)
        if canonical_url:
            mapping[file_path] = canonical_url

    create_csv(mapping, output_csv)

if __name__ == "__main__":
    directory = '../'  # Replace with the path to your directory
    output_csv = 'output.csv'  # Replace with the desired output CSV file name
    main(directory, output_csv)
