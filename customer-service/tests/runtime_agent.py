import csv
import os
import time
import traceback
import sys
import inspect
import json
from datetime import datetime
from flask import request, g
from threading import Lock

# ========== Setup Directories ==========

BASE_DIR = os.path.dirname(__file__)
LOG_DIR = os.path.join(BASE_DIR, 'CodeTraceCSV')
os.makedirs(LOG_DIR, exist_ok=True)

# 🔁 Clean up all files in the log directory at startup
for filename in os.listdir(LOG_DIR):
    file_path = os.path.join(LOG_DIR, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)
        print(f"🧹 Deleted: {file_path}")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = os.path.join(LOG_DIR, f'runtime_method_logs-{timestamp}.csv')
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', 'app'))
MARKER_FILE = os.path.join(LOG_DIR, '.last-extracted.txt')

FIELDNAMES = [
    'timestamp', 'Event Type', 'Python File', 'Class Name', 'Method Name', 'Short Summary',
    'Input Type', 'Input Parameters', 'Return Type', 'Output Response', 'Error', 'API Path', 'HTTP Method'
]

extract_once_lock = Lock()

# ========== Serialization ==========

def safe_serialize(obj):
    def is_serializable(val):
        try:
            json.dumps(val)
            return True
        except Exception:
            return False

    try:
        if isinstance(obj, (list, tuple)):
            return [safe_serialize(item) for item in obj]
        elif isinstance(obj, dict):
            return {k: safe_serialize(v) for k, v in obj.items() if not k.startswith('_')}
        elif hasattr(obj, 'to_dict'):
            return safe_serialize(obj.to_dict())
        elif hasattr(obj, '__dict__'):
            raw = vars(obj)
            return {
                k: safe_serialize(v)
                for k, v in raw.items()
                if not k.startswith('_') and not isinstance(v, type(obj)) and is_serializable(v)
            }
        elif is_serializable(obj):
            return obj
        else:
            return str(obj)
    except Exception as e:
        return f"<Unserializable object: {e}>"

def write_log(entry):
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow(entry)

def get_latest_trace_file():
    files = [f for f in os.listdir(LOG_DIR) if f.startswith('runtime_method_logs')]
    files.sort(reverse=True)
    return os.path.join(LOG_DIR, files[0]) if files else None

# ========== Flask Middleware ==========

def init_runtime_logger(app):
    @app.before_request
    def log_request_info():
        g.start_time = time.time()
        g.request_data = request.get_json(silent=True) or request.form.to_dict() or request.args.to_dict()
        try:
            view_func = app.view_functions.get(request.endpoint)
            file_name = view_func.__module__ if view_func else 'unknown'
            method_name = view_func.__name__ if view_func else 'unknown'
            qualname = getattr(view_func, '__qualname__', '')
            class_name = qualname.split('.')[0] if '.' in qualname else ''

            g.func_info = {
                'timestamp': datetime.utcnow().isoformat(),
                'Event Type': 'ENTER',
                'Python File': file_name,
                'Class Name': class_name,
                'Method Name': method_name,
                'Short Summary': qualname,
                'Input Type': 'json/form/args',
                'Input Parameters': str(g.request_data),
                'Return Type': '',
                'Output Response': '',
                'Error': '',
                'API Path': request.path,
                'HTTP Method': request.method
            }
            write_log(g.func_info)
            sys.settrace(trace_internal_calls)
        except Exception as e:
            g.func_info = {
                'timestamp': datetime.utcnow().isoformat(),
                'Python File': 'unknown',
                'Class Name': '',
                'Method Name': '',
                'Short Summary': '',
                'Input Type': 'json/form/args',
                'Input Parameters': str(g.request_data),
                'Return Type': '',
                'Output Response': '',
                'Error': f"Exception in pre-request: {str(e)}",
                'API Path': request.path
            }

    @app.after_request
    def log_response_info(response):
        try:
            g.func_info.update({
                'Return Type': type(response).__name__,
                'Output Response': response.get_data(as_text=True),
                'Event Type': 'EXIT'
            })
            write_log(g.func_info)
        except Exception as e:
            print(f"Logging failed in after_request: {e}")
        finally:
            sys.settrace(None)
        return response

    @app.teardown_request
    def log_exception_info(exc):
        if exc:
            g.func_info.update({
                'Error': traceback.format_exc()
            })
            write_log(g.func_info)
            sys.settrace(None)

# ========== Tracer ==========

trace_map = {}

def trace_internal_calls(frame, event, arg):
    code = frame.f_code
    filename = frame.f_globals.get('__file__', '')

    if not filename or not os.path.abspath(filename).startswith(PROJECT_ROOT):
        return

    filename = os.path.relpath(os.path.abspath(filename), PROJECT_ROOT)
    func_name = code.co_name
    local_vars = frame.f_locals
    cls_name = local_vars.get('self', type('', (), {}))().__class__.__name__ if 'self' in local_vars else ''
    frame_id = id(frame)

    if event == 'call':
        try:
            arg_info = inspect.getargvalues(frame)
            args_info = {arg: local_vars.get(arg, '<?>') for arg in arg_info.args}
        except Exception as e:
            args_info = {'error': str(e)}

        trace_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'Event Type': 'ENTER',
            'Python File': filename.replace(os.sep, '.').replace('.py', ''),
            'Class Name': cls_name,
            'Method Name': func_name,
            'Short Summary': f"{cls_name + '.' if cls_name else ''}{func_name}",
            'Input Type': 'runtime',
            'Input Parameters': str(args_info),
            'Return Type': '',
            'Output Response': '',
            'Error': '',
            'API Path': '',
            'HTTP Method': ''
        }
        trace_map[frame_id] = trace_entry
        write_log(trace_entry)
        return trace_internal_calls

    elif event == 'return':
        if frame_id in trace_map:
            trace_entry = trace_map.pop(frame_id)
            output = safe_serialize(arg)
            trace_entry.update({
                'Event Type': 'EXIT',
                'Output Response': str(output),
                'Return Type': type(arg).__name__
            })
            write_log(trace_entry)
    return
