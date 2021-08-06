# Show inventory to csv by Bryan Barragán
# Written in Python 3.7.3

#Import libraries
import re
import csv
import os

def main():
	# Working directory
	path=os.getcwd()
	# Obtaining just the files
	onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
	print(onlyfiles)
	# Files untouched
	# n = onlyfiles.count("inventory.csv")
	#onlyfiles.pop(n)
	n = onlyfiles.index("inventory.py")
	onlyfiles.pop(n)
	# Regex's
	hostname_pattern = r"([\w\- ]+)#"
	serial_pattern = r"SN: ([\w\- ]+)"
	pid_pattern = r"PID: ([\w\- /]+)"
	name_pattern= r"NAME: \"([\w\(\)\- /+:]+)\""
	descr_pattern= r"DESCR: \"([\w\-,\(\) /+.]+)\""
	# Control variable to know when I have enough information
	patterns = 0
	# One file version
	#report_file = "10.141.4.1 2021 02 01 130308.txt"
	#report_file = "192.168.160.38 2021 02 01 130240.txt"

	output_file = 'inventory.csv'
	
	# Opening the output file
	with open(output_file, 'w', newline='') as f:
		fieldnames = ["Hostname", "Name", "Part ID", "Serial Number", "Description"]
		writer = csv.writer(f, delimiter=';')
		writer.writerow(fieldnames)
		# Walkthrough
		for report_file in onlyfiles:
			# Reading the content of each file
			with open(report_file, 'r') as f:
				lines=f.readlines()
				f.close()
			hostname = None
			# Control variable to collect information
			infoline = []
			for line in lines:
				# Searching
				obtain=re.search(serial_pattern, line)
				if obtain != None:			
					serial = obtain.group(1)
					patterns += 1
				if hostname == None:
					hostname=re.search(hostname_pattern, line)
				obtain=re.search(name_pattern, line)
				if obtain != None:
					name = obtain.group(1) 
					patterns += 1
				obtain=re.search(descr_pattern, line)
				if obtain != None:
					descr = obtain.group(1)
					patterns += 1
				obtain=re.search(pid_pattern, line)
				if obtain != None:
					pid = obtain.group(1)
					patterns += 1
				# Once I count 4 patterns I have enough information to push in the file
				if patterns == 4:
					infoline.clear()
					infoline.append(hostname[1])
					infoline.append(name)
					infoline.append(pid)
					infoline.append(serial)
					infoline.append(descr)
					writer.writerow(infoline)
					# Resetting the control variable to start another part on the show inventory
					patterns = 0
		f.close()

main()
