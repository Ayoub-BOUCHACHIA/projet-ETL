import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

# def insert_task_by_priority(conn, tuple):
#     """
#     Query tasks by priority
#     :param conn: the Connection object
#     :param priority:
#     :return:
#     """
#     print("inserting ... data : ",tuple)
#     cur = conn.cursor()
#     cur.execute("INSERT INTO data_interaction_dataproducts(id_product,id_category,id_provider,date) values(?,?,?,?)", tuple)
#     conn.commit()
#     return cur.lastrowid

connexion = create_connection('db.sqlite3')

# with open("produits-tous.orig",'r') as data_produits_file:
#     data_produits = data_produits_file.readlines()

# for instance in data_produits:
#     (date, id_product,id_category,id_provider) = instance.split(" ")
    
#     date = date[:4]+'-'+date[4:6]+'-'+date[6:]
#     id_product = int(id_product)
#     id_category = int(id_category)
#     id_provider = int(id_provider.replace('\n',''))
#     insert_task_by_priority(connexion, (id_product,id_category,id_provider, date))


def insert_task_by_vente(conn, tuple):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    print("inserting ... data : ",tuple)
    cur = conn.cursor()
    cur.execute("INSERT INTO data_interaction_accordsvente(date,id_product,id_category,id_provider,id_vente) values(?,?,?,?,?)", tuple)
    conn.commit()
    return cur.lastrowid




with open("pointsDeVente-tous",'r') as data_produits_file:
    data_produits = data_produits_file.readlines()

for instance in data_produits:
    (date, id_product,id_category,id_provider,id_vente) = instance.split(" ")
    
    date = date[:4]+'-'+date[4:6]+'-'+date[6:]
    id_product = int(id_product)
    id_category = int(id_category)
    id_provider = int(id_provider)
    id_vente = int(id_vente.replace('\n',''))
    insert_task_by_vente(connexion, (date, id_product,id_category,id_provider,id_vente))

