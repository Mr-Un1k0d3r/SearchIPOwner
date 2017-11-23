import urllib2
import json
import sys
import os
import time

VERSION = "1.0"

def query_arin_ip(ip):
	request = urllib2.Request("https://whois.arin.net/rest/ip/%s" % ip)
	request.add_header("Accept", "application/json")
	response = ""
	
	try:
		response = urllib2.urlopen(request)
	except:
		print "[-] ARIN API failed to return proper data"
		return None
	
	return json.loads(response.read())

if __name__ == "__main__":
	save_csv = False
	output = ""
	print "ARIN API search owner v%s\nMr.Un1k0d3r RingZer0 Team\n---------------------------------------------------------\n" % VERSION

	if len(sys.argv) < 2:
		print "Usage: %s path [option]\n\n\tPath\tPath to a file that contains bunch of IPs\n\t-csv\tSave to a file in CSV format" % sys.argv[0]
		sys.exit(0)
			
	if not os.path.exists(sys.argv[1]):
		print "[-] %s not found"
		sys.exit(0)
			
	if "-csv" in sys.argv:
		save_csv = True
			
	for ip in open(sys.argv[1], "rb").readlines():
		try:
			current = ip.strip()
			data = query_arin_ip(current)
			name = data["net"]["orgRef"]["@name"]
			netBlock = data["net"]["netBlocks"]
			range = "%s/%s" % (netBlock["netBlock"]["startAddress"]["$"], netBlock["netBlock"]["cidrLength"]["$"])
			print "[+] %s" % current
			print " |_ %s" % name
			print " \_ %s\n" % range
			if save_csv:
				output += "%s,%s,%s" % (current, range, name)
		except:
			print "[+] %s" % current
			print " |_ No Result\n"
			output += "%s,null,null" % current
		
	if save_csv:
		path = "%s/%s.csv" % (os.getcwd(), time.time())
		open(path, "wb+").write(output)
		print "[+] Output saved to %s" % path
