import asyncio

global memory


class ClientServerProtocol(asyncio.Protocol):


    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        global memory
        answer = ''
        try:
            data_decoded = data.decode()
        except Error:
            return "error\n{wrong command}\n\n"

        data_temp = data_decoded.replace('\n', '').split()

        try:
            if data_temp[0] == 'put':
                if memory.find(data_decoded.replace('put','')) == -1:
                    memory += data_decoded('put', '')
                else:
                    memory = memory.replace(data_decoded.replace('put', ''),'')
                    memory += data_decoded.replace('put', '')
                answer = 'ok\n\n'
            elif data_temp[0] == "get":
                key = data_temp[1]
                if key == '*':
                    answer = 'ok\n' + memory + '\n'
                else:
                    for metric in memory.split('\n'):
                        if len(metric.split()) == 3 and metric.split()[0]== key:
                            answer = 'ok\n' + metric + '\n\n'

        except Error:
            self.transport.write(b'f"error\n{wrong command}\n\n"')

        self.transport.write(answer.encode())


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    run_server('127.0.0.1', 8888)
