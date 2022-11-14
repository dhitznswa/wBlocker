try:
    import http.client as httplib
    import os
    import platform
    import sys
    import time
    from datetime import date
    from threading import Thread

    import requests
    from rich.console import Console
except ImportError:
    print('\nERROR: Module Not Found !!')
    print('[~] There are some modules that are not installed yet. Type "pip install -r request.txt" in the terminal with the path where your folder saves this tool\n')
    exit()


if platform.system() == "Windows":
    hosts_path = "C:\Windows\System32\drivers\etc\hosts"
else:
    hosts_path = "/etc/hosts"

version_path = os.path.join('core', 'version.txt')
default_hosts = os.path.join('core', 'default-hosts.txt')


class wBlocker():
    def __init__(self):
        self._path = hosts_path
        self.ipder = "127.0.0.1"
        self.done = False
        self.today = date.today().strftime("%d/%m/%Y")
        self.console = Console()

        try:
            self._sites = open('sites.txt', 'r')
        except FileNotFoundError:
            self.console.print(
                '\n[bold red]FAILED :[/bold red] Website list file not found !!\n')
            exit()
        try:
            self._sites = open(version_path, 'r')
        except FileNotFoundError:
            self.console.print(
                '\n[bold red]FAILED :[/bold red] Website list file not found !!\n')
            exit()
        try:
            self._hosts = open('hosts', 'a')
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
                "[bold blue][+] An update has been found ::: Updating...  [/bold blue]\n")
            conn.request("GET", "/dhitznswa/wBlocker/main/wBlocker.py")
            newCode = conn.getresponse().read().strip().decode()
            with open("wBlocker.py", "w") as wb:
                wb.write(newCode)
            with open(version_path, "w") as vp:
                vp.write(vrepo)
            self.console.print(
                "[bold green][*] Successfully updated :smile: [/bold green]\n")
            conn.close()
            exit()

    def disable(self):
        sites = self._sites.readlines()
        self._hosts.write(
            f"\n# Website Disable on {self.today} with wBlocker Tools")
        with self.console.status("[bold green]Working on task ...") as status:
            for site in sites:
                site = site.strip()
                if len(site) < 6:
                    continue
                self._hosts.write("\n" + self.ipder + " " + site)
                self.console.print("[bold green]BLOCKED[/bold green] -", site)
                time.sleep(0.5)
            self.done = True
            self._hosts.close()
            self._sites.close()
            self.console.print(
                "\nNote : All sites have been [bold green][u]BLOCKED[/u][/bold green] ! \n")

    def unblock_all_site(self):
        dhosts = open(default_hosts, 'r')
        hosts = open('hosts', 'w')
        hosts.truncate()
        hosts.write(dhosts.read())
        self.console.print(
            "\nNote : [bold green]Successfully[/bold green] opened all sites that have been blocked! \n")
        hosts.close()
        dhosts.close()


if __name__ == "__main__":
    wBlocker().update_wb()
