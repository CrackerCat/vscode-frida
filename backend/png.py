import base64
import zlib, struct

def encode(buf, width, height):
    """ buf: must be bytes or a bytearray in Python3.x,
        a regular string in Python2.x.
    """


    width_byte_4 = width * 4
    raw_data = b''.join(
        b'\x00' + buf[span:span + width_byte_4]
        for span in range(0, (height - 1) * width_byte_4, width_byte_4)
    )

    def png_pack(png_tag, data):
        chunk_head = png_tag + data
        return (struct.pack("!I", len(data)) +
                chunk_head +
                struct.pack("!I", 0xFFFFFFFF & zlib.crc32(chunk_head)))

    return b''.join([
        b'\x89PNG\r\n\x1a\n',
        png_pack(b'IHDR', struct.pack("!2I5B", width, height, 8, 6, 0, 0, 0)),
        png_pack(b'IDAT', zlib.compress(raw_data, 9)),
        png_pack(b'IEND', b'')])


def to_uri(icon):
    if not icon:
        return None

    if type(icon) is dict:
        buf = encode(icon['image'], icon['width'], icon['height'])
    else:
        assert icon.rowstride == icon.width * 4
        buf = encode(icon.pixels, icon.width, icon.height)

    return 'data:image/png;base64,' + base64.b64encode(buf).decode('ascii')