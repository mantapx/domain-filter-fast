import os
import re
from collections import defaultdict

def normalize_domain(line):
    line = line.strip().lower()
    if not line:
        return None
    line = re.sub(r'^https?://', '', line)
    line = line.split('/')[0]
    return line if '.' in line else None

def extract_full_extension(domain):
    parts = domain.split('.')
    if len(parts) < 2:
        return 'unknown'
    
    # Cek kombinasi 2-3 level seperti co.id, go.id, ac.uk, dll
    common_multi = {"co.id", "go.id", "ac.id", "or.id", "sch.id", "co.uk", "ac.uk", "gov.uk"}
    last_two = ".".join(parts[-2:])
    last_three = ".".join(parts[-3:])

    if last_three in common_multi:
        return last_three
    elif last_two in common_multi:
        return last_two
    else:
        return parts[-1]

def split_domains_bigfile(input_file, output_dir='hasil'):
    os.makedirs(output_dir, exist_ok=True)
    writers = defaultdict(lambda: None)

    try:
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as infile:
            for i, line in enumerate(infile, 1):
                domain = normalize_domain(line)
                if not domain:
                    continue
                ext = extract_full_extension(domain)
                filename = f"{ext}.txt"
                output_path = os.path.join(output_dir, filename)

                if writers[ext] is None:
                    writers[ext] = open(output_path, 'a', encoding='utf-8')

                writers[ext].write(domain + '\n')

                if i % 100000 == 0:
                    print(f"[INFO] Processed {i:,} lines...")

        print("\n✓ Selesai! Domain dipisahkan di folder:", output_dir)

    finally:
        for f in writers.values():
            if f:
                f.close()

if __name__ == "__main__":
    input_file = input("Masukkan file berisi daftar domain (contoh: weblist.txt): ").strip()
    if not os.path.isfile(input_file):
        print(f"⚠️ File '{input_file}' tidak ditemukan.")
    else:
        split_domains_bigfile(input_file)
