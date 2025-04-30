import socket
import os
import time
import random

def resolve_domains(input_file, output_file):
    ips = []
    seen = set()
    batch_size = 250

    # Charger les IP existantes
    if os.path.isfile(output_file):
        with open(output_file, 'r') as f:
            for line in f:
                ip = line.strip()
                if ip and ip not in seen:
                    seen.add(ip)
                    ips.append(ip)

    # Lire tous les domaines
    with open(input_file, 'r') as f:
        all_domains = [line.strip() for line in f if line.strip()]
    
    total = len(all_domains)
    processed = 0

    # Traiter par lots de 250
    while processed < total:
        batch = all_domains[processed:processed+batch_size]
        print(f"Traitement des domaines {processed+1}-{min(processed+batch_size, total)}/{total}")

        for domain in batch:
            try:
                results = socket.getaddrinfo(domain, None, socket.AF_INET)
                for res in results:
                    ip = res[4][0]
                    if ip not in seen:
                        seen.add(ip)
                        ips.append(ip)
            except socket.gaierror:
                print(f"Domaine non résolu : {domain}")
            except Exception as e:
                print(f"Erreur avec {domain} : {e}")
        
        processed += len(batch)
        
        if processed < total:
            delay = random.randint(10, 20)
            print(f"Pause aléatoire de {delay} secondes avant le prochain lot...")
            time.sleep(delay)

    # Vérification finale des doublons
    unique_count = len(ips)
    ips = list(dict.fromkeys(ips))  # Suppression des doublons tout en conservant l'ordre
    duplicates_removed = unique_count - len(ips)
    
    if duplicates_removed > 0:
        print(f"Vérification finale : {duplicates_removed} doublons supprimés")

    # Écrire le fichier final
    with open(output_file, 'w') as f:
        for ip in ips:
            f.write(ip + '\n')

    print(f"Nombre total d'adresses IP uniques : {len(ips)}")

if __name__ == "__main__":
    resolve_domains("domains.txt", "ip-list.txt")
    print("Résolution terminée. Résultats dans ip-list.txt")
