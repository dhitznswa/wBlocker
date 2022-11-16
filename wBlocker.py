try:
    import http.client as httplib
    import os
    import platform
    import sys
    import time
    from datetime import date
    from threading import Thread

    import requests
    from dotenv import dotenv_values
    from rich.console import Console
except ImportError:
    print('\nERROR: Module Not Found !!')
    print('[~] There are some modules that are not installed yet. Type "pip install -r request.txt" in the terminal with the path where your folder saves this tool\n')
    exit()

env = dotenv_values(".env")

if platform.system() == "Windows":
    hosts_path = "C:\Windows\System32\drivers\etc\hosts"
    clearT = "cls"
else:
    hosts_path = "/etc/hosts"
    clearT = "clear"

if env.get("MODE") == "development":
    hosts_path = 'hosts'

version_path = os.path.join('core', 'version.txt')
default_hosts = os.path.join('core', 'default-hosts.txt')


class wBlocker():
    def __init__(self):
        self._path = hosts_path
        self.ipder = "127.0.0.1"
        self.exit = False
        self.today = date.today().strftime("%d/%m/%Y")
        self.console = Console()

        try:
            self._sites = open('sites.txt', 'r')
        except FileNotFoundError:
            self.console.print(
                '\n[bold red]FAILED :[/bold red] Website list file not found !!\n')
            exit()

        try:
            self._hosts = open(hosts_path, 'a')
        except FileNotFoundError:
            self.console.print(
                '\n[bold red]FAILED :[/bold red] Your operating system is not supported\n')
            exit()

    def cnet(self):
        try:
            requests.get("https://www.google.com/", timeout=5)
            return True
        except:
            return False

    def update_wb(self):
        if not os.path.isfile(version_path):
            self.console.print(
                '\n[bold red]WARNING :[/bold red] Please re-clone the script to fix this problem\n')
            exit()
        self.console.print(
            "[bold blue][~] Checking for update... [/bold blue]")
        conn = httplib.HTTPSConnection("raw.githubusercontent.com")
        conn.request("GET", "/dhitznswa/wBlocker/main/core/version.txt")
        vrepo = conn.getresponse().read().strip().decode()
        with open(version_path) as vpath:
            verPath = vpath.read().strip()
        if vrepo == verPath:
            self.console.print(
                "[bold green][*] wBlocker is up to date!! [/bold green]\n")
            conn.close()
            exit()
        else:
            self.console.print(
                "[bold blue][+] An update has been found, Updating... [/bold blue]\n")
            conn.request("GET", "/dhitznswa/wBlocker/main/wBlocker.py")
            newCode = conn.getresponse().read().strip().decode()
            with open("wBlocker.py", "w") as wb:
                wb.write(newCode)
            with open(version_path, "w") as vp:
                vp.write(vrepo)
            self.console.print(
                "[bold green][+] Successfully updated :thumbs_up: [/bold green]\n")
            conn.close()
            exit()

    def disable(self):
        sites = self._sites.readlines()
        self._hosts.write(
            f"\n# Website Disable on {self.today} with wBlocker Tools")
        with self.console.status("[bold green]Working on task ...") as status:
            for s in sites:
                s = s.strip()
                if len(s) < 6:
                    continue
                self._hosts.write("\n" + self.ipder + " " + s)
                self.console.print("[bold green]BLOCKED[/bold green] -", s)
                time.sleep(0.5)
            self._hosts.close()
            self._sites.close()
            self.console.print(
                "\nNote: All sites have been [bold green][u]BLOCKED[/u][/bold green] ! \n")

    def unblock_all_site(self):
        dhosts = open(default_hosts, 'r')
        hosts = open(hosts_path, 'w')
        hosts.truncate()
        hosts.write(dhosts.read())
        self.console.print(
            "[bold green]Successfully[/bold green] opened all sites that have been blocked! \n")
        hosts.close()
        dhosts.close()

    def main(self):
        while self.exit == False:
            os.system(clearT)
            self.console.print(
                "++++++++++++++++++++++++++++++++++++", style="bold green")
            self.console.print(
                "     WBlocker Tools by Dhitznswa    ", style="bold red")
            self.console.print(
                "++++++++++++++++++++++++++++++++++++", style="bold green")
            self.console.print("[WB-001] Block Site", style="blue")
            self.console.print("[WB-002] Unblock Site", style="blue")
            self.console.print("[WB-999] Exit Tools", style="blue")
            self.console.print(
                "++++++++++++++++++++++++++++++++++++", style="bold green")
            pilih = input("[+] Option? WB-")
            self.console.print(
                f"\nAction For Code (WB-{pilih}) :", style="bold blue")
            if pilih == "001":
                self.disable()
                self.console.print("Please wait 6s ..", style="dim")
                time.sleep(6)
            elif pilih == "002":
                self.unblock_all_site()
                self.console.print("Please wait 6s ..", style="dim")
                time.sleep(5)
            elif pilih == "999":
                self.exit = True
                self.console.print(
                    "[bold green]Goodbay :thumbs_up:[/bold green] Thank you for using these tools\n")
            else:
                self.console.print(
                    '\n[bold red]FAILED :[/bold red] What you entered is not in the list of options\n')
                self.console.print("Please wait 6s ..", style="dim")
                time.sleep(5)


if __name__ == "__main__":
    wBlocker().main()
