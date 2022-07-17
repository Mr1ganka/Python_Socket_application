Before Running the application get inside the base directory and activate the environmnt with ".\env\Scripts\activate" Then make sure to install the requirements using "pip install -r requirements.py"

After the above steps have been completed use "flask run" to run the server -On a different terminal use "python client.py" to run the client

--you can have more than 1 clients

--use "!clients" to get the number of connections

--use "!elapsed" to get the time which elapsed since the connection

--use "!current" to get the current server time stamp

--use "!disconnect" to disconnect the client from the server

--after every 60 seconds the server sends a connected message to all of its clients.