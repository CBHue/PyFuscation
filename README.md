# PyFuscation

Requires python3 

![alt text](https://github.com/CBHue/PyFuscation/blob/dev/PyFuscation.png)

usage: PyFuscation.py [-h] [-w] [-f] [-v] [-p] [--ps SCRIPT] 

Optional arguments: 

	• -h, --help show this help message and exit
  
	• -f    Obfuscate functions
		○ Do this First ... Its probably the most likely to work well
		
	• -v    Obfuscate variables
		○ If your going to obfuscate variables do the parameters too. 
		
	• -p    Obfuscate parameters
		○  If your going to obfuscate parameters do the variables too. 

	• -w    Remove WhiteSpace/Comments
		○  Remove the comments and whitespace. 

Required arguments:
--ps  <SCRIPT> 	Obfuscate script 

	python3 PyFuscation.py -wfvp --ps ./Scripts/Invoke-Mimikatz.ps1 
