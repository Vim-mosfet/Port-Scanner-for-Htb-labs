# Port-Scanner-for-Htb-labs
TCP port scanner project in Python, illustrating fundamental networking, socket handling, and open/closed port detection.  I utilized AI assistance in the initial code structure. More information and usage instructions can be found in the README.md file.

## README.md - English
# TCP Port Scanner in Python

This project presents a TCP port scanner written in Python, designed to illustrate fundamental networking and socket concepts. It enables you to:

*   Scan all or a specified range of ports on a given IP address.
*   Identify the status (open or closed) of each port.
*   Log results to a file.
*   Displays a progress bar to track scan progress.

**Technologies Used:**

*   Python 3.x
*   Socket Programming

**Prerequisites:**

*   Python 3.x installed on your system.

**Usage:**

```bash
python scanner_ports.py -n <IP address> -p <port range>
```

**Script**
```
import argparse
import nmap  # On importe la bibliothèque python-nmap pour interagir avec Nmap.
from tqdm import tqdm  # On importe tqdm pour afficher une barre de progression pendant le scan (optionnel, mais utile pour les scans longs).
from time import sleep  # On importe sleep pour ajouter des pauses entre les scans (optionnel, mais peut aider à éviter d'être détecté comme un scan agressif).
from datetime import datetime  # On importe datetime pour enregistrer les timestamps des scans (optionnel, mais utile pour les rapports).

def is_valid_port(port):
    """Vérifie si un port est valide (entre 1 et 65535)."""
    return 1 <= port <= 65535         

def scan_ports(target, ports='all', output_file=None):
    """
    Scanne les ports d'une IP en utilisant Nmap et affiche les résultats.

    Args:
        target (str): IP ou Hostname cible.
        ports (str): Série de numéros séparés par des virgules (importants) des ports à scanner. 
                     Si argument est 'all', tous les ports sont scannés. 
                     Par défaut : 'all'.
        output_file (str): Nom du fichier de sortie pour enregistrer les résultats.
   """
    
    nm = nmap.PortScanner(host=target, options='-T4')  # Initialise le PortScanner, l'objet principal pour interagir avec Nmap et on ajoute l'option '-T4' pour accélérer le scan (plus rapide que le mode par défaut).

    try:
        print(f"Scan en cours sur {target}...") # On affiche le message qui indique que le scan est en cours.

        if ports == 'all':
            # Scanne tous les ports
            nm.scan(target, '1-65535')  # Effectue le scan de tous les ports TCP
            for port in range(1, 65536):  # Boucle de 1 à 65535 pour scanner tous les ports (Max port tpc/udp).
                try:
                    state = nm[target]['tcp'][port]['state']  # Récuperation de l'état du port (ouvert, fermé, filtré).
                    if state == 'open': # On affiche seulement les ports ouverts
                        result = f"Port {port}: Ouvert - {nm[target]['tcp'][port]['name']}\n"
                        print(result.strip()) # On affiche plus d'infos sur le service relatif au port ouvert.
                        if output_file:
                            with open(output_file, "a") as f:
                                f.write(result)

                except KeyError:
                    pass  # Port fermé / non trouvé, on skip et on passe au port suivant.
                except Exception as e:
                    print(f"Erreur lors du traitement du port {port}: {e}") # Si on obtient une erreur, affiche un message.

        else: # Si on indique des ports spécifique à scanner (au lieu de 'all'), on les traites comme une liste d'entiers.
            port_list = [int(p) for p in ports.split(',')] # On convertit la chaîne de ports indiqués et séparés par des virgules en une liste d'entiers.
            port_str = ','.join(str(p) for p in port_list)
            nm.scan(target, port_str)  # Effectue le scan des ports spécifiés
            for port in port_list:
                try:
                    state = nm[target]['tcp'][port]['state']  # Récuperation de l'état du port (ouvert, fermé, filtré).
                    if state == 'open':  # On affiche seulement les ports ouverts
                        result = f"Port {port}: Ouvert - {nm[target]['tcp'][port]['name']}\n"
                        print(result.strip()) # On affiche plus d'infos sur le service relatif au port ouvert.
                        if output_file:
                            with open(output_file, "a") as f:
                                f.write(result)

                except KeyError:
                    pass  # Port fermé / non trouvé, on skip et on passe au port suivant.
                except Exception as e:
                    print(f"Erreur lors du traitement du port {port}: {e}") # Si on obtient une erreur, affiche un message.

    except nmap.PortScannerError as e:
        print(f"Erreur Nmap : {e}")  # Affiche les erreurs spécifiques à Nmap
    except Exception as e:
        print(f"Une erreur s'est produite : {e}") # Si on obtient une erreur générale, affiche un message.



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scanner les ports d'une adresse IP (tous ou spécifiés).") # Crée un objet ArgumentParser pour gérer les arguments de la ligne de commande
    parser.add_argument("target", help="L'adresse IP ou le nom d'hôte de la cible.")  # Définit l'argument obligatoire "target"
    parser.add_argument("--ports", help="Une chaîne séparée par des virgules contenant les numéros de port à scanner (par défaut: tous).") # Définit l'argument optionnel "--ports"
    parser.add_argument("--output", help="Nom du fichier de sortie pour enregistrer les résultats.")  # Définit l'argument optionnel "--output"

    args = parser.parse_args() # Analyse les arguments passés en ligne de commande
    output_file = args.output
    if output_file is None:
        output_file = input("Entrez le nom du fichier de sortie : ")
    if output_file:
        try:
            with open(output_file, "w") as f:  # Ouvre le fichier en mode écriture ("w") pour créer ou écraser le fichier de sortie
                f.write("Scan en cours...\n") # Ajout d'un message indiquant que le scan est en cours
            print(f"Les résultats seront écrits dans {output_file}")
        except Exception as e:
            print(f"Erreur lors de l'ouverture du fichier : {e}")
    scan_ports(args.target, args.ports, output_file)  # Appelle la fonction pour effectuer le scan avec les arguments fournis

```



