from scylla.providers.plain_text_provider import PlainTextProvider

class TheSpeedXProvider(PlainTextProvider):

    def urls(self) -> [str]:
        return [
            'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt',
            'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt',
            'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt',
        ]
