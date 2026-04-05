import subprocess
import sys
import socket

# -------------------------------
# AUTO INSTALL MODULES
# -------------------------------
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_and_install():
    try:
        import requests
    except ImportError:
        print("[+] Installing required module: requests")
        install("requests")

check_and_install()

import requests


# -------------------------------
# BANNER
# -------------------------------
def show_banner():
    banner = r"""
██████╗ ██╗  ██╗ █████╗ ███╗   ██╗████████╗ ██████╗ ███╗   ███╗
██╔══██╗██║  ██║██╔══██╗████╗  ██║╚══██╔══╝██╔═══██╗████╗ ████║
██████╔╝███████║███████║██╔██╗ ██║   ██║   ██║   ██║██╔████╔██║
██╔═══╝ ██╔══██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╔╝██║
██║     ██║  ██║██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚═╝ ██║
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝

            PHANTOMSCAN 👻
"""
    print(banner)


# -------------------------------
# CLEAN TARGET
# -------------------------------
def clean_target(target):
    target = target.replace("http://", "")
    target = target.replace("https://", "")
    target = target.replace("www.", "")
    return target.strip()


# -------------------------------
# VALIDATE TARGET
# -------------------------------
def validate_target(target):
    try:
        socket.gethostbyname(target)
        return True
    except:
        return False


# -------------------------------
# IP RESOLVER
# -------------------------------
def get_ip(target):
    print("\n[+] Resolving IP Address...")
    try:
        ip = socket.gethostbyname(target)
        print(f"[IP] {target} -> {ip}")
        return ip
    except:
        print("[-] Unable to resolve IP")
        return "N/A"


# -------------------------------
# SUBDOMAIN FINDER (LIVE PROGRESS)
# -------------------------------
def find_subdomains(domain):
    print("\n[+] Finding Subdomains...")

    wordlist = [
        "www","mail","webmail","smtp","secure","server","ns1","ns2",
        "dev","test","staging","beta","alpha",
        "admin","administrator","portal","dashboard","panel","cpanel",
        "api","api1","api2","api-dev","api-test",
        "app","apps","mobile","m","web",
        "blog","news","shop","store","payment","checkout",
        "login","signin","auth","account",
        "cdn","static","media","images","img","assets",
        "files","uploads","download","downloads",
        "ftp","ssh","vpn","remote",
        "db","database","sql","mysql","postgres",
        "internal","intranet","private","corp",
        "support","help","ticket","crm",
        "devops","jenkins","git","gitlab","github",
        "monitor","status","health",
        "mail2","mail1","mx","mx1","mx2"
    ]

    found = []

    for i, sub in enumerate(wordlist, 1):
        url = f"http://{sub}.{domain}"

        # SAME LINE PROGRESS
        print(f"\r[{i}/{len(wordlist)}] Checking: {url}", end="")

        try:
            requests.get(url, timeout=2)
            print(f"\n[FOUND] {url}")
            found.append(url)
        except:
            pass

    print()
    return found


# -------------------------------
# PORT SCANNER (FILE + SERVICE)
# -------------------------------
def scan_ports(target):
    print("\n[+] Scanning Ports (File Only Mode)...")
    open_ports = []

    try:
        with open("ports.txt", "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("[-] ports.txt not found!")
        return open_ports

    for line in lines:
        parts = line.strip().split()
        if len(parts) == 0:
            continue

        try:
            port = int(parts[0])
            service = parts[1] if len(parts) > 1 else "Unknown"
        except:
            continue

        try:
            s = socket.socket()
            s.settimeout(1)

            if s.connect_ex((target, port)) == 0:
                print(f"[OPEN] Port {port} ({service})")
                open_ports.append(f"{port} ({service})")

            s.close()
        except:
            pass

    return open_ports


# -------------------------------
# TECH DETECTION
# -------------------------------
def detect_tech(target):
    print("\n[+] Detecting Technologies...")
    tech = {}
    detected = []

    try:
        res = requests.get(f"http://{target}", timeout=5)
        headers = res.headers
        content = res.text.lower()

        tech["Server"] = headers.get("Server")
        tech["X-Powered-By"] = headers.get("X-Powered-By")

        print(f"Server: {tech['Server']}")
        print(f"X-Powered-By: {tech['X-Powered-By']}")

        tech_signatures = {
            "WordPress": ["wp-content", "wp-includes"],
            "Laravel": ["laravel_session"],
            "React": ["react", "_next"],
            "Angular": ["ng-version"],
            "Vue": ["vue"],
            "PHP": ["php"],
            "Cloudflare": ["cloudflare"],
            "jQuery": ["jquery"],
            "Bootstrap": ["bootstrap"]
        }

        for t, signs in tech_signatures.items():
            for sign in signs:
                if sign in content:
                    print(f"[DETECTED] {t}")
                    detected.append(t)
                    break

        tech["Detected"] = detected

    except:
        print("[-] Failed to detect tech")

    return tech


# -------------------------------
# DIRECTORY BRUTEFORCE
# -------------------------------
def dir_bruteforce(target):
    print("\n[+] Bruteforcing Directories...")
    found = []

    try:
        with open("dirs.txt", "r") as f:
            paths = f.read().splitlines()

        for path in paths:
            url = f"http://{target}/{path}"

            try:
                res = requests.get(url, timeout=3)

                if res.status_code == 200:
                    print(f"[FOUND] {url}")
                    found.append(url)

            except:
                pass

    except FileNotFoundError:
        print("[-] dirs.txt not found!")

    return found


# -------------------------------
# REPORT
# -------------------------------
def generate_report(target, ip, subs, ports, tech, dirs):
    print("\n[+] Generating Report...")

    filename = f"{target}_report.txt"

    with open(filename, "w") as f:
        f.write(f"Target: {target}\n")
        f.write(f"IP Address: {ip}\n\n")

        f.write("Subdomains:\n")
        for s in subs:
            f.write(s + "\n")

        f.write("\nOpen Ports:\n")
        for p in ports:
            f.write(p + "\n")

        f.write("\nTechnologies:\n")
        f.write(str(tech) + "\n")

        f.write("\nDirectories:\n")
        for d in dirs:
            f.write(d + "\n")

    print(f"[+] Report saved as {filename}")


# -------------------------------
# MAIN
# -------------------------------
def main():
    show_banner()

    target = input("Enter target (example.com): ")
    target = clean_target(target)

    if not validate_target(target):
        print("\n[-] Invalid domain or website not reachable!")
        return

    ip = get_ip(target)
    subs = find_subdomains(target)
    ports = scan_ports(target)
    tech = detect_tech(target)
    dirs = dir_bruteforce(target)

    generate_report(target, ip, subs, ports, tech, dirs)


# -------------------------------
# RUN
# -------------------------------
if __name__ == "__main__":
    main()
