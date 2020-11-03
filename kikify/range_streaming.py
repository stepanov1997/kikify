from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import mimetypes
import os
import re

range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)


class RangeFileWrapper(object):
    def __init__(self, bytes, blksize=2048, offset=0):
        self.bytes = bytes
        self.blksize = blksize
        self.offset = offset

    def close(self):
        if hasattr(self.filelike, 'close'):
            self.filelike.close()

    def __iter__(self):
        return self

    def next(self):
        # If remaining is None, we're reading the entire file.
        old_offset = self.offset
        if old_offset + self.blksize > len(bytes):
            self.offset = len(bytes)
            data = bytearray(self.bytes[old_offset:len(bytes)])
        else:
            self.offset += self.blksize
            data = bytearray(self.bytes[old_offset:self.offset])

        if data:
            return data
        raise StopIteration()


def stream(request, bytes):
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_match = range_re.match(range_header)
    size = len(bytes)
    content_type = 'application/octet-stream'
    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else size - 1
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(RangeFileWrapper(bytes=bytes, offset=first_byte), status=206,
                                     content_type=content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
    else:
        resp = StreamingHttpResponse(FileWrapper(bytes=bytes, content_type=content_type))
        resp['Content-Length'] = str(size)
    resp['Accept-Ranges'] = 'bytes'
    return resp
