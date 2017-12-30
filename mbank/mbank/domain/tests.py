from .entities import Account
from .events import CreateAccountEvent, DepositEvent
from .repository import DomainRepo
import unittest, uuid


class ClientTests(unittest.TestCase):

    def test_create_account(self):
        acc = Account(uuid.uuid4(), '21-123')
        self.assertIsInstance(acc, Account)

    def test_deposit(self):
        acc = Account(uuid.uuid4(), '21-123')
        acc.deposit(100)
        self.assertEqual(100, acc.get_balance())

    def test_withdraw(self):
        acc = Account(uuid.uuid4(), '21-123')
        acc.withdraw(100)
        self.assertEqual(-100, acc.get_balance())

    def test_get_events(self):
        acc = Account(uuid.uuid4(), '21-123')
        acc.deposit(100)

        self.assertEqual(len(acc.get_events()), 2)
        self.assertIsInstance(acc.get_events()[0], CreateAccountEvent)
        self.assertIsInstance(acc.get_events()[1], DepositEvent)

    def test_events_version(self):
        acc = Account(uuid.uuid4(), '21-123')
        acc.deposit(100)
        acc.withdraw(100)

        i = 0

        for e in acc.get_events():
            self.assertEqual(e.get_version(), i)
            i = i + 1


class DomainRepoTests(unittest.TestCase):

    def test_find_all(self):
        acc1 = Account(uuid.uuid4(), '21-123')
        acc2 = Account(uuid.uuid4(), '21-456')
        repo = DomainRepo()
        repo.create(acc1)
        repo.create(acc2)

        result = repo.find_all()
        self.assertEqual(acc1.get_account_number(), result[1].get_account_number())
        self.assertEqual(acc2.get_account_number(), result[2].get_account_number())

    def test_find_by_id(self):
        acc1 = Account(uuid.uuid4(), '21-123')
        # id = acc1.get_uuid()
        repo = DomainRepo()
        repo.create(acc1)

        acc2 = repo.find_by_account_uuid(acc1.get_uuid())
        self.assertEqual(acc1.get_uuid(), acc2.get_uuid())
        self.assertEqual(acc1.get_client_uuid(), acc2.get_client_uuid())
        self.assertEqual(acc1.get_balance(), acc2.get_balance())
        self.assertEqual(len(acc1.get_events()), len(acc2.get_events()))

    def test_create_not_duplicated(self):
        acc1 = Account(uuid.uuid4(), '21-123')
        repo = DomainRepo()
        repo.create(acc1)
        repo.create(acc1)
        self.assertEqual(len(repo.find_all()), 1)

    def test_find_by_client_uuid(self):
        repo = DomainRepo()
        client_uuid = uuid.uuid4()

        acc1 = Account(client_uuid, '21-123')
        acc2 = Account(client_uuid, '21-456')
        repo.create(acc1)
        repo.create(acc2)

        result = repo.find_by_client_uuid(client_uuid)

        self.assertEqual(result[0].get_uuid(), acc1.get_uuid())
        self.assertEqual(result[1].get_uuid(), acc2.get_uuid())


