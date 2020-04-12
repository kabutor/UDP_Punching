# UDP_Punching

UDP Punching is where two hosts behind a NAT (A and B) try to establish a direct connection, using a server (S) just for matchmaking. Both hosts connect to the server at port 5000, server will swap the IP/Port of the other client and send it, then both hosts will initiate a connection to the other client, so the NAT will know where to route the packets to.

I needed that for a game in Unity I was doing, so I just did it in python to test it, you can find the server and client files here, server need to have direct connection to the internet, or forward UDP port number 5000 (in the example, you can change it to any other port number) to the server.

It took me some time until I made it work, in case you are trying to do something like this, here is a tip, once the ip are swapped to the clients, don't send the signal to the other host once, do it 5-10 times and then it will work.

