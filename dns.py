import csv

""" dnscrypt-resolvers.csv
['Name', 'Full name', 'Description', 'Location', 'Coordinates', 'URL', 'Version', 'DNSSEC validation', 'No logs', 'Namecoin', 'Resolver address', 'Provider name', 'Provider public key', 'Provider public key TXT record']
"""

try:
	infos = [ "name", "fullname", "desc", "location", "coords", "url", "version", "dnssec", "nologs", "namecoin", "ip4addr", "provname", "provkey", "provtxt" ]
	DATA = {}
	with open('dnscrypt-resolvers.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, quotechar='"')
		for row in reader:
			i = 0
			name = row[i]
			TMPDATA = {}
			if "d0wn" in name:
				for info in infos:
					TMPDATA[info] = row[i]
					i += 1
				#print TMPDATA
				#print TMPDATA["dnssec"]
			#if i > 0:
			#	print i
		
except:
	pass


try:
	DATA = {}
	with open('dns.txt', 'rb') as csvfile:
		reader = csv.reader(csvfile, quotechar='"')
		for row in reader:
			name = row[0]
			ip4addr = row[1]
			ip6addr = row[2]
			location = row[3]
			provkey = row[4]
			provname = row[5]
			ports = row[6]
			validto = row[7]
			provtxt = row[8]
			hoster = row[9]
			sponsor = row[10]
			sponsorurl = row[11]
			active = row[12]
			
			addname = "%s-%s-%s" % (name.split(".")[3],name.split(".")[1],name.split(".")[0])
			fullname = "OpenNIC Resolver %s %s @ Ports %s" % (location,name.split(".")[0].upper(),ports)
			desc = "provided by dns.d0wn.biz"
			coords = ""
			url = "https://dns.d0wn.biz"
			version = 1
			dnssec = "no"
			nologs = "yes"
			namecoin = "yes"
			if len(provkey) == 79:
				DATA[name] = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (addname,fullname,desc,location,coords,url,version,dnssec,nologs,namecoin,ip4addr,provname,provkey,provtxt)
				print DATA[name]
				fp = open("d0wns.csv",'a')
				writedata = "%s\n" % DATA[name]
				fp.write(writedata)

except:
	print "reading dns.txt fail"