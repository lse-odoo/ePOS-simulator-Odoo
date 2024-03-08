
import base64
import datetime
import functools
from io import BytesIO
import re
from PIL import Image


class ImageInfo():
    def __init__(self, receipt_payload: bytes) -> None:
        self.receive_time = datetime.datetime.now()
        self.image = self._extract_image_from_payload(receipt_payload)

    def _extract_image_from_payload(self, receipt_payload: bytes) -> Image:
        # TODO: do with 1 regex (as the order is always the same)
        width = int(re.search(b'width="(\d+)"', receipt_payload).group(1))
        height = int(re.search(b'height="(\d+)"', receipt_payload).group(1))
        
        image_content_base_64 = re.search(b'<image .*?>(.*)</image>', receipt_payload).group(1)
        # TODO: maybe image_content_base_64 can be used to show the image in the browser directly ?

        # Reconvert the received data by something we can interpret
        decoded_string = base64.b64decode(image_content_base_64)
        binary_img = ''.join(format(byte, '08b') for byte in decoded_string)
        data = bytes([255 if b == '0' else 0 for b in binary_img])

        # TODO: check if mode 1 can be used instead of 'L'
        #  https://pillow.readthedocs.io/en/stable/handbook/concepts.html#modes
        return Image.frombytes('L', (width, height), data)
    
    @functools.cached_property
    def image_base_64(self):
        buff = BytesIO()
        self.image.save(buff, format="JPEG")
        return base64.b64encode(buff.getvalue()).decode('utf-8')
