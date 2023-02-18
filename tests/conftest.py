import pytest

@pytest.fixture()
def dummy_shopee_account():
    dummy_acct = {"username": "testusername",
                  "password": "testpassword",
                  "app": "shopeepy-wrapped"}

    return dummy_acct

@pytest.fixture()
def dummy_shopee_account_wrong_type():
    dummy_acct = {"username": 123,
                  "password": "test-password",
                  "app": "shopeepy-wrapped"}

    return dummy_acct
