#-plugin-sig:SuxBwt1CtR8NzDKEBZ2blx0jG3SP8OrDbEKQCeIqhe8ftfkPxJRa8V8evJeQjVd/cyswDCqc36ZkHhjKDCmeonTMFyO/Vdzw14TcfYP7milrwj8mqWKXw8gGt6Y3on/nSvRHBaDSqp9HQOU/yLQyEPxEbsqdFm07icSTPWk6A5JuzF4joE44QLV8JhR/m/9HELxnt0uBlnmUBwmFA43jVyEeO8SYijcJgMbv2qSQzWCNsVueQ3W8oaI49hAGHe+dJ9aco9RTZpArRQSzMDU3MAkzDdIR9aVyhSWtT+9jwo3zPgNJvAkQnl6mq0dCbNz60w46MoApYhZtf4PseMu6dA==
import re

from functools import partial

from ACEStream.PluginsContainer.livestreamer.plugin import Plugin
from ACEStream.PluginsContainer.livestreamer.plugin.api import http, validate
from ACEStream.PluginsContainer.livestreamer.stream import HLSStream, HDSStream

STREAM_INFO_URL = "http://live.daserste.de/{0}/livestream.xml"
SWF_URL = "http://live.daserste.de/lib/br-player/swf/main.swf"
STREAMING_TYPES = {
    "streamingUrlLive": (
        "HDS", partial(HDSStream.parse_manifest, pvswf=SWF_URL)
    ),
    "streamingUrlIPhone": (
        "HLS", HLSStream.parse_variant_playlist
    )
}

_url_re = re.compile("http(s)?://live.daserste.de/(?P<channel>[^/?]+)?")

_livestream_schema = validate.Schema(
    validate.xml_findall("video/*"),
    validate.filter(lambda e: e.tag in STREAMING_TYPES),
    validate.map(lambda e: (STREAMING_TYPES.get(e.tag), e.text)),
    validate.transform(dict),
)

class ard_live(Plugin):
    @classmethod
    def can_handle_url(cls, url):
        return _url_re.match(url)

    def _get_streams(self):
        match = _url_re.match(self.url)
        channel = match.group("channel")
        res = http.get(STREAM_INFO_URL.format(channel))
        urls = http.xml(res, schema=_livestream_schema)

        streams = {}
        for (name, parser), url in urls.items():
            try:
                streams.update(parser(self.session, url))
            except IOError as err:
                self.logger.warning("Unable to extract {0} streams: {1}", name, err)

        return streams

__plugin__ = ard_live
