import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from .models import Attendee
from .utils.badge_generator import generate_badge_pdf
from .utils.print_service import send_to_printer


def home(request):
    return HttpResponse('EventPass is running')


def health_check(request):
    return JsonResponse({'status': 'ok', 'project': 'EventPass'})


def scan_page(request):
    return render(request, 'core/scan.html')


@csrf_exempt
def checkin_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    uuid_str = data.get('uuid', '').strip()
    if not uuid_str:
        return JsonResponse({'error': 'uuid is required'}, status=400)

    try:
        attendee = Attendee.objects.select_related('event').get(uuid=uuid_str)
    except (Attendee.DoesNotExist, ValueError):
        return JsonResponse({'error': 'Attendee not found'}, status=404)

    if attendee.is_checked_in:
        return JsonResponse({
            'status': 'already_checked_in',
            'name': attendee.full_name,
            'event': attendee.event.name,
            'checked_in_at': attendee.checked_in_at.isoformat(),
            'print_status': 'skipped',
        })

    # Mark checked in
    attendee.is_checked_in = True
    attendee.checked_in_at = timezone.now()
    attendee.save(update_fields=['is_checked_in', 'checked_in_at'])

    # Generate badge PDF
    pdf_file = generate_badge_pdf(attendee)
    attendee.badge_pdf.save(pdf_file.name, pdf_file, save=True)

    # Send to printer
    print_result = send_to_printer(attendee.badge_pdf.path)

    if print_result['success']:
        attendee.badge_printed = True
        attendee.badge_print_count += 1
        attendee.save(update_fields=['badge_printed', 'badge_print_count'])

    return JsonResponse({
        'status': 'checked_in',
        'name': attendee.full_name,
        'event': attendee.event.name,
        'uuid': str(attendee.uuid),
        'checked_in_at': attendee.checked_in_at.isoformat(),
        'print_status': 'success' if print_result['success'] else 'failed',
        'print_error': print_result.get('error'),
    })
