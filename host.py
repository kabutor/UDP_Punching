import asyncio, time
DEBUG=True
servidor="1.1.1.1" #write here the ip of the server
class DiscoveryProtocol(asyncio.DatagramProtocol):
    def __init__(self):
        super().__init__()
        self.cola = []
    async def _punch(self, direccion):
        print ("punch " + str(direccion) )
        for i in range(10):
            time = 1
            await asyncio.sleep(time)
            self.transport.sendto(("GO#" + str(i)).encode(), (direccion[0],int(direccion[1])))
            print("sending Punch -> " + str(direccion))

    def connection_made(self, transport):
        self.transport = transport
        print ("conn ", end="")
        self.sock = transport.get_extra_info('socket') 
        self.lport = (self.sock.getsockname()[1])
        
        print (self.lport)
        if (self.lport==9002):
            enviar=b'HELLO'
            self.transport.sendto(enviar, (servidor,5000))
    def datagram_received(self, data, addr):
        recieved = data.decode('utf-8') 
        if (DEBUG): {print("recieved: " + recieved + " " + str(self.lport) , end="" )}
        if (DEBUG):{ print (" address: " + str(addr))}
        
        mensaje = recieved.split("#")
        
        if (mensaje[0] == "QUEUE"):
            if (DEBUG): {print("recibido QUEUE <- " + str(addr) )}

        if (mensaje[0] == "CONN"):
            self._udppunch = asyncio.ensure_future(self._punch( (mensaje[1], mensaje[2]) ) )
            print (mensaje[1] + " " + mensaje [2]) 

            
def start_discovery():
    loop = asyncio.get_event_loop()
    t = loop.create_datagram_endpoint(DiscoveryProtocol,local_addr=('0.0.0.0',9002))
    
    loop.run_until_complete(t)

    loop.run_forever()

start_discovery()
