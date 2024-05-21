from configuration_manager import ConfigurationManager
from database_connection_pool import DBConnectionPool
from print_spooler import PrintSpooler


if __name__ == '__main__':

    match i:=input("Choose an option: \n1."
                   " Configuration Manager \n2."
                   " Database Connection Pool \n3."
                   " Print Spooler \n"
                   "Your choice: "):
        case '1':
            config_manager = ConfigurationManager()
            config_manager.create_config()
            config_manager.add('Section4', 'Key1', 'Value1')
            config_manager.add('Section5', 'Key3', 'Value3')
            config_manager.add('Section6', 'Key3', 'Value3')
            config_manager.update('Section6', 'Key6', 'Value6')
            config_manager.delete('Section1')
            config_manager.read_all()
        case '2':
            # Get the instance of the connection pool
            connection_pool = DBConnectionPool()

            # Get a connection from the pool
            connection = connection_pool.get_connection()

            # Use the connection for database operations
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM example")
            rows = cursor.fetchall()
            for row in rows:
                print(row)

            # Release the connection back to the pool
            connection_pool.release_connection(connection)

            # Close all connections when shutting down the application
            connection_pool.close_all_connections()
        case '3':
            spooler = PrintSpooler()
            spooler.add_to_queue("Print job 1")  # Low priority
            spooler.add_to_queue("Print job 2", 1)  # High priority
            spooler.process_queue()
        case _:
            print(i)

