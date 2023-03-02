import json
import requests as client

def test_create_user(client):
    response = client.post('/users', json={
        'email': 'jane@example.com',
        'password': 'password'
    })
    assert response.status_code == 201
    assert 'access_token' in response.json

def test_create_post(client, access_token):
    response = client.post('/posts', headers={
        'Authorization': f'Bearer {access_token}'
    }, json={
        'title': 'My First Post',
        'content': 'Hello, World!',
        'user_id': 1
    })
    assert response.status_code == 201
    assert response.json['title'] == 'My First Post'
    assert response.json['content'] == 'Hello, World!'
    assert response.json['user_id'] == 1

def test_like_post(client, access_token):
    response = client.post('/posts/1/like', headers={
        'Authorization': f'Bearer {access_token}'
    })
    assert response.status_code == 200
    assert response.json['likes'] == 1

def test_get_all_posts(client):
    response = client.get('/posts')
    assert response.status_code == 200
    assert len(response.json) == 1

def test_delete_post(client, access_token):
    response = client.delete('/posts/1', headers={
        'Authorization': f'Bearer {access_token}'
    })
    assert response.status_code == 204
