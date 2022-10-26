from generate_table import initialize_db
from generate_table.lawyers import generate_lawyers, drop_lawyers

def generate_table():
    ddb = initialize_db()
    generate_lawyers(ddb)

def drop_table():
    ddb = initialize_db()
    drop_lawyers(ddb)

if __name__ == '__main__':
    generate_table()
