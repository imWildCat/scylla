def _create_db_file():
    from scylla.database import create_connection, create_db_tables
    create_connection()
    create_db_tables()


def _delete_db_file():
    import os
    os.remove('scylla.db')


def pytest_sessionstart(session):
    """ before session.main() is called. """
    _create_db_file()
    print("\n ===setup=== \n")


def pytest_sessionfinish(session, exitstatus):
    """ whole test run finishes. """
    _delete_db_file()
