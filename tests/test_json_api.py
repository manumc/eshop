from hypothesis import given, settings
from hypothesis.strategies import dates


def test_json_api(client):
    r = client.get('/api/v1/report?date=2019-08-01')

    js = r.get_json()

    required_keys = [
        "customers",
        "total_discount_amount",
        "items",
        "order_total_avg",
        "discount_rate_avg",
        "commissions",
        # "promotions",
        # "total",
        # "order_average",
    ]

    assert r.status_code == 200
    assert r.headers['Content-Type'] == "application/json"
    assert all([i in js for i in required_keys])

def test_bad_date(client):
    r = client.get('/api/v1/report?date=garbage')

    js = r.get_json()

    assert r.status_code == 400
    assert "Invalid query" == js

def test_bad_parameter(client):
    r = client.get('/api/v1/report?dat')

    js = r.get_json()

    assert r.status_code == 400
    assert "Invalid parameter" == js

def test_empty_date(client):
    r = client.get('/api/v1/report?date=')

    js = r.get_json()

    assert r.status_code == 400
    assert "Invalid query" == js

@given(d=dates())
@settings(max_examples=500)
def test_any_date(d, client):
    r = client.get('/api/v1/report?date={}'.format(str(d)))

    assert r.status_code == 200
    assert r.headers['Content-Type'] == "application/json"
