import urllib.request, urllib.error, urllib.parse
import json
import sys
import os
import time

VERSION = "1.0"

def query_arin_ip(ip):
        request = urllib.request.Request("https://whois.arin.net/rest/ip/%s" % ip)
        request.add_header("Accept", "application/json")
        response = ""

        try:
                response = urllib.request.urlopen(request)
        except:
                print("[-] ARIN API failed to return proper data")
                return None

        return json.loads(response.read())

def get_org(data):
        if "orgRef" in data["net"]:
                return data["net"]["orgRef"]["@name"]
        if "customerRef" in data["net"]:
                return data["net"]["customerRef"]["@name"]
        return "N/A"

if __name__ == "__main__":
        save_csv = False
        verbose = False
        get_range = False
        if "debug" in sys.argv:
            verbose = True
        if "range" in sys.argv:
            get_range = True
        output = ""
        print("Search IP Owner v%s\nMr.Un1k0d3r RingZer0 Team\n---------------------------------------------------------\n" % VERSION)

        if len(sys.argv) < 2:
                print("Usage: %s path [option]\n\n\tPath\tPath to a file that contains bunch of IPs\n\t-csv\tSave to a file in CSV format" % sys.argv[0])
                sys.exit(0)

        if not os.path.exists(sys.argv[1]):
                print("[-] %s not found")
                sys.exit(0)

        if "-csv" in sys.argv:
                save_csv = True

        for ip in open(sys.argv[1], "r").readlines():
                try:
                        current = ip.strip()
                        data = query_arin_ip(current)
                        name = get_org(data)
                        netBlock = data["net"]["netBlocks"]
                        ip_range = ""
                        if get_range:
                            ip_range = "%s/%s" % (netBlock["netBlock"]["startAddress"]["$"], netBlock["netBlock"]["cidrLength"]["$"])
                        print("[+] %s" % current)
                        print(" |_ %s" % name)
                        if get_range:
                            print(" \\_ %s\n" % ip_range)
                        if save_csv:
                                output += "%s,%s,%s\r\n" % (current, ip_range, name)
                except Exception as e:
                        if verbose:
                            print("[-] Error: %s" % e)
                        print("[+] %s" % current)
                        print(" |_ No Result\n")
                        output += "%s,null,null\n" % current

        if save_csv:
                path = "%s/%s.csv" % (os.getcwd(), time.time())
                open(path, "w+").write(output)
                print("[+] Output saved to %s" % path)
