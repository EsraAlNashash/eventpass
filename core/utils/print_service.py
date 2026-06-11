import os
import subprocess
import sys


def send_to_printer(pdf_path):
    """Send a PDF file to the system default printer. Returns a status dict."""
    if not os.path.exists(pdf_path):
        return {'success': False, 'error': 'PDF file not found'}

    try:
        if sys.platform == 'win32':
            # Fire-and-forget: launch default PDF handler's print action
            os.startfile(pdf_path, 'print')
        else:
            # Linux/macOS
            subprocess.run(['lp', pdf_path], check=True, timeout=30)

        return {'success': True}

    except subprocess.TimeoutExpired:
        return {'success': False, 'error': 'Printer timeout'}
    except Exception as e:
        return {'success': False, 'error': str(e)}
