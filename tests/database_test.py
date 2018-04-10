from scylla.database import create_connection, create_db_tables, ProxyIP


def test_create_connection():
    db = create_connection()
    print(db)


def test_create_db_tables():
    create_db_tables()


def test_create_ip():
    ip = ProxyIP(ip='127.0.0.1', port=3306, latency=200.00, stability=100.0)
    ip.save()

    count = ProxyIP.select().count()
    assert count >= 1


def test_delete_ip():
    ret = ProxyIP.delete().execute()
    print(ret)
