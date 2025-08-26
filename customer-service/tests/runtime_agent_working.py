
# import csv
# import os
# import time
# import traceback
# import glob
# import sys
# import inspect
# from datetime import datetime
# from flask import request, g, current_app

# # LOG_FILE = os.path.join(os.path.dirname(__file__), 'CodeTraceCSV', 'runtime_method_logs.csv')

# timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# # LOG_FILE = os.path.join(
# #     os.path.dirname(__file__),
# #     'CodeTraceCSV',
# #     f'runtime_method_logs-{timestamp}.csv'
# # )

# log_dir = os.path.join(os.path.dirname(__file__), 'CodeTraceCSV')

# # Delete all old logs
# for old_log in glob.glob(os.path.join(log_dir, 'runtime_method_logs-*.csv')):
#     os.remove(old_log)

# # Create new timestamped log file
# timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# LOG_FILE = os.path.join(log_dir, f'runtime_method_logs-{timestamp}.csv')
# os.makedirs(log_dir, exist_ok=True)


# os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# # # Backup previous log with timestamp
# # if os.path.exists(LOG_FILE):
# #     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# #     backup_file = LOG_FILE.replace(".csv", f"-{timestamp}.csv")
# #     os.rename(LOG_FILE, backup_file)

# def init_runtime_logger(app):
#     @app.before_request
#     def log_request_info():
#         g.start_time = time.time()
#         g.request_data = request.get_json(silent=True) or request.form.to_dict() or request.args.to_dict()

#         try:
#             view_func = app.view_functions.get(request.endpoint)
#             file_name = view_func.__module__ if view_func else 'unknown'
#             method_name = view_func.__name__ if view_func else 'unknown'
#             qualname = getattr(view_func, '__qualname__', '')
#             class_name = qualname.split('.')[0] if '.' in qualname else ''

#             g.func_info = {
#                 'timestamp': datetime.utcnow().isoformat(),
#                 'Event Type': 'ENTER',
#                 'Python File': file_name,
#                 'Class Name': class_name,
#                 'Method Name': method_name,
#                 'Short Summary': qualname,
#                 'Input Type': 'json/form/args',
#                 'Input Parameters': str(g.request_data),
#                 'Return Type': '',
#                 'Output Response': '',
#                 'Error': '',
#                 'API Path': request.path,
#                 'HTTP Method': request.method
#             }
#             write_log(g.func_info) 
#         except Exception as e:
#             g.func_info = {
#                 'timestamp': datetime.utcnow().isoformat(),
#                 'Python File': 'unknown',
#                 'Class Name': '',
#                 'Method Name': '',
#                 'Short Summary': '',
#                 'Input Type': 'json/form/args',
#                 'Input Parameters': str(g.request_data),
#                 'Return Type': '',
#                 'Output Response': '',
#                 'Error': f"Exception in pre-request: {str(e)}",
#                 'API Path': request.path
#             }

#     @app.after_request
#     def log_response_info(response):
#         try:
            
#             g.func_info.update({
#                 'Return Type': type(response).__name__,
#                 'Output Response': response.get_data(as_text=True),
#             })
#             g.func_info['Event Type'] = 'EXIT'
#             write_log(g.func_info)
#         except Exception as e:
#             print(f"Logging failed in after_request: {e}")
#         return response

#     @app.teardown_request
#     def log_exception_info(exc):
#         if exc:
#             g.func_info.update({
#                 'Error': traceback.format_exc()
#             })
#             write_log(g.func_info)

# def write_log(entry):
#     file_exists = os.path.isfile(LOG_FILE)
#     fieldnames = [
#         'timestamp', 'Event Type', 'Python File', 'Class Name', 'Method Name', 'Short Summary',
#         'Input Type', 'Input Parameters', 'Return Type', 'Output Response', 'Error', 'API Path', 'HTTP Method'
#     ]
#     with open(LOG_FILE, 'a', newline='', encoding='utf-8') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         if not file_exists:
#             writer.writeheader()
#         writer.writerow(entry)



import csv
import os
import time
import traceback
import sys
import inspect
import json
from datetime import datetime
from flask import request, g

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

# Define log directory and ensure it's created
BASE_DIR = os.path.dirname(__file__)
LOG_DIR = os.path.join(BASE_DIR, 'CodeTraceCSV')
os.makedirs(LOG_DIR, exist_ok=True)

# Generate timestamped log file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = os.path.join(LOG_DIR, f'runtime_method_logs-{timestamp}.csv')

# App base path to detect internal project files only
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', 'app'))

# Set up CSV fieldnames
FIELDNAMES = [
    'timestamp', 'Event Type', 'Python File', 'Class Name', 'Method Name', 'Short Summary',
    'Input Type', 'Input Parameters', 'Return Type', 'Output Response', 'Error', 'API Path', 'HTTP Method'
]

def write_log(entry):
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow(entry)

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

            # Enable scoped tracing
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
            sys.settrace(None)  # Disable tracing after request
        return response

    @app.teardown_request
    def log_exception_info(exc):
        if exc:
            g.func_info.update({
                'Error': traceback.format_exc()
            })
            write_log(g.func_info)
            sys.settrace(None)

# def trace_internal_calls(frame, event, arg):
#     if event != 'call':
#         return

#     code = frame.f_code
#     filename = frame.f_globals.get('__file__', '')

#     if not filename or not os.path.abspath(filename).startswith(PROJECT_ROOT):
#         return

#     func_name = code.co_name
#     try:
#         filename = os.path.relpath(filename, PROJECT_ROOT)
#     except ValueError:
#         filename = os.path.abspath(filename)

#     local_vars = frame.f_locals
#     cls_name = local_vars.get('self', type('', (), {}))().__class__.__name__ if 'self' in local_vars else ''

#     try:
#         arg_names = inspect.getfullargspec(frame).args
#         args_info = {arg: local_vars.get(arg, '<?>') for arg in arg_names}
#     except Exception:
#         args_info = {}

#     trace_entry = {
#         'timestamp': datetime.utcnow().isoformat(),
#         'Event Type': 'ENTER',
#         'Python File': filename,
#         'Class Name': cls_name,
#         'Method Name': func_name,
#         'Short Summary': f"{cls_name + '.' if cls_name else ''}{func_name}",
#         'Input Type': 'runtime',
#         'Input Parameters': str(args_info),
#         'Return Type': '',
#         'Output Response': '',
#         'Error': '',
#         'API Path': '',
#         'HTTP Method': ''
#     }
#     write_log(trace_entry)
#     return trace_internal_calls

# Use normal dict with frame IDs
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
            'Python File': filename,
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
        return trace_internal_calls  # Continue tracing nested calls

    # elif event == 'return':
    #     if frame_id in trace_map:
    #         trace_entry = trace_map.pop(frame_id)
    #         trace_entry.update({
    #             'Event Type': 'EXIT',
    #             'Output Response': str(arg),
    #             'Return Type': type(arg).__name__
    #         })
    #         write_log(trace_entry)
    elif event == 'return':
        if frame_id in trace_map:
            trace_entry = trace_map.pop(frame_id)

            # try:
            #     # Try to convert to dict if it has a __dict__ or to_dict method
            #     if hasattr(arg, 'to_dict'):
            #         output = arg.to_dict()
            #     elif hasattr(arg, '__dict__'):
            #         output = vars(arg)
            #     else:
            #         output = str(arg)
            # except Exception as e:
            #     output = f"<Non-serializable: {e}>"
            output = safe_serialize(arg)

            trace_entry.update({
                'Event Type': 'EXIT',
                'Output Response': str(output),
                'Return Type': type(arg).__name__
            })
            write_log(trace_entry)


    return
