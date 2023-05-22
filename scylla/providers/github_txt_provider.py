from scylla.providers.plain_text_provider import PlainTextProvider

class TheSpeedXProvider(PlainTextProvider):

    def urls(self) -> [str]:
        return [
            'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt',
            'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt',
            'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt',
            'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http%2Bhttps.txt',
            'https://sunny9577.github.io/proxy-scraper/proxies.txt'
        ]
