from django.contrib import admin
from django.utils.html import format_html
from .models import Event, AttendeeType, BadgeTemplate, Attendee


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'registration_url': ('name',)}


@admin.register(AttendeeType)
class AttendeeTypeAdmin(admin.ModelAdmin):
    list_display = ('label', 'name', 'event', 'badge_color')
    list_filter = ('event',)


@admin.register(BadgeTemplate)
class BadgeTemplateAdmin(admin.ModelAdmin):
    list_display = ('event', 'font_family', 'font_size', 'text_color', 'updated_at')
    readonly_fields = ('background_preview',)
    fieldsets = (
        ('Event', {
            'fields': ('event',),
        }),
        ('Background Design', {
            'fields': ('background_image', 'background_preview'),
            'description': 'Upload the badge background image (PNG/JPG). '
                           'Coordinates below are pixel positions measured from the top-left corner.',
        }),
        ('Typography', {
            'fields': ('font_family', 'font_size', 'text_color'),
        }),
        ('Field Positions (pixels from top-left)', {
            'fields': (
                ('name_x', 'name_y'),
                ('company_x', 'company_y'),
                ('job_title_x', 'job_title_y'),
                ('qr_x', 'qr_y', 'qr_size'),
            ),
            'description': 'Set the X/Y pixel position for each field on the badge. '
                           'Open your background image in any image editor to find the coordinates.',
        }),
    )

    def background_preview(self, obj):
        if obj.background_image:
            return format_html(
                '<img src="{}" style="max-width:500px; max-height:350px; border:1px solid #ccc;" />',
                obj.background_image.url,
            )
        return 'No background image uploaded yet.'
    background_preview.short_description = 'Preview'


@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'company', 'event', 'attendee_type', 'is_checked_in', 'badge_printed', 'registered_at')
    list_filter = ('event', 'attendee_type', 'is_checked_in', 'badge_printed')
    search_fields = ('full_name', 'email', 'company')
    readonly_fields = ('uuid', 'registered_at', 'qr_code_preview', 'badge_pdf_link')

    def qr_code_preview(self, obj):
        if obj.qr_code:
            return format_html(
                '<p><strong>UUID:</strong> {}</p>'
                '<img src="{}" width="150" height="150" />',
                obj.uuid,
                obj.qr_code.url,
            )
        return 'Not generated yet'
    qr_code_preview.short_description = 'QR Code'

    def badge_pdf_link(self, obj):
        if obj.badge_pdf:
            return format_html('<a href="{}" target="_blank">Download Badge PDF</a>', obj.badge_pdf.url)
        return 'Not generated yet'
    badge_pdf_link.short_description = 'Badge PDF'
