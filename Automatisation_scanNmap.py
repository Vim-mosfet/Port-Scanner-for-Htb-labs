import argparse
import nmap # On importe la bibliothèque python-nmap pour interagir avec Nmap.

def scan_ports(target, ports='all', output_file=None): # On définit une fonction scan_ports qui prend en paramètres l'IP cible, les ports à scanner (par défaut 'all' pour tous les ports) et un fichier de sortie optionnel pour enregistrer les résultats.
    """
    Scanne les ports d'une IP en utilisant Nmap et affiche les résultats.

    Args:
        target (str): IP ou Hostname cible.
        ports (str): Série de numéros séparés par des virgules (importants) des ports à scanner. 
                     Si argument est 'all', tous les ports sont scannés. 
                     Par défaut : 'all'.
        output_file (str): Nom du fichier de sortie pour enregistrer les résultats.
    """
    nm = nmap.PortScanner() # Initialise le PortScanner, l'objet principal pour interagir avec Nmap

    try:
        print(f"Scan en cours sur {target}...") # On affiche le message qui indique que le scan est en cours.

        if ports == 'all': # Si on ne donne pas de ports spécifiques on active le scan de tous les ports (1-65535).
            nm.scan(hosts=target, ports='1-65535', arguments='-T4')  # Effectue le scan de tous les ports TCP avec une vitesse de scan rapide (-T4).

            for host in nm.all_hosts(): # Parcourt tous les hôtes trouvés par le scan (généralement il n'y en aura qu'un, celui ciblé).
                for proto in nm[host].all_protocols(): # Parcourt tous les protocoles détectés pour cet hôte (généralement TCP, mais peut aussi être UDP).
                    for port in nm[host][proto]: # Parcourt tous les ports détectés pour ce protocole.
                        if nm[host][proto][port]['state'] == 'open': # Vérifie si le port est ouvert.
                            result = f"Port {port}: Ouvert - {nm[host][proto][port]['name']}\n" # Formate le résultat pour indiquer le port, son état (ouvert) et le nom du service associé.
                            print(result.strip()) # Affiche le résultat à la console, en supprimant les espaces superflus.

                            if output_file:
                                with open(output_file, "a") as f:
                                    f.write(result)

        else:
            port_list = [int(p) for p in ports.split(',')] # Si des ports spécifiques sont fournis, on les convertit en une liste d'entiers à partir de la chaîne de caractères fournie (ex: "80,443" devient [80, 443]).
            port_str = ','.join(str(p) for p in port_list) # On reconvertit la liste de ports en une chaîne de caractères formatée pour Nmap (ex: [80, 443] devient "80,443").

            nm.scan(hosts=target, ports=port_str, arguments='-T4') # Effectue le scan des ports spécifiés avec une vitesse de scan rapide (-T4).

            for host in nm.all_hosts(): # Parcourt tous les hôtes trouvés par le scan (généralement il n'y en aura qu'un, celui ciblé).
                for proto in nm[host].all_protocols(): # Parcourt tous les protocoles détectés pour cet hôte (généralement TCP, mais peut aussi être UDP).
                    for port in nm[host][proto]: # Parcourt tous les ports détectés pour ce protocole.
                        if nm[host][proto][port]['state'] == 'open': # Vérifie si le port est ouvert.
                            result = f"Port {port}: Ouvert - {nm[host][proto][port]['name']}\n" # Formate le résultat pour indiquer le port, son état (ouvert) et le nom du service associé.
                            print(result.strip()) # Affiche le résultat à la console, en supprimant les espaces superflus.

                            if output_file: 
                                with open(output_file, "a") as f: 
                                    f.write(result)

    except Exception as e:
        print(f"Erreur : {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scanner les ports d'une IP.") # On crée un objet ArgumentParser pour gérer les arguments de la ligne de commande, avec une description du programme.
    parser.add_argument("target", help="IP ou hostname") # On ajoute un argument obligatoire "target" pour spécifier l'IP ou le hostname à scanner.
    parser.add_argument("--ports", help="Ports ex: 80,443") # On ajoute un argument optionnel "--ports" pour spécifier les ports à scanner, avec un exemple de format (ex: "80,443"). Si cet argument n'est pas fourni, le programme scannera tous les ports.
    parser.add_argument("--output", help="Fichier de sortie") # On ajoute un argument optionnel "--output" pour spécifier un fichier de sortie où les résultats du scan seront enregistrés. Si cet argument n'est pas fourni, les résultats seront affichés uniquement à la console.

    args = parser.parse_args() # On utilise argparse pour gérer les arguments de la ligne de commande. L'utilisateur doit fournir une cible (IP ou hostname), et peut optionnellement spécifier des ports à scanner et un fichier de sortie pour enregistrer les résultats.

    ports = args.ports if args.ports else 'all'
    output_file = args.output

    if output_file:
        with open(output_file, "w") as f: # Si un fichier de sortie est spécifié, on l'ouvre en mode écriture pour créer ou écraser le fichier existant, et on écrit un message initial indiquant que le scan est en cours.
            f.write("Scan en cours...\n") # On écrit un message initial dans le fichier de sortie pour indiquer que le scan est en cours.

    scan_ports(args.target, ports, output_file) # On appelle la fonction scan_ports avec les arguments fournis par l'utilisateur (IP cible, ports à scanner et fichier de sortie).
