import os
import re
from collections import defaultdict

def normalize_domain(line):
    """
    Ambil hanya domain utama, hilangkan http/https/path/port
    """
    line = line.strip().lower()
    if not line:
        return None
    line = re.sub(r'^https?://', '', line)
    domain = line.split('/')[0].split(':')[0]
    return domain if '.' in domain else None

def extract_full_extension(domain):
    """
    Ambil ekstensi akhir: go.id, co.id, org, com, dll
    """
    parts = domain.split('.')
    if len(parts) < 2:
        return 'unknown'
    multi_ext = {"co.id", "go.id", "ac.id", "or.id", "sch.id", "co.uk", "ac.uk", "gov.uk"}
    last_three = ".".join(parts[-3:])
    last_two = ".".join(parts[-2:])
    if last_three in multi_ext:
        return last_three
    elif last_two in multi_ext:
        return last_two
    return parts[-1]

def split_domains_cpu_friendly(input_file, output_dir='hasil'):
    os.makedirs(output_dir, exist_ok=True)
    file_handles = {}

    try:
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f, 1):
                domain = normalize_domain(line)
                if not domain:
                    continue
                ext = extract_full_extension(domain)
                output_path = os.path.join(output_dir, f"{ext}.txt")

                if ext not in file_handles:
                    file_handles[ext] = open(output_path, 'a', encoding='utf-8')

                file_handles[ext].write(domain + '\n')

                if i % 500000 == 0:
                    print(f"[INFO] Diproses {i:,} baris...")

        print(f"\n✓ Selesai. Semua hasil tersimpan di folder: '{output_dir}'")

    finally:
        for f in file_handles.values():
            f.close()

if __name__ == "__main__":
    input_file = input("Masukkan nama file list domain (contoh: input.txt): ").strip()
    if not os.path.isfile(input_file):
        print(f"⚠️ File '{input_file}' tidak ditemukan.")
    else:
        split_domains_cpu_friendly(input_file)
