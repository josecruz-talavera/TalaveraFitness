import pytest
import os

PT_flask = os.environ["PWD"]
import sys

sys.path.insert(0, PT_flask)
from app.starting_app import app

from app.user_functions import create_user, user_exists, delete_users
from app.models import Test_User, db
from user_testing_data import fake


class Test_user_functions:

    def test_create_user(self):
        with app.app_context():
            user = create_user(
                Test_User,
                fake.username_test(),
                fake.email_test(),
                fake.first_name_test(),
                fake.last_name_test(),
                fake.password_test(),
                None,
            )
            assert (
                user.username,
                user.email,
                user.first_name,
                user.last_name,
                user.password,
                user.goal,
                user.level,
            ) == (
                "jcruz6003",
                "jcruz6003@gmail.com",
                "jose",
                "cruz",
                "loka1234",
                None,
                "advanced",
            )

    def test_user_exists(self):
        with app.app_context():
            assert (user_exists(Test_User, fake.username_test())) == (True)
            assert (user_exists(Test_User, "jereo")) == (False)

    def test_delete_users(self):
        with app.app_context():
            assert delete_users(Test_User) == None


#    def test_contact(self):
#        with app.app_context():
#
#            contact_us = contact(
#                Test_contact_us,
#                fake.contact_name_test(),
#                fake.contact_email_test(),
#                fake.contact_message_test(),
#            )
#
#            assert (contact_us.name, contact_us.email, contact_us.message) == (
#                "jeremy",
#                "jeremy6003@gmail.com",
#                "I have a problem",
#            )
#
