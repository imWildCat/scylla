from scylla.providers.plain_text_provider import PlainTextProvider

class RmccurdyProvider(PlainTextProvider):

    def urls(self) -> [str]:
        return [
            'https://www.rmccurdy.com/scripts/proxy/good.txt',
        ]
