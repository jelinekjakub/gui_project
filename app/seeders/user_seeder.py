import pymongo
import uuid
from passlib.hash import pbkdf2_sha256
from extensions.db import users_db


users_db.insert_many([
    {
        "_id": uuid.uuid4().hex,
        "name": "test_user",
        "email": "test@test.cz",
        "password": pbkdf2_sha256.encrypt("123456789")
    },
    {
        "_id": uuid.uuid4().hex,
        "name": "Alice Nováková",
        "email": "alice@example.com",
        "password": pbkdf2_sha256.encrypt("securepassword1")
    },
    {
        "_id": uuid.uuid4().hex,
        "name": "Bob Novák",
        "email": "bob@example.com",
        "password": pbkdf2_sha256.encrypt("strongpassword2")
    },
    {
        "_id": uuid.uuid4().hex,
        "name": "Charlie Dvořák",
        "email": "charlie@example.com",
        "password": pbkdf2_sha256.encrypt("safepassword3")
    },
    {
        "_id": uuid.uuid4().hex,
        "name": "David Svoboda",
        "email": "david@example.com",
        "password": pbkdf2_sha256.encrypt("password4")
    },
    {
        "_id": uuid.uuid4().hex,
        "name": "Eva Černá",
        "email": "eva@example.com",
        "password": pbkdf2_sha256.encrypt("secretword5")
    },
])