import os
import csv
import ast
import pytest

from app import create_app
from app.services.transaction_service import add_money_by_plsql

app = create_app()

CSV_FILE = os.path.join(os.path.dirname(__file__), "services_transaction_service_add_money_by_plsql.csv")
RESULTS_CSV_FILE = os.path.join(os.path.dirname(__file__), "test_results_add_money_by_plsql.csv")

def load_test_cases():
    test_cases = []
    with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            input_params = ast.literal_eval(row['Input Parameters'])
            expected_output = ast.literal_eval(row['Output Response'])
            test_cases.append((input_params, expected_output))
    return test_cases

def write_test_result(input_params, expected_output, actual_output, status):
    file_exists = os.path.isfile(RESULTS_CSV_FILE)
    with open(RESULTS_CSV_FILE, mode='a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Input Parameters', 'Expected Output', 'Actual Output', 'Status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            'Input Parameters': repr(input_params),
            'Expected Output': repr(expected_output),
            'Actual Output': repr(actual_output),
            'Status': status
        })

@pytest.mark.parametrize("input_params,expected_output", load_test_cases())
def test_add_money_by_plsql(input_params, expected_output):
    with app.app_context():
        try:
            result = add_money_by_plsql(**input_params)
            print("RESULT =========>",result)
            actual_output = result.to_dict()
        except Exception as e:
            actual_output = {'exception': str(e)}
        status = 'PASS' if actual_output == expected_output else 'FAIL'
        write_test_result(input_params, expected_output, actual_output, status)
        assert actual_output == expected_output