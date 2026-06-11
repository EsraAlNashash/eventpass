import qrcode
from io import BytesIO
from django.core.files.base import ContentFile


def generate_qr_code(uuid_value):
    """Generate a QR code image from a UUID and return a Django ContentFile."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(str(uuid_value))
    qr.make(fit=True)

    img = qr.make_image(fill_color='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return ContentFile(buffer.getvalue(), name=f'{uuid_value}.png')
