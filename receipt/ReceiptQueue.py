
from collections import deque

from receipt.ImageInfo import ImageInfo

_receipt_queue = deque(maxlen=50)

def add_receipt_to_queue(image_info: ImageInfo) -> None:
    _receipt_queue.append(image_info)

def get_receipts() -> list[ImageInfo]:
    return list(_receipt_queue)[::-1]
