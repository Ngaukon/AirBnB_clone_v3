#!/usr/bin/python3
"""
Unit Test for DBStorage Class
"""
import unittest
from datetime import datetime
from models import *
import os
from models.base_model import Base
from models.engine.db_storage import DBStorage

storage_type = os.environ.get('HBNB_TYPE_STORAGE')
storage = DBStorage()

@unittest.skipIf(storage_type != 'db', 'skip if environ is not db')
class TestDBStorageDocs(unittest.TestCase):
    """Class for testing documentation in DBStorage"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('..... Testing Documentation .....')
        print('..... For DBStorage Class .....')
        print('.................................\n\n')

    def test_doc_file(self):
        """Test documentation for the file"""
        expected = ' Database engine '
        actual = DBStorage.__doc__
        self.assertEqual(expected, actual)

    def test_doc_class(self):
        """Test documentation for DBStorage class"""
        expected = 'handles long term storage of all class instances'
        actual = DBStorage.__doc__
        self.assertEqual(expected, actual)

    def test_doc_all(self):
        """Test documentation for all method"""
        expected = ' returns a dictionary of all objects '
        actual = DBStorage.all.__doc__
        self.assertEqual(expected, actual)

    def test_doc_new(self):
        """Test documentation for new method"""
        expected = ' adds objects to current database session '
        actual = DBStorage.new.__doc__
        self.assertEqual(expected, actual)

    def test_doc_save(self):
        """Test documentation for save method"""
        expected = ' commits all changes of current database session '
        actual = DBStorage.save.__doc__
        self.assertEqual(expected, actual)

    def test_doc_reload(self):
        """Test documentation for reload method"""
        expected = ' creates all tables in database & session from engine '
        actual = DBStorage.reload.__doc__
        self.assertEqual(expected, actual)

    def test_doc_delete(self):
        """Test documentation for delete method"""
        expected = ' deletes obj from current database session if not None '
        actual = DBStorage.delete.__doc__
        self.assertEqual(expected, actual)

@unittest.skipIf(storage_type != 'db', 'skip if environ is not db')
class TestStateDBInstances(unittest.TestCase):
    """Test the State class instances in DBStorage"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('......... Testing DBStorage ........')
        print('.......... State  Class ..........')
        print('.................................\n\n')

    def setUp(self):
        """Initializes a new State object for testing"""
        self.state = State(name="California")
        self.state.save()

    def test_state_all(self):
        """Test if all() returns newly created State instance"""
        all_objs = storage.all()
        all_state_objs = storage.all('State')

        exist_in_all = any(self.state.id in k for k in all_objs.keys())
        exist_in_all_states = any(self.state.id in k for k in all_state_objs.keys())

        self.assertTrue(exist_in_all)
        self.assertTrue(exist_in_all_states)

    def test_state_delete(self):
        """Test if delete() removes State instance"""
        state_id = self.state.id
        storage.delete(self.state)
        storage.save()
        exist_in_all = any(state_id in k for k in storage.all().keys())
        self.assertFalse(exist_in_all)

@unittest.skipIf(storage_type != 'db', 'skip if environ is not db')
class TestUserDBInstances(unittest.TestCase):
    """Test the User class instances in DBStorage"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('......... Testing DBStorage ........')
        print('.......... User  Class ..........')
        print('.................................\n\n')

    def setUp(self):
        """Initializes a new User object for testing"""
        self.user = User(email='test@example.com', password='testpassword')
        self.user.save()

    def test_user_all(self):
        """Test if all() returns newly created User instance"""
        all_objs = storage.all()
        all_user_objs = storage.all('User')

        exist_in_all = any(self.user.id in k for k in all_objs.keys())
        exist_in_all_users = any(self.user.id in k for k in all_user_objs.keys())

        self.assertTrue(exist_in_all)
        self.assertTrue(exist_in_all_users)

    def test_user_delete(self):
        """Test if delete() removes User instance"""
        user_id = self.user.id
        storage.delete(self.user)
        storage.save()
        exist_in_all = any(user_id in k for k in storage.all().keys())
        self.assertFalse(exist_in_all)

@unittest.skipIf(storage_type != 'db', 'skip if environ is not db')
class TestCityDBInstances(unittest.TestCase):
    """Test the City class instances in DBStorage"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('......... Testing DBStorage ........')
        print('.......... City  Class ..........')
        print('.................................\n\n')

    def setUp(self):
        """Initializes a new City object for testing"""
        self.state = State(name="California")
        self.state.save()
        self.city = City(name="Fremont", state_id=self.state.id)
        self.city.save()

    def test_city_all(self):
        """Test if all() returns newly created City instance"""
        all_objs = storage.all()
        all_city_objs = storage.all('City')

        exist_in_all = any(self.city.id in k for k in all_objs.keys())
        exist_in_all_city = any(self.city.id in k for k in all_city_objs.keys())

        self.assertTrue(exist_in_all)
        self.assertTrue(exist_in_all_city)

@unittest.skipIf(storage_type != 'db', 'skip if environ is not db')
class TestPlaceDBInstances(unittest.TestCase):
    """Test the Place class instances in DBStorage"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('......... Testing DBStorage ........')
        print('.......... Place  Class ..........')
        print('.................................\n\n')

    def setUp(self):
        """Initializes a new Place object for testing"""
        self.user = User(email='test@example.com', password='testpassword')
        self.user.save()
        self.state = State(name="California")
        self.state.save()
        self.city = City(name="San Mateo", state_id=self.state.id)
        self.city.save()
        self.place = Place(city_id=self.city.id, user_id=self.user.id,
                           name='test_place', description='test_description',
                           number_rooms=2, number_bathrooms=1, max_guest=4,
                           price_by_night=100, latitude=120.12, longitude=101.4)
        self.place.save()

    def test_place_all(self):
        """Test if all() returns newly created Place instance"""
        all_objs = storage.all()
        all_place_objs = storage.all('Place')

        exist_in_all = any(self.place.id in k for k in all_objs.keys())
        exist_in_all_place = any(self.place.id in k for k in all_place_objs.keys())

        self.assertTrue(exist_in_all)
        self.assertTrue(exist_in_all_place)

@unittest.skipIf(storage_type != 'db', 'skip if environ is not db')
class TestStorageGet(unittest.TestCase):
    """Test the get() method in DBStorage"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('...... Testing Get() Method ......')
        print('.......... State  Class ..........')
        print('.................................\n\n')

    def setUp(self):
        """Initializes a State object for testing"""
        self.state = State(name="Florida")
        self.state.save()

    def test_get_method_obj(self):
        """Test get() method returns an object"""
        result = storage.get(cls="State", id=self.state.id)
        self.assertIsInstance(result, State)

    def test_get_method_return(self):
        """Test get() method returns the correct object"""
        result = storage.get(cls="State", id=str(self.state.id))
        self.assertEqual(self.state.id, result.id)

    def test_get_method_none(self):
        """Test get() method returns None for non-existent object"""
        result = storage.get(cls="State", id="doesnotexist")
        self.assertIsNone(result)

@unittest.skipIf(storage_type != 'db', 'skip if environ is not db')
class TestStorageCount(unittest.TestCase):
    """Test the count() method in DBStorage"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('...... Testing Count() Method ......')
        print('.......... State  Class ..........')
        print('.................................\n\n')

    def setUp(self):
        """Initializes multiple State objects for testing count"""
        self.state1 = State(name="California")
        self.state1.save()
        self.state2 = State(name="Colorado")
        self.state2.save()
        self.state3 = State(name="Wyoming")
        self.state3.save()
        self.state4 = State(name="Virginia")
        self.state4.save()
        self.state5 = State(name="Oregon")
        self.state5.save()
        self.state6 = State(name="New York")
        self.state6.save()
        self.state7 = State(name="Ohio")
        self.state7.save()

    def test_count_all(self):
        """Test counting all instances"""
        result = storage.count()
        self.assertEqual(len(storage.all()), result)

    def test_count_state(self):
        """Test counting State instances"""
        result = storage.count(cls="State")
        self.assertEqual(len(storage.all("State")), result)

    def test_count_city(self):
        """Test counting City instances"""
        result = storage.count(cls="City")
        self.assertEqual(len(storage.all("City")), result)

if __name__ == '__main__':
    unittest.main()

