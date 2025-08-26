import os
import csv
import ast
import pytest

from app import create_app
from app.services.transaction_service import pay_bill_by_plsql

app = create_app()

# Paths
BASE_DIR = os.path.dirname(__file__)
INPUT_CSV = os.path.join(BASE_DIR, "services_transaction_service_pay_bill_by_plsql.csv")
RESULTS_CSV = os.path.join(BASE_DIR, "test_results_pay_bill_by_plsql.csv")

# Read test cases from CSV
def load_test_cases():
    test_cases = []
    with open(INPUT_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            input_params = ast.literal_eval(row['Input Parameters'])
            expected_output = ast.literal_eval(row['Output Response'])
            test_cases.append((input_params, expected_output))
    return test_cases

# Prepare test cases for parameterization
test_cases = load_test_cases()

# Ensure results CSV has header
def ensure_results_csv_header():
    if not os.path.exists(RESULTS_CSV) or os.path.getsize(RESULTS_CSV) == 0:
        with open(RESULTS_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Input Parameters',
                'Expected Output',
                'Actual Output',
                'Result'
            ])

ensure_results_csv_header()

@pytest.mark.parametrize("input_params,expected_output", test_cases)
def test_pay_bill_by_plsql(input_params, expected_output):
    with app.app_context():
        try:
            result_obj = pay_bill_by_plsql(**input_params)
            print("RESULT =========>",result_obj)
            actual_output = result_obj.to_dict()
        except Exception as e:
            actual_output = {'exception': str(e)}

        passed = actual_output == expected_output
        result_str = 'PASS' if passed else 'FAIL'

        # Log to results CSV
        with open(RESULTS_CSV, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                repr(input_params),
                repr(expected_output),
                repr(actual_output),
                result_str
            ])

        assert passed, f"Input: {input_params}\nExpected: {expected_output}\nActual: {actual_output}"