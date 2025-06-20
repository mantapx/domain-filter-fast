import socket
import concurrent.futures
from tqdm import tqdm
from colorama import Fore, Style, init

# Inisialisasi colorama
init(autoreset=True)

def resolve_domain(domain):
    domain = domain.strip()
    if not domain:
        return None
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except socket.gaierror:
        return None

def main():
    input_file = input(f"{Fore.CYAN}Masukkan file web (contoh: web.txt): {Style.RESET_ALL}").strip()

    try:
        with open(input_file, 'r') as file:
            domains = list(set([line.strip() for line in file if line.strip()]))  # bersihkan dan unik
    except FileNotFoundError:
        print(f"{Fore.RED}❌ File tidak ditemukan.{Style.RESET_ALL}")
        return

    print(f"\n{Fore.GREEN}🔄 Resolving {len(domains)} domain...\n{Style.RESET_ALL}")

    with open("ips.txt", "w") as output_file:
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            futures = {executor.submit(resolve_domain, domain): domain for domain in domains}

            for future in tqdm(concurrent.futures.as_completed(futures), total=len(domains),
                               desc=Fore.GREEN + "Resolving" + Style.RESET_ALL, ncols=100):
                ip = future.result()
                if ip:
                    output_file.write(ip + "\n")

    print(f"\n{Fore.GREEN}✅ Selesai! Semua IP berhasil disimpan ke 'ips.txt'.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
