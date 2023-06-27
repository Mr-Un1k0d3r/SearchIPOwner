import urllib.request
import json
import sys
import os
import time

VERSION = "1.0"

def query_arin_ip(ip):
	url = f"https://whois.arin.net/rest/ip/{ip}"
	request = urllib.request.Request(url)
	request.add_header("Accept", "application/json")

	try:
		with urllib.request.urlopen(request) as response:
			data = json.loads(response.read().decode())
	except:
		print("[-] ARIN API failed to return proper data")
		return None

	return data

def get_org(data):
	if "orgRef" in data["net"]:
		return data["net"]["orgRef"]["@name"]
	if "customerRef" in data["net"]:
		return data["net"]["customerRef"]["@name"]
	return "null"

if __name__ == "__main__":
	save_csv = False
	output = ""
	print(f"Search IP Owner v{VERSION}\nMr.Un1k0d3r RingZer0 Team\n---------------------------------------------------------\n")

	if len(sys.argv) < 2:
		print(f"Usage: {sys.argv[0]} path [option]\n\n\tPath\tPath to a file that contains bunch of IPs\n\t-csv\tSave to a file in CSV format")
		sys.exit(0)

	if not os.path.exists(sys.argv[1]):
		print(f"[-] {sys.argv[1]} not found")
		sys.exit(0)

	if "-csv" in sys.argv:
		save_csv = True

	with open(sys.argv[1], "r") as f:
		for ip in f.readlines():
			try:
				current = ip.strip()
				data = query_arin_ip(current)
				name = get_org(data)
				netBlock = data["net"]["netBlocks"]
				range = f"{netBlock['netBlock']['startAddress']['$']}/{netBlock['netBlock']['cidrLength']['$']}"
				print(f"[+] {current}")
				print(f" |_ {name}")
				print(f" \_ {range}\n")
				if save_csv:
					output += f"{current},{range},{name}\n"
			except:
				print(f"[+] {current}")
				print(" |_ No Result\n")
				if save_csv:
					output += f"{current},null,null\n"

	if save_csv:
		path = f"{os.getcwd()}/{time.time()}.csv"
		with open(path, "w+") as f:
			f.write(output)
		print(f"[+] Output saved to {path}")
