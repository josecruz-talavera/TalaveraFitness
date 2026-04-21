from faker import Faker

fake = Faker()

from faker.providers import BaseProvider


class User_data(BaseProvider):

    def username_test(self):
        return "jcruz6003"

    def first_name_test(self):
        return "jose"

    def last_name_test(self):
        return "cruz"

    def email_test(self):
        return "jcruz6003@gmail.com"

    def password_test(self):
        return "loka1234"

    def level_test(self):
        return "advanced"


class Contact_us_data(BaseProvider):

    def contact_name_test(self):
        return "jeremy"

    def contact_email_test(self):
        return "jeremy6003@gmail.com"

    def contact_message_test(self):
        return "I have a problem"


fake.add_provider(User_data)
