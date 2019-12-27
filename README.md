# PyFuscation

Requires python3 

![alt text](https://github.com/CBHue/PyFuscation/blob/master/PyFuscation.png)

usage: PyFuscation.py [-h] [-f] [-v] [-p] [--ps SCRIPT] 

Optional arguments: 

	• -h, --help show this help message and exit
  
	• -f    Obfuscate functions
		○ Do this First ... Its probably the most likely to work well
		
	• -v    Obfuscate variables
		○ If your going to obfuscate variables do the parameters too. 
		
	• -p    Obfuscate parameters
		○  If your going to obfuscate parameters do the variables too. 

Required arguments:
--ps  <SCRIPT> 	Obfuscate script 

	python3 PyFuscation.py -fvp --ps ./Scripts/Invoke-Mimikatz.ps1 
