import subprocess
import csv


domains = ["google.com", "github.com", "apple.com", "yandex.ru", "soundcloud.com"]
output_file = "lab10_results.csv"

with open(output_file, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Домен", "IP-адрес", "Результат traceroute"])

    for domain in domains:
        print(f"Проверяем: {domain}")

        dns = subprocess.run(["dig", "+short", domain], capture_output=True, text=True)
        ips = dns.stdout.strip().splitlines()

        if not ips:
            print("  DNS не ответил")
            writer.writerow([domain, "N/A", "DNS failed"])
            continue

        ip = ips[0]
        print(f"  IP: {ip}")

        trace = subprocess.run(["traceroute", "-m", "10", "-w", "2", ip], capture_output=True, text=True)
        trace_text = trace.stdout.strip().replace("\n", " | ")
        print("  Traceroute завершён")

        writer.writerow([domain, ip, trace_text])

print(f"\nГотово! Результаты сохранены в: {output_file}")