# Phishtank to ELK
A program to import Phishtank https://www.phishtank.com/ dataset into elasticsearch

# Installation

	1. Clone or fork this repo git@github.com:michaelhidalgo/phishtank-to-elk.git
	2. Navigate to the root of the project
	3. Create a virtual environment using virtualenv:
	    virtualenv env
	4. Activate the virtual environment running source env/bin/activate from the root folder.
	5. Install dependencies from requirements file pip3 install -r requirements.txt
	6. Export following environment variables with Elasticsearch IP address and port:
	  export es_hostname='Your ELK IP'
	  export es_port='Your ELK port (9200 by default)'  
	7. Run the program using Python3:
	    python3 main.py
    
# Screenshots

