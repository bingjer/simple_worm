==========================================================================
Adam Nelson
CPSC 456
Assignment 2
4/28/2021
==========================================================================
Files Included in the zip: 
 worm.py - The executable python script.
 REAME.txt - This file.
==========================================================================
This project was completed using python 2.7.17 on the GNS3 Lubuntux hosts.
The GNS3 network topology was established per assignment 2's instructions
and the DHCP set up was followed exactly as in class on 4/23. Testing was
performed on my GNS3 setup. Successful completetion was proven by showing
"infected.txt" and "worm.py" created in the /tmp directory of every 
Lubuntu machine (3 total). No extra credit was attempted. 
==========================================================================
Instructions to execute worm:
1) Make sure you have a network topology setup and running like the 
	instructions for assignment 2.
2) Check the /tmp directory and delete any file called "infected.txt"
	as we are assuming we are acting on a victim, thus the file
	should not be there.
3) In your terminal, navigate to the directory where you have 
	stored the file, "worm.py".
4) In your terminal execute the following "python worm.py".
5) Wait as the terminal displays information about spreading and
	unsuccseful attacks.
6) When the spreading is complete, the terminal will display 
	"Spreading Complete".
7) Verify all Lubuntu systems are infected by viewing "worm.py"
	and "infected.txt" in the /tmp directory of each machine.

