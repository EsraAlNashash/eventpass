import os
import subprocess
import sys

# Render injects this env var in all environments (build + runtime).
# When present, no physical printer is available — skip silently.
_PRINTING_AVAILABLE = not bool(os.environ.get('RENDER'))


def send_to_printer(pdf_path):
    """Send a PDF to the default printer. Returns a status dict.
    On Render (production), printing is unavailable — returns a graceful no-op
    so the check-in flow continues without error."""
    if not _PRINTING_AVAILABLE:
        return {'success': False, 'error': 'Printing not available in this environment'}

    if not os.path.exists(pdf_path):
        return {'success': False, 'error': 'PDF file not found'}

    try:
        if sys.platform == 'win32':
            os.startfile(pdf_path, 'print')
        else:
            subprocess.run(['lp', pdf_path], check=True, timeout=30)
        return {'success': True}
    except subprocess.TimeoutExpired:
        return {'success': False, 'error': 'Printer timeout'}
    except Exception as e:
        return {'success': False, 'error': str(e)}
