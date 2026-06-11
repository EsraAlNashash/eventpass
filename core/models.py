import uuid
from django.db import models
from core.utils.qr_generator import generate_qr_code


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    logo = models.ImageField(upload_to='event_logos/', blank=True, null=True)
    registration_url = models.SlugField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class AttendeeType(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendee_types')
    name = models.CharField(max_length=100)
    label = models.CharField(max_length=100)
    badge_color = models.CharField(max_length=7, default='#000000', help_text='Hex color code')
    badge_tag = models.CharField(max_length=50, blank=True)

    class Meta:
        unique_together = ('event', 'name')

    def __str__(self):
        return f'{self.event.name} — {self.label}'


class BadgeTemplate(models.Model):
    FONT_CHOICES = [
        ('Arial', 'Arial'),
        ('Arial Bold', 'Arial Bold'),
        ('Times New Roman', 'Times New Roman'),
        ('Courier New', 'Courier New'),
        ('Verdana', 'Verdana'),
    ]

    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='badge_template')
    background_image = models.ImageField(upload_to='badge_backgrounds/')

    # Text field pixel coordinates (relative to top-left of background image)
    name_x = models.PositiveIntegerField(default=100)
    name_y = models.PositiveIntegerField(default=120)
    company_x = models.PositiveIntegerField(default=100)
    company_y = models.PositiveIntegerField(default=180)
    job_title_x = models.PositiveIntegerField(default=100)
    job_title_y = models.PositiveIntegerField(default=220)
    qr_x = models.PositiveIntegerField(default=400)
    qr_y = models.PositiveIntegerField(default=100)
    qr_size = models.PositiveIntegerField(default=150, help_text='QR code size in pixels')

    # Typography
    font_family = models.CharField(max_length=50, choices=FONT_CHOICES, default='Arial')
    font_size = models.PositiveIntegerField(default=36, help_text='Font size for attendee name (px)')
    text_color = models.CharField(max_length=7, default='#000000', help_text='Hex color, e.g. #000000')

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Badge template — {self.event.name}'


class Attendee(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendees')
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    company = models.CharField(max_length=255, blank=True)
    job_title = models.CharField(max_length=255, blank=True)
    attendee_type = models.ForeignKey(
        AttendeeType, on_delete=models.SET_NULL, null=True, blank=True, related_name='attendees'
    )
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    badge_pdf = models.FileField(upload_to='badges/', blank=True, null=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    is_checked_in = models.BooleanField(default=False)
    checked_in_at = models.DateTimeField(null=True, blank=True)
    badge_printed = models.BooleanField(default=False)
    badge_print_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-registered_at']
        unique_together = ('event', 'email')

    def __str__(self):
        return f'{self.full_name} ({self.event.name})'

    def save(self, *args, **kwargs):
        if not self.qr_code:
            self.qr_code.save(
                f'{self.uuid}.png',
                generate_qr_code(self.uuid),
                save=False,
            )
        super().save(*args, **kwargs)
