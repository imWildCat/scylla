from scylla.providers.plain_text_provider import PlainTextProvider

class RudnkhProvider(PlainTextProvider):

    def urls(self) -> [str]:
        return [
            'https://proxy.rudnkh.me/txt',
        ]
