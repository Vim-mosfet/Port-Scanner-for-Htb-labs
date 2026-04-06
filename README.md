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

**Installation:**

1.  Clone the repository: git clone [URL of your repository]
2.  Navigate to the project directory: cd [project folder name]
3.  Install dependencies (if any): pip install -r requirements.txt (If you have a requirements.txt file)

**Usage:**

bash
python scanner_ports.py -n <IP address> -p <port range>
