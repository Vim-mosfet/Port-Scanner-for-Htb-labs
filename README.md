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
python Automatisation_scanNmap.py <IP> --ports <ports>
```
**Exemple**

```bash
python Automatisation_scanNmap.py 192.1.1.1 # Scan all ports without saving output 
python Automatisation_scanNmap.py 192.1.1.1 --ports 80,443,22 # Scan specificports without saving output 
python Automatisation_scanNmap.py 192.1.1.1 --ports 22,80 --output EXEMPLE.txt # Scan sspecific ports with saving output

```
**Script**

```
import argparse
import nmap

def scan_ports(target, ports='all', output_file=None):
    nm = nmap.PortScanner()

    try:
        print(f"Scan en cours sur {target}...")

        if ports == 'all':
            nm.scan(hosts=target, ports='1-65535', arguments='-T4')

            for host in nm.all_hosts():
                for proto in nm[host].all_protocols():
                    for port in nm[host][proto]:
                        if nm[host][proto][port]['state'] == 'open':
                            result = f"Port {port}: Ouvert - {nm[host][proto][port]['name']}\n"
                            print(result.strip())

                            if output_file:
                                with open(output_file, "a") as f:
                                    f.write(result)

        else:
            port_list = [int(p) for p in ports.split(',')]
            port_str = ','.join(str(p) for p in port_list)

            nm.scan(hosts=target, ports=port_str, arguments='-T4')

            for host in nm.all_hosts():
                for proto in nm[host].all_protocols():
                    for port in nm[host][proto]:
                        if nm[host][proto][port]['state'] == 'open':
                            result = f"Port {port}: Ouvert - {nm[host][proto][port]['name']}\n"
                            print(result.strip())

                            if output_file:
                                with open(output_file, "a") as f:
                                    f.write(result)

    except Exception as e:
        print(f"Erreur : {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scanner les ports d'une IP.")
    parser.add_argument("target", help="IP ou hostname")
    parser.add_argument("--ports", help="Ports ex: 80,443")
    parser.add_argument("--output", help="Fichier de sortie")

    args = parser.parse_args()

    ports = args.ports if args.ports else 'all'
    output_file = args.output

    if output_file:
        with open(output_file, "w") as f:
            f.write("Scan en cours...\n")

    scan_ports(args.target, ports, output_file)

```



