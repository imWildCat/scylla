class ProxyIP(object):

    def __init__(self, ip: str, port: str):
        """Initialize the ProxyIP object

        :param ip: the ip address
        :type ip: str
        :param port: the port number
        :type port: str
        """

        self.ip = ip
        self.port = int(port)

    def __str__(self):
        return '[class scylla.proxy_ip.ProxyIP {}:{}]'.format(self.ip, self.port)

    def __repr__(self):
        return self.__str__()
