import mysql.connector
from mysql.connector import Error
import config
import threading


def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host=config.HOST,
            database=config.DATABASE,
            user=config.USER,
            password=config.PASSWORD
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def join_or_create_group(connection, group_name):
    cursor = connection.cursor()
    
    try:
        # Start a transaction
        connection.start_transaction()
        
        # Insert group with ON DUPLICATE KEY UPDATE to handle concurrent inserts
        insert_query = """
        INSERT INTO `group` (name)
        VALUES (%s)
        ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id)
        """
        cursor.execute(insert_query, (group_name,))
        
        # Get the group ID
        group_id = cursor.lastrowid
        
        # Commit the transaction
        connection.commit()
        
        print(f"Group '{group_name}' has ID {group_id}.")
    except Error as e:
        connection.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()
        
    return group_id

def join_group_thread(group_name):
    connection = connect_to_database()
    if connection:
        join_or_create_group(connection, group_name)
        connection.close()
        
def main():
    group_name = input("Enter the group name to join: ")
    
    threads = []
    for i in range(10):  # Create 10 threads to simulate 10 concurrent users
        thread = threading.Thread(target=join_group_thread, args=(group_name+str(i%2),))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
