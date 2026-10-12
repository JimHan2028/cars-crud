from app import database
from app.schemas import CarInput

def test_saved_car_can_be_read_from_sqlite(database_path):
    database.initialize(database_path)
    saved=database.create_car(
        database_path,
        CarInput(make="Toyota", model="Yaris", year=2020, color="Blue"),
    )
    loaded=database.get_car(database_path,saved.id)

    assert loaded is not None
    assert loaded.id==saved.id
    assert loaded.make == "Toyota"
    assert loaded.year == 2020

def test_deleting_one_car_keeps_the_other(database_path):
    database.initialize(database_path)
    car1_input = CarInput(make="Toyota", model="Yaris", year=2020)
    car1 = database.create_car(database_path, car1_input)

    car2_input = CarInput(make="Honda", model="Civic", year=2021)
    car2 = database.create_car(database_path, car2_input)

    database.delete_car(database_path, car1.id)

    loaded1=database.get_car(database_path, car1.id)
    assert loaded1 is None

    loaded2=database.get_car(database_path, car2.id)
    assert loaded2 is not None
    assert loaded2.id == car2.id

    all_cars=database.list_cars(database_path)
    assert len(all_cars)==1
    assert all_cars[0].id==car2.id

