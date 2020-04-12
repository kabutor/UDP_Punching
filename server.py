import asyncio, time
DEBUG=True

class DiscoveryProtocol(asyncio.DatagramProtocol):
    def __init__(self):
        super().__init__()
        self.cola = []
                
    async def _pasatiempo(self):
        await asyncio.sleep(self.timer)
        if (DEBUG): {print ("time out no match empty queue")}
        self.cola.pop()
        self._keepalive.cancel()
    async def _keepa(self, direcc):
        for i in range(60):
            await asyncio.sleep(self.time_keep_alive)
            self.transport.sendto(b'KA',direcc)
            print ('Keepalive :' + str(direcc))
    def connection_made(self, transport):
        self.transport = transport
        print ("conn")
    def datagram_received(self, data, addr):
        recieved = data.decode('utf-8') 
        if (DEBUG): {print("recieved: " + recieved, end="" )}
        if (DEBUG):{ print (" address: " + str(addr))}
       
        if (recieved == "HELLO"):
            #test if someone is on the queue
            if not self.cola:
                #empty queue
                if (DEBUG): {print("Player add to QUEUE")}
                self.cola.append(addr)
                #send Queue signal
                self.transport.sendto(b'QUEUE', (addr) )
                if (DEBUG): {print("send to QUEUE: " + str(addr))}
                #enable timeout to disconnect host
                self.timer = 25 
                self._crono =  asyncio.ensure_future(self._pasatiempo())
                #enable 1second keepalive signal (not needed)
                self.time_keep_alive = 5
                self._keepalive = asyncio.ensure_future(self._keepa(addr))

            else:
                self._keepalive.cancel()
                #someone on queue
                if (DEBUG): {print("CLIENT matched to QUEUE")}
                #UDP PUNCHING
                #send to the Queue the ip of the new Client
                sending = ("CONN" + "#" + str(addr[0]) + "#" + str(addr[1]) ).encode()
                direccion = (self.cola[0][0], self.cola[0][1])
                if (DEBUG): {print("send CONN to Queue " + str(sending) + " -> " + str(direccion) )}
                self.transport.sendto(sending,  direccion )

            

                #send the IP of queue to the other Host
                sending = ("CONN" + "#" + str(self.cola[0][0]) + "#" + str(self.cola[0][1]) ).encode()
                if (DEBUG): {print("send CONN to Client: " + str(sending) + " -> " + str(addr) )}
                self.cola.pop()
                self._crono.cancel()
                self.transport.sendto(sending, addr )

            
def start_discovery():
    loop = asyncio.get_event_loop()
    t = loop.create_datagram_endpoint(DiscoveryProtocol,local_addr=('0.0.0.0',5000))
    loop.run_until_complete(t)
    loop.run_forever()

start_discovery()
