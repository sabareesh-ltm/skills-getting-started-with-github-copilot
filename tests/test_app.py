def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert expected_activity in data
    assert data[expected_activity]["schedule"] == "Fridays, 3:30 PM - 5:00 PM"


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "natalie@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    data = response.json()
    all_activities = client.get("/activities").json()

    # Assert
    assert response.status_code == 200
    assert data["message"] == f"Signed up {email} for {activity_name}"
    assert email in all_activities[activity_name]["participants"]


def test_signup_existing_participant_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    data = response.json()

    # Assert
    assert response.status_code == 400
    assert data["detail"] == "Student already signed up"


def test_unregister_from_activity_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})
    data = response.json()
    all_activities = client.get("/activities").json()

    # Assert
    assert response.status_code == 200
    assert data["message"] == f"Removed {email} from {activity_name}"
    assert email not in all_activities[activity_name]["participants"]


def test_unregister_missing_participant_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = "missing@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})
    data = response.json()

    # Assert
    assert response.status_code == 400
    assert data["detail"] == "Participant not found"


def test_root_redirects_to_static_index(client):
    # Arrange

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"
