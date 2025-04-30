
# DNS2IP

Un programme simple et efficace pour résoudre des noms de domaine en adresses IP.

## Description

Ce programme lit une liste de noms de domaine à partir d'un fichier texte et résout chacun d'eux en adresses IP correspondantes. Les résultats sont enregistrés dans un fichier de sortie. Le script est conçu pour être robuste, avec une gestion des erreurs et un traitement par lots pour éviter de surcharger les serveurs DNS.

## Fonctionnalités

- Résolution de noms de domaine en adresses IP
- Traitement par lots (250 domaines à la fois)
- Pauses aléatoires entre les lots pour éviter les limitations
- Élimination des doublons dans les résultats
- Reprise du traitement (conservation des IP déjà résolues)
- Gestion d'erreurs pour les domaines non résolus

## Prérequis

- Python 3.x
- Modules standards Python (aucune installation supplémentaire requise)

## Installation

Clonez ce dépôt ou téléchargez le fichier source :

```bash
git clone https://github.com/votre-utilisateur/dns-resolver.git
cd dns-resolver
```

## Configuration

1. Créez un fichier `domains.txt` contenant les noms de domaine à résoudre, un par ligne :

```
example.com
google.com
github.com
...
```

Format standard "hosts" supporté :

```
# mon commentaire
0.0.0.0 example.com
0.0.0.0 google.com
0.0.0.0 github.com
...
```

2. Assurez-vous que le fichier a les permissions appropriées pour être lu par le script.

## Utilisation

Exécutez le script avec la commande :

```bash
python dns2ip.py
```

Par défaut, le script :
- Lit les domaines depuis `domains.txt`
- Écrit les résultats dans `ip-list.txt`

## Paramètres ajustables

Le script contient plusieurs paramètres que vous pouvez ajuster en fonction de vos besoins :

- `batch_size` : Nombre de domaines traités dans chaque lot (défaut: 250)
- Délai entre les lots : Actuellement configuré pour une pause aléatoire de 10 à 20 secondes
  ```python
  delay = random.randint(10, 20)
  ```

## Limites et considérations

- Le script effectue uniquement des résolutions IPv4 (socket.AF_INET)
- N'essaie pas de résoudre à nouveau les domaines qui ont échoué
- Utilise des pauses aléatoires pour éviter les limitations des serveurs DNS

## Structure de sortie

Le fichier de sortie `ip-list.txt` contiendra une liste d'adresses IP uniques, une par ligne :

```
192.0.2.1
192.0.2.2
198.51.100.1
...
```

## Licence

MIT License

## Executable

Pour plus de facilité, vous pouvez utiliser directement la version compilée en EXE dans les Release.
