import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from django.core.files.base import ContentFile

# Try platform font paths in order: Linux (Render/Ubuntu), Windows, macOS.
# Falls back to PIL's built-in bitmap font if nothing is found.
_FONT_CANDIDATES = {
    'Arial': [
        '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/truetype/freefont/FreeSans.ttf',
        r'C:\Windows\Fonts\arial.ttf',
        '/Library/Fonts/Arial.ttf',
        '/System/Library/Fonts/Supplemental/Arial.ttf',
    ],
    'Arial Bold': [
        '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
        '/usr/share/fonts/truetype/freefont/FreeSansBold.ttf',
        r'C:\Windows\Fonts\arialbd.ttf',
    ],
    'Times New Roman': [
        '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',
        '/usr/share/fonts/truetype/freefont/FreeSerif.ttf',
        r'C:\Windows\Fonts\times.ttf',
    ],
    'Courier New': [
        '/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',
        '/usr/share/fonts/truetype/freefont/FreeMono.ttf',
        r'C:\Windows\Fonts\cour.ttf',
    ],
    'Verdana': [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
        '/usr/share/fonts/truetype/freefont/FreeSans.ttf',
        r'C:\Windows\Fonts\verdana.ttf',
    ],
}


def _load_font(family, size):
    for path in _FONT_CANDIDATES.get(family, []):
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def _hex_to_rgb(hex_color):
    h = hex_color.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def _image_to_pdf(pil_image, attendee_uuid):
    """Wrap a PIL image in a single-page PDF. Page size matches image at 96 DPI."""
    w_px, h_px = pil_image.size
    w_pt = w_px * 72 / 96
    h_pt = h_px * 72 / 96

    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=(w_pt, h_pt))

    img_buf = BytesIO()
    pil_image.convert('RGB').save(img_buf, format='PNG')
    img_buf.seek(0)
    c.drawImage(ImageReader(img_buf), 0, 0, w_pt, h_pt)
    c.save()
    return ContentFile(buf.getvalue(), name=f'badge_{attendee_uuid}.pdf')


def _render_with_template(attendee, template):
    """Render badge using event's BadgeTemplate (background image + coordinates)."""
    bg = Image.open(template.background_image.path).convert('RGBA')
    draw = ImageDraw.Draw(bg)

    color = _hex_to_rgb(template.text_color)
    font_name = _load_font(template.font_family, template.font_size)
    font_detail = _load_font(template.font_family, max(int(template.font_size * 0.65), 16))

    draw.text((template.name_x, template.name_y), attendee.full_name, font=font_name, fill=color)

    if attendee.company:
        draw.text((template.company_x, template.company_y), attendee.company, font=font_detail, fill=color)

    if attendee.job_title:
        draw.text((template.job_title_x, template.job_title_y), attendee.job_title, font=font_detail, fill=color)

    if attendee.qr_code and os.path.exists(attendee.qr_code.path):
        qr = Image.open(attendee.qr_code.path).convert('RGBA')
        qr = qr.resize((template.qr_size, template.qr_size))
        bg.paste(qr, (template.qr_x, template.qr_y), qr)

    return _image_to_pdf(bg, attendee.uuid)


def _render_fallback(attendee):
    """Clean default badge layout used when no BadgeTemplate exists for the event."""
    from reportlab.lib.units import mm
    from reportlab.lib import colors

    BADGE_W = 100 * mm
    BADGE_H = 70 * mm

    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=(BADGE_W, BADGE_H))

    c.setFillColor(colors.white)
    c.rect(0, 0, BADGE_W, BADGE_H, fill=1, stroke=0)
    c.setFillColor(colors.HexColor('#1a237e'))
    c.rect(0, BADGE_H - 14 * mm, BADGE_W, 14 * mm, fill=1, stroke=0)

    c.setFillColor(colors.white)
    c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(BADGE_W / 2, BADGE_H - 9 * mm, attendee.event.name[:40])

    c.setFillColor(colors.black)
    c.setFont('Helvetica-Bold', 18)
    c.drawCentredString(BADGE_W / 2, BADGE_H - 28 * mm, attendee.full_name[:35])

    c.setFont('Helvetica', 10)
    c.setFillColor(colors.HexColor('#444444'))
    if attendee.job_title:
        c.drawCentredString(BADGE_W / 2, BADGE_H - 36 * mm, attendee.job_title[:40])

    c.setFont('Helvetica-Bold', 10)
    c.setFillColor(colors.HexColor('#1a237e'))
    if attendee.company:
        c.drawCentredString(BADGE_W / 2, BADGE_H - 43 * mm, attendee.company[:40])

    if attendee.qr_code and os.path.exists(attendee.qr_code.path):
        qr_size = 22 * mm
        c.drawImage(ImageReader(attendee.qr_code.path),
                    BADGE_W - qr_size - 4 * mm, 4 * mm, qr_size, qr_size)

    c.setFont('Helvetica', 5)
    c.setFillColor(colors.grey)
    c.drawRightString(BADGE_W - 4 * mm, 2.5 * mm, str(attendee.uuid)[:18] + '…')
    c.setStrokeColor(colors.HexColor('#1a237e'))
    c.setLineWidth(1)
    c.line(0, 0, BADGE_W, 0)
    c.save()
    return ContentFile(buf.getvalue(), name=f'badge_{attendee.uuid}.pdf')


def generate_badge_pdf(attendee):
    """
    Entry point. Uses event's BadgeTemplate if configured, otherwise fallback layout.
    Returns a ContentFile (PDF).
    """
    try:
        template = attendee.event.badge_template
        if template.background_image:
            return _render_with_template(attendee, template)
    except Exception:
        pass
    return _render_fallback(attendee)
