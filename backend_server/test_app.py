import pytest
from app import app, db
import datetime
from models import init_db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
    client = app.test_client()
    yield client
    with app.app_context():
        db.drop_all()

def test_user_registration(client):
    response = client.post('/users/register', json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    assert b"User registered successfully" in response.data

def test_user_login(client):
    client.post('/users/register', json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123"
    })

    response = client.post('/users/login', json={
        "email": "test@example.com",
        "password": "password123"
    })

    assert response.status_code == 200
    assert b"Login successful" in response.data

    response = client.post('/users/login', json={
        "email": "test@example.com",
        "password": "wrongpassword"
    })

    assert response.status_code == 401
    assert b"Invalid credentials" in response.data

def test_subscription_management(client):
    response = client.get('/subscriptions/plans')
    assert response.status_code == 200
    plans = response.get_json()
    assert len(plans) > 0

    client.post('/users/register', json={
        "name": "Subscriber",
        "email": "subscriber@example.com",
        "password": "password123"
    })
    login_response = client.post('/users/login', json={
        "email": "subscriber@example.com",
        "password": "password123"
    })
    user_id = login_response.get_json()["user_id"]

    response = client.post('/subscriptions/subscribe', json={
        "user_id": user_id,
        "plan_type": "Premium",
        "start_date": "2024-01-01"
    })
    assert response.status_code == 201
    assert b"Subscription successful!" in response.data

def test_get_play_history(client):
    client.post('/users/register', json={
        "name": "History User",
        "email": "historyuser@example.com",
        "password": "password123"
    })
    login_response = client.post('/users/login', json={
        "email": "historyuser@example.com",
        "password": "password123"
    })
    user_id = login_response.get_json()["user_id"]

    from models import Song
    with client.application.app_context():
        if not Song.query.get(1):
            db.session.add(Song(SongID=1, Title="Test Song"))
            db.session.commit()

    song_id = 1
    client.post(f'/songs/play/{song_id}', json={"user_id": user_id})

    response = client.get(f'/songs/history/{user_id}')
    assert response.status_code == 200
    history = response.get_json()
    assert len(history) > 0
    assert history[0] == "Test Song"

def test_create_playlist(client):
    client.post('/users/register', json={
        "name": "Playlist User",
        "email": "playlistuser@example.com",
        "password": "password123"
    })
    login_response = client.post('/users/login', json={
        "email": "playlistuser@example.com",
        "password": "password123"
    })
    user_id = login_response.get_json()["user_id"]

    response = client.post('/playlists/', json={
        "user_id": user_id,
        "title": "My Favorite Songs",
        "description": "A collection of my favorite songs"
    })

    assert response.status_code == 201
    response_data = response.get_json()
    assert response_data["message"] == "Playlist created successfully!"
    assert "playlist_id" in response_data

def test_add_song_to_playlist(client):
    client.post('/users/register', json={
        "name": "Playlist User",
        "email": "playlistuser@example.com",
        "password": "password123"
    })
    login_response = client.post('/users/login', json={
        "email": "playlistuser@example.com",
        "password": "password123"
    })
    user_id = login_response.get_json()["user_id"]

    from models import Song
    with client.application.app_context():
        if not Song.query.get(1):
            db.session.add(Song(SongID=1, Title="Test Song"))
            db.session.commit()

    response = client.post('/playlists/', json={
        "user_id": user_id,
        "title": "My Playlist",
        "description": "A test playlist"
    })
    playlist_id = response.get_json()["playlist_id"]
    response = client.post(f'/playlists/{playlist_id}/add-song', json={
        "song_id": 1
    })

    assert response.status_code == 200
    assert response.get_json()["message"] == "Song added to playlist!"

def test_delete_playlist(client):
    client.post('/users/register', json={
        "name": "Playlist User",
        "email": "playlistuser@example.com",
        "password": "password123"
    })
    login_response = client.post('/users/login', json={
        "email": "playlistuser@example.com",
        "password": "password123"
    })
    user_id = login_response.get_json()["user_id"]

    response = client.post('/playlists/', json={
        "user_id": user_id,
        "title": "My Playlist",
        "description": "A test playlist"
    })
    playlist_id = response.get_json()["playlist_id"]

    response = client.delete(f'/playlists/{playlist_id}')
    assert response.status_code == 200
    assert response.get_json()["message"] == "Playlist deleted successfully!"

def test_rate_song(client):
    client.post('/users/register', json={
        "name": "Rater",
        "email": "rater@example.com",
        "password": "password123"
    })
    login_response = client.post('/users/login', json={
        "email": "rater@example.com",
        "password": "password123"
    })
    user_id = login_response.get_json()["user_id"]

    from models import Song
    with client.application.app_context():
        if not Song.query.get(1):
            db.session.add(Song(SongID=1, Title="Test Song"))
            db.session.commit()

    response = client.post('/ratings/1', json={
        "user_id": user_id,
        "rating": 5
    })

    assert response.status_code == 201
    assert response.get_json()["message"] == "Song rated successfully!"

def test_comment_song(client):
    client.post('/users/register', json={
        "name": "Commenter",
        "email": "commenter@example.com",
        "password": "password123"
    })
    login_response = client.post('/users/login', json={
        "email": "commenter@example.com",
        "password": "password123"
    })
    user_id = login_response.get_json()["user_id"]

    from models import Song
    with client.application.app_context():
        if not Song.query.get(1):
            db.session.add(Song(SongID=1, Title="Test Song"))
            db.session.commit()

    response = client.post('/ratings/comments/1', json={
        "user_id": user_id,
        "comment": "Amazing song!"
    })

    assert response.status_code == 201
    assert response.get_json()["message"] == "Comment added successfully!"


