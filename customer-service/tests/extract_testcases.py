# import csv
# import os
# from datetime import datetime
# from collections import defaultdict

# # ========= Main Function =========
# def extract_testcases(trace_path, mapping_path, output_dir):
#     if not os.path.isfile(trace_path):
#         print(f"❌ Trace file not found: {trace_path}")
#         return

#     if not os.path.isfile(mapping_path):
#         print(f"❌ Mapping file not found: {mapping_path}")
#         return

#     with open(mapping_path, 'r', newline='', encoding='utf-8-sig') as f:
#         reader = csv.DictReader(f)
#         rows = list(reader)
#         print(f"[DEBUG] Loaded {len(rows)} rows from mapping file.")
#         mapping = set(
#             (row['Python File'].strip(), row['Method Name'].strip())
#             for row in rows
#             if row.get('Python File') and row.get('Method Name')
#         )

#     with open(trace_path, 'r', newline='', encoding='utf-8') as f:
#         reader = csv.DictReader(f)
#         rows = list(reader)

#     grouped = defaultdict(list)
#     seen = set()

#     for row in rows:
#         if row['Event Type'].strip().upper() != 'EXIT':
#             continue

#         file_key = row['Python File'].strip()
#         method_key = row['Method Name'].strip()

#         if (file_key, method_key) in mapping and (file_key, method_key) not in seen:
#             grouped[(file_key, method_key)].append(row)
#             seen.add((file_key, method_key))

#     if grouped:
#         os.makedirs(output_dir, exist_ok=True)
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

#         # Write master file
#         method_log_path = os.path.join(output_dir, f"method_log_plsql-{timestamp}.csv")
#         with open(method_log_path, 'w', newline='', encoding='utf-8') as f:
#             writer = csv.DictWriter(f, fieldnames=rows[0].keys())
#             writer.writeheader()
#             for group_rows in grouped.values():
#                 writer.writerows(group_rows)
#         print(f"✅ Extracted {sum(len(v) for v in grouped.values())} matching EXIT rows to {method_log_path}")

#         # Write per-method files
#         method_dir = os.path.join(output_dir, 'MethodCSV')
#         os.makedirs(method_dir, exist_ok=True)

#         for (py_file, method), group_rows in grouped.items():
#             safe_name = f"{py_file.replace('.', '_')}_{method}.csv"
#             method_file_path = os.path.join(method_dir, safe_name)
#             with open(method_file_path, 'w', newline='', encoding='utf-8') as f:
#                 writer = csv.DictWriter(f, fieldnames=group_rows[0].keys())
#                 writer.writeheader()
#                 writer.writerows(group_rows)
#             print(f"📁 Wrote {len(group_rows)} row(s) to {method_file_path}")

#     else:
#         print("⚠️ No matching EXIT rows found in trace file.")

# # ========= Auto-locate latest trace file =========
# def get_latest_trace_file(directory):
#     files = [f for f in os.listdir(directory) if f.startswith('runtime_method_logs-') and f.endswith('.csv')]
#     files.sort(reverse=True)
#     return os.path.join(directory, files[0]) if files else None

# if __name__ == '__main__':
#     BASE_DIR = os.path.dirname(__file__)
#     OUTPUT_DIR = os.path.join(BASE_DIR, 'CodeTraceCSV')
#     MAPPING_FILE = os.path.join(BASE_DIR, 'flask-agent-classes.csv')
#     TRACE_FILE = get_latest_trace_file(OUTPUT_DIR)

#     if TRACE_FILE:
#         extract_testcases(TRACE_FILE, MAPPING_FILE, OUTPUT_DIR)
#     else:
#         print("❌ No trace file found to process.")


import csv
import os
from datetime import datetime
from collections import defaultdict

# ========= Main Function =========
def extract_testcases(trace_path, mapping_path, output_dir):
    if not os.path.isfile(trace_path):
        print(f"❌ Trace file not found: {trace_path}")
        return

    if not os.path.isfile(mapping_path):
        print(f"❌ Mapping file not found: {mapping_path}")
        return

    with open(mapping_path, 'r', newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        print(f"[DEBUG] Loaded {len(rows)} rows from mapping file.")
        mapping = set(
            (row['Python File'].strip(), row['Method Name'].strip())
            for row in rows
            if row.get('Python File') and row.get('Method Name')
        )

    with open(trace_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    grouped = defaultdict(list)
    seen = set()

    for row in rows:
        if row['Event Type'].strip().upper() != 'EXIT':
            continue

        file_key = row['Python File'].strip()
        method_key = row['Method Name'].strip()

        if (file_key, method_key) in mapping and (file_key, method_key) not in seen:
            grouped[(file_key, method_key)].append(row)
            seen.add((file_key, method_key))

    if grouped:
        method_dir = os.path.join(output_dir, 'MethodCSV')
        os.makedirs(method_dir, exist_ok=True)

        for (py_file, method), group_rows in grouped.items():
            safe_name = f"{py_file.replace('.', '_')}_{method}.csv"
            method_file_path = os.path.join(method_dir, safe_name)
            with open(method_file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=group_rows[0].keys())
                writer.writeheader()
                writer.writerows(group_rows)
            print(f"📁 Wrote {len(group_rows)} row(s) to {method_file_path}")

    else:
        print("⚠️ No matching EXIT rows found in trace file.")

# ========= Auto-locate latest trace file =========
def get_latest_trace_file(directory):
    files = [f for f in os.listdir(directory) if f.startswith('runtime_method_logs-') and f.endswith('.csv')]
    files.sort(reverse=True)
    return os.path.join(directory, files[0]) if files else None

if __name__ == '__main__':
    BASE_DIR = os.path.dirname(__file__)
    OUTPUT_DIR = os.path.join(BASE_DIR, 'CodeTraceCSV')
    MAPPING_FILE = os.path.join(BASE_DIR, 'flask-agent-classes.csv')
    TRACE_FILE = get_latest_trace_file(OUTPUT_DIR)

    if TRACE_FILE:
        extract_testcases(TRACE_FILE, MAPPING_FILE, OUTPUT_DIR)
    else:
        print("❌ No trace file found to process.")
