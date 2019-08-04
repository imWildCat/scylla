from scylla.providers.plain_text_provider import PlainTextProvider

class PubproxyProvider(PlainTextProvider):

    def urls(self) -> [str]:
        return [
            'http://pubproxy.com/api/proxy?limit=5&format=txt&type=http&level=anonymous&last_check=60&no_country=CN',
        ]
