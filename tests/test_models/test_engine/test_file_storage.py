#!/usr/bin/python3
"""
Unit Test for FileStorage Class
"""
import unittest
from datetime import datetime
import models
from models.engine.file_storage import FileStorage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8

FileStorage = FileStorage
storage = models.storage
F = './file.json'
storage_type = os.environ.get('HBNB_TYPE_STORAGE')

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


@unittest.skipIf(storage_type == 'db', 'skip if environ is db')
class TestFileStorageDocs(unittest.TestCase):
    """Class for testing FileStorage documentation"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('..... Testing Documentation .....')
        print('..... For FileStorage Class .....')
        print('.................................\n\n')

    def test_doc_file(self):
        """Test documentation for the file_storage.py module"""
        expected = ("\nHandles I/O, writing and reading, of JSON for storage "
                    "of all class instances\n")
        actual = FileStorage.__module__.__doc__
        self.assertEqual(expected, actual)

    def test_doc_class(self):
        """Test documentation for the FileStorage class"""
        expected = 'handles long term storage of all class instances'
        actual = FileStorage.__doc__
        self.assertEqual(expected, actual)

    def test_doc_all(self):
        """Test documentation for all() method"""
        expected = 'returns private attribute: __objects'
        actual = FileStorage.all.__doc__
        self.assertEqual(expected, actual)

    def test_doc_new(self):
        """Test documentation for new() method"""
        expected = ("sets / updates in __objects the obj with key <obj class "
                    "name>.id")
        actual = FileStorage.new.__doc__
        self.assertEqual(expected, actual)

    def test_doc_save(self):
        """Test documentation for save() method"""
        expected = 'serializes __objects to the JSON file (path: __file_path)'
        actual = FileStorage.save.__doc__
        self.assertEqual(expected, actual)

    def test_doc_reload(self):
        """Test documentation for reload() method"""
        expected = ("if file exists, deserializes JSON file to __objects, "
                    "else nothing")
        actual = FileStorage.reload.__doc__
        self.assertEqual(expected, actual)


@unittest.skipIf(storage_type == 'db', 'skip if environ is db')
class TestFileStorage(unittest.TestCase):
    """Testing FileStorage functionality"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('...... Testing FileStorage ......')
        print('..... For FileStorage Class .....')
        print('.................................\n\n')

    def setUp(self):
        """Initializes new FileStorage instance for testing"""
        self.storage = FileStorage()
        self.storage.reload()

    def test_all_returns_dict(self):
        """Test that all() returns the __objects attribute"""
        new_dict = self.storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, self.storage._FileStorage__objects)

    def test_new(self):
        """Test that new() adds an object to __objects"""
        self.storage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                self.storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, self.storage._FileStorage__objects)

    def test_save(self):
        """Test that save() properly saves objects to file.json"""
        self.storage._FileStorage__objects = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            self.storage._FileStorage__objects[instance_key] = instance
        self.storage.save()
        with open(F, "r") as f:
            data = f.read()
        new_dict = {}
        for key, value in self.storage._FileStorage__objects.items():
            new_dict[key] = value.to_dict()
        self.assertEqual(json.loads(data), new_dict)


@unittest.skipIf(storage_type == 'db', 'skip if environ is db')
class TestFileStorageAdditional(unittest.TestCase):
    """Additional tests for FileStorage class"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('...... Additional Testing ......')
        print('..... For FileStorage Class .....')
        print('.................................\n\n')

    def setUp(self):
        """Initializes new FileStorage instance for testing"""
        self.storage = FileStorage()
        self.bm_obj = BaseModel()

    def test_storage_file_exists(self):
        """Test if file.json exists after saving an object"""
        if os.path.exists(F):
            os.remove(F)
        self.bm_obj.save()
        self.assertTrue(os.path.isfile(F))

    def test_obj_saved_to_file(self):
        """Test if an object is saved to file.json"""
        if os.path.exists(F):
            os.remove(F)
        self.bm_obj.save()
        bm_id = self.bm_obj.id
        with open(F, "r") as f:
            storage_dict = json.load(f)
        self.assertTrue(any(bm_id in key for key in storage_dict.keys()))

    def test_reload(self):
        """Test if objects are reloaded correctly"""
        if os.path.exists(F):
            os.remove(F)
        self.bm_obj.save()
        new_storage = FileStorage()
        new_storage.reload()
        all_obj = new_storage.all()
        self.assertIn(self.bm_obj.id, all_obj)

    def test_to_json(self):
        """Test if to_json() method returns a serializable dict"""
        my_model_json = self.bm_obj.to_json()
        self.assertIsInstance(my_model_json, dict)
        try:
            json.dumps(my_model_json)
            result = True
        except:
            result = False
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
