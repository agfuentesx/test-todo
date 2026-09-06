import pymysql

def lambda_handler(event, context):
    
    # Cambia estos valores por los tuyos
    DB_HOST = 'todo-demo-db.cxwe8u2cw016.us-east-2.rds.amazonaws.com'  # ← TU ENDPOINT
    DB_USER = 'admin'
    DB_PASSWORD = '1525.edu'  # ← TU PASSWORD
    DB_NAME = 'todos'
    
    print(f"Connecting to {DB_HOST}...")
    
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            connect_timeout=10
        )
        
        print("Connected successfully!")
        
        cursor = connection.cursor()
        
        # Crear tabla
        print("Creating table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                completed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        print("Table created!")
        
        # Insertar datos de prueba
        print("Inserting sample data...")
        cursor.execute("""
            INSERT INTO todos (title, description, completed) VALUES
            ('Buy groceries', 'Milk, eggs, bread, and coffee', FALSE),
            ('Finish AWS project', 'Complete Lambda and RDS integration', FALSE),
            ('Read documentation', 'AWS Lambda best practices', TRUE),
            ('Exercise', 'Go for a 30-minute run', FALSE)
        """)
        connection.commit()
        print("Sample data inserted!")
        
        # Verificar
        cursor.execute("SELECT COUNT(*) as count FROM todos")
        result = cursor.fetchone()
        total = result[0]
        
        cursor.execute("SELECT * FROM todos")
        todos = cursor.fetchall()
        
        print(f"Total todos in database: {total}")
        
        return {
            'statusCode': 200,
            'body': f'SUCCESS! Database initialized with {total} todos. Details: {todos}'
        }
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}'
        }
    
    finally:
        if 'connection' in locals():
            connection.close()
            print("Connection closed")