def test_post_car_returns_201_and_json(client):
    payload={
        "make": "Ford",
        "model": "Fiesta",
        "year": 2018,
        "color": "Black",
    }
    response = client.post("/api/cars", json=payload)
    assert response.status_code == 201
    car=response.json()
    assert car["id"]>0
    assert car["make"]=="Ford"
    assert car["model"]=="Fiesta"
    assert response.headers["Location"]==f"/api/cars/{car['id']}"
def test_invalid_year_is_not_saved(client):
    post=client.post("/api/cars", json={
        "make": "Honda",
        "model": "Civic",
        "year": 1800
    })
    assert post.status_code==422
    get_resp=client.get("/api/cars")
    assert get_resp.json()==[]