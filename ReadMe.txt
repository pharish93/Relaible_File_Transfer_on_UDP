IP Project 2 
Go Back N Protocol on top of UDP sockets 

Name:
Harish Pullagurla 200178872 hpullag@ncsu.edu
	Venkatasuryasubrahmanyam Nukala 200158956 vnukala@ncsu.edu

Code tested on Python 2.7 

Steps to Run the project . 

1. 	a) Put the server.py file located in the server directory on the host system .
	b) Run it first through the command line with the inputs 
	python server.py <portno : 7735> <FIle name :server.txt> <probability :0.05 >
	example : python server.py 7735 'server.txt' 0.05

2.	a) Run the client.py file located in the client directory on your system after knowing the server Ip address 
	python client.py <server ip > <server port :7735> <filename :client.txt> <N window size :10> <MSS :500>
	example : python client.py 152.46.18.96 7735 'client.txt' 64 500

Note : Run step 1 and step 2 in the same order.
At the end of the program . clinet.py prints the time taken for executing the program 