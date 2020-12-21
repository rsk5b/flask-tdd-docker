# src/tests/test_users.py


import json

from src.api.models import User


def test_add_user(test_app, test_database):

    # given
    test_database.session.query(User).delete()  # delete old data
    client = test_app.test_client()

    # when
    resp = client.post(
        "/users",
        data=json.dumps({"username": "randall", "email": "rsk5b@bogus.com"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())

    # then
    assert resp.status_code == 201
    assert "rsk5b@bogus.com was added!" in data["message"]


def test_add_user_invalid_json(test_app, test_database):

    # given
    test_database.session.query(User).delete()  # delete old data
    client = test_app.test_client()

    # when
    resp = client.post(
        "/users",
        data=json.dumps({}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())

    # then
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_add_user_invalid_json_keys(test_app, test_database):
    # given
    test_database.session.query(User).delete()  # delete old data
    client = test_app.test_client()
    # when
    resp = client.post(
        "/users",
        data=json.dumps({"email": "john@testdriven.io"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    # then
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_add_user_duplicate_email(test_app, test_database):
    client = test_app.test_client()
    client.post(
        "/users",
        data=json.dumps({"username": "michael", "email": "michael@testdriven.io"}),
        content_type="application/json",
    )
    resp = client.post(
        "/users",
        data=json.dumps({"username": "michael", "email": "michael@testdriven.io"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Sorry. That email already exists." in data["message"]


def test_single_user(test_app, test_database, add_user):

    # given
    test_database.session.query(User).delete()  # delete old data
    user = add_user("jeffrey", "jeffrey@testdriven.io")
    client = test_app.test_client()

    # when
    url = f"/users/{user.id}"
    resp = client.get(url)
    data = json.loads(resp.data.decode())

    # then
    assert resp.status_code == 200
    assert "jeffrey" in data["username"]
    assert "jeffrey@testdriven.io" in data["email"]


def test_single_user_incorrect_id(test_app, test_database):
    # given
    client = test_app.test_client()

    # when
    id = 999
    resp = client.get(f"/users/{id}")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert f"User {id} does not exist" in data["message"]


def test_all_users(test_app, test_database, add_user):
    # given
    test_database.session.query(User).delete()  # delete old data
    add_user("michael", "michael@mherman.org")
    add_user("fletcher", "fletcher@notreal.com")
    client = test_app.test_client()

    # when
    resp = client.get("/users")
    data = json.loads(resp.data.decode())

    # then
    assert resp.status_code == 200
    assert len(data) == 2
    assert "michael" in data[0]["username"]
    assert "michael@mherman.org" in data[0]["email"]
    assert "fletcher" in data[1]["username"]
    assert "fletcher@notreal.com" in data[1]["email"]
