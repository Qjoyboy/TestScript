
import json
import pytest
from src.src import Src
from utils.utils import Utils


def test_normalize_keys():
    utils = Utils()
    input_data = {
        "Hourly_Rate": "50",
        "Name": "Alice",
        "Email": "alice@example.com",
        "Rate": "40",
        "payout": "5000",
        "hours_worked": "160",
    }

    expected_data = {
        "name": "Alice",
        "email": "alice@example.com",
        "rate": "40",
        "payout": "5000",
        "hours_worked": "160",
    }

    res = utils.normalize_keys(input_data)
    assert res == expected_data


def test_add_new_key():
    data = [
        {"hours_worked": "160", "rate": "50"},
        {"hours_worked": "150", "rate": "40"},
        {"hours_worked": "170", "rate": "60"},
    ]

    Utils.add_new_key(data)

    assert data[0]["payout"] == 8000
    assert data[1]["payout"] == 6000
    assert data[2]["payout"] == 10200

def test_sorted_data():
    unsorted = [
        {"id": "2", "department": "Sales", "name": "Karen"},
        {"id": "1", "department": "HR", "name": "Alice"},
        {"id": "3", "department": "Marketing", "name": "Bob"}
    ]

    expected = [
        {"id": "1", "department": "HR", "name": "Alice"},
        {"id": "3", "department": "Marketing", "name": "Bob"},
        {"id": "2", "department": "Sales", "name": "Karen"}
    ]

    res = Src.sorted_data(unsorted)

    assert res == expected
def test_beauty_view(capsys):
    data = [
        {
            "id": "1",
            "name": "Alice",
            "email": "alice@example.com",
            "hours_worked": "160",
            "rate": "50",
            "payout": 8000,
            "department": "HR"
        },
        {
            "id": "2",
            "name": "Bob",
            "email": "bob@example.com",
            "hours_worked": "150",
            "rate": "40",
            "payout": 6000,
            "department": "HR"
        },
        {
            "id": "3",
            "name": "Carol",
            "email": "carol@example.com",
            "hours_worked": "170",
            "rate": "60",
            "payout": 10200,
            "department": "Design"
        }
    ]

    Src.beauty_view(data)

    captured = capsys.readouterr()
    output = captured.out

    assert "--------HR--------" in output
    assert "--------Design--------" in output
    assert "Alice" in output
    assert "Carol" in output
    assert "bob@example.com" in output
    assert "payout" in output

def test_get_data(tmp_path):

    content = (
        "id,name,email,hours_worked,rate,department\n"
        "1,Alice,alice@example.com,160,50,HR\n"
        "2,Bob,bob@example.com,150,40,HR\n"
    )
    test_file = tmp_path / "test.csv"
    test_file.write_text(content, encoding='utf-8')

    utils = Utils()
    result = utils.get_data(str(test_file))

    expected = [
        {
            "id": "1",
            "name": "Alice",
            "email": "alice@example.com",
            "hours_worked": "160",
            "rate": "50",
            "department": "HR",
            "payout": 8000,
        },
        {
            "id": "2",
            "name": "Bob",
            "email": "bob@example.com",
            "hours_worked": "150",
            "rate": "40",
            "department": "HR",
            "payout": 6000,
        },
    ]

    assert result == expected

class MockArgs:
    def __init__(self):
        self.report = 'test_report'
        self.files = ['file1.csv']


@pytest.fixture
def mock_args():
    return MockArgs()


"""Тест для метода get_files"""
# помогите
def test_get_files(mock_args, mocker, monkeypatch):
    monkeypatch.setattr('sys.argv', ['script.py', '--report', 'json', 'file1.csv', 'file2.csv'])

    mock_data = [{'id': '1', 'name': 'Alice', 'department': 'HR'}]
    mock_get_data = mocker.patch.object(Utils, 'get_data', return_value=mock_data)

    src = Src()

    result = src.get_files()

    assert mock_get_data.call_count == 2

    assert result == mock_data * 2

"""ТЕСТ ДЛЯ ФУНКЦИИ report_creator_json"""
# Данный код слишком замудрен, поэтому добавил коменты чтоб не забыть что я тут написал
def test_report_creator_json(mock_args, mocker, monkeypatch):
    data = [
        {"id": "1", "name": "Alice", "email": "alice@example.com", "hours_worked": "160", "rate": "50", "payout": "8000", "department": "HR"},
        {"id": "2", "name": "Bob", "email": "bob@example.com", "hours_worked": "150", "rate": "40", "payout": "6000", "department": "HR"},
        {"id": "3", "name": "Charlie", "email": "charlie@example.com", "hours_worked": "170", "rate": "60", "payout": "10200", "department": "Engineering"}
    ]

    monkeypatch.setattr('sys.argv', ['pytest', '--report', 'test_report', 'test_file.csv'])

    src = Src()

    mock_open = mocker.patch("builtins.open", mocker.mock_open())

    src.report_creator_json(data)

    mock_open.assert_called_with("report_test_report.json", 'w', encoding='utf-8')

    handle = mock_open()
    write_calls = handle.write.call_args_list

    written_data = ''.join([call[0][0] for call in write_calls])

    written_json = json.loads(written_data)

    expected_data = {
        "HR": [
            {"id": "1", "name": "Alice", "email": "alice@example.com", "hours_worked": "160", "rate": "50",
             "payout": "8000", "department": "HR"},
            {"id": "2", "name": "Bob", "email": "bob@example.com", "hours_worked": "150", "rate": "40",
             "payout": "6000", "department": "HR"}
        ],
        "Engineering": [
            {"id": "3", "name": "Charlie", "email": "charlie@example.com", "hours_worked": "170", "rate": "60",
             "payout": "10200", "department": "Engineering"}
        ]
    }

    assert written_json == expected_data
