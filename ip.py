import socket
import concurrent.futures

def resolve_domain(domain):
    domain = domain.strip()
    if not domain:
        return None
    try:
        ip = socket.gethostbyname(domain)
        return f"{domain} -> {ip}"
    except socket.gaierror:
        return f"{domain} -> Gagal resolve"

def main():
    input_file = input("Masukkan file web (contoh: web.txt): ").strip()

    try:
        with open(input_file, 'r') as file:
            domains = list(set([line.strip() for line in file if line.strip()]))  # hapus kosong dan duplikat
    except FileNotFoundError:
        print("File tidak ditemukan.")
        return

    print(f"Resolving {len(domains)} domain...\n")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(resolve_domain, domains))

    with open("ips.txt", "w") as output:
        for line in results:
            if "->" in line and "Gagal" not in line:
                output.write(line.split("->")[1].strip() + "\n")  # hanya IP

    print(f"\nSelesai. Hasil berhasil disimpan ke 'ips.txt'.")

if __name__ == "__main__":
    main()
