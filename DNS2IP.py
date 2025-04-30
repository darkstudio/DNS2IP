import socket
import os
import time
import random
import re

def extract_domain(line):
    """
    Extrait le nom de domaine effectif d'une ligne.
    - Ignore les lignes vides et les commentaires.
    - Si la ligne commence par une IP et un espace, retourne le domaine.
    - Sinon, retourne la ligne telle quelle si c'est un domaine.
    - Retourne None si la ligne ne contient pas de domaine.
    """
    line = line.strip()
    if not line or line.startswith('#'):
        return None
    # Format "0.0.0.0 domain.com"
    match = re.match(r'^(?:\d{1,3}\.){3}\d{1,3}\s+([^\s#]+)', line)
    if match:
        return match.group(1)
    # Format "domain.com"
    if re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', line):
        return line
    return None

def resolve_domains(input_file, output_file):
    # Vérifier si le fichier domains.txt existe
    if not os.path.isfile(input_file):
        print(f"Le fichier '{input_file}' n'existe pas.")
        print(f"Création du fichier '{input_file}' à la racine du projet...")
        with open(input_file, 'w') as f:
            f.write("# Exemple de liste de domaines à remplir, un domaine par ligne :\n")
            f.write("google.be\n")
            f.write("google.com\n")
        print(f"Veuillez remplir '{input_file}' avec vos domaines, puis relancez le script.")
        time.sleep(10)
        return

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

    # Lire et extraire les domaines effectifs
    with open(input_file, 'r') as f:
        all_domains = []
        for line in f:
            domain = extract_domain(line)
            if domain:
                all_domains.append(domain)

    if not all_domains:
        print(f"Aucun domaine valide trouvé dans '{input_file}'. Veuillez le remplir avec des noms de domaines valides (ex : google.com).")
        time.sleep(10)
        return

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
    print("Résolution terminée. Résultats dans ip-list.txt")
    print("DNS2IP va se fermer dans 10 secondes...")
    time.sleep(10)

if __name__ == "__main__":
    resolve_domains("domains.txt", "ip-list.txt")
