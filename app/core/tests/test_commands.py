"""
Test commands for Django 
"""

from unittest.mock import patch # for mocking the database because we need to be simulate when the database return response not.
from psycopg2 import OperationalError as Psycopg2Error # An exception when we might get errors when connecting database

from django.core.management import call_command #Helper function that django to simulate and allowing us actually calling the command 
from django.db.utils import OperationalError # Another exception error that may get thrown from database. and it helps for another control
from django.test import SimpleTestCase 

@patch('core.management.commands.wait_for_db.Command.check') # Bu satırda wait_for_db'yi çekerek Command check atmasını sağlar
class CommandTests(SimpleTestCase):
    def test_for_waiting_database(self,patch_check):
        patch_check.return_value = True

        call_command('wait_for_db')
        patch_check.assert_called_once_with(databases=['default']) #mocklanmış olan check methodunu database default yazdığımız paramtetre ile çağırıp emin oluyoruz
        @patch('time.sleep') #unit test yaparken çok zorlamamak için aslında bu patchleri kullanıyoruz.
        def test_for_waiting_database_delay(self, patch_sleep, patch_check):
            patch_check.side_effect= [Psycopg2Error]* 2 + [OperationalError]* 3 + [True]

            call_command('wait_for_db')

            self.assertEqual(patch_check.call_count, 6)
            patch_check.assert_called_with(databases=['default'])

