import pyodbc
import toml
import streamlit as st

def save_secrets_to_toml(secrets_list, filename="secrets.toml"):
    try:
        # Save the list of secrets to the specified file
        with open(filename, "w") as toml_file:
            toml.dump({"secrets": secrets_list}, toml_file)
        st.success("Secrets saved successfully!")
    except Exception as e:
        st.error(f"Error: Unable to save secrets. {e}")

def load_existing_secrets(filename="secrets.toml"):
    try:
        # Load existing secrets from the specified file
        with open(filename, "r") as toml_file:
            secrets_data = toml.load(toml_file)
            return secrets_data.get("secrets", [])
    except FileNotFoundError:
        return []



def get_database_connection(secrets):
    try:
        # Construct the SQL Server connection string
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={secrets['server']};"
            f"DATABASE={secrets['database']};"
            f"UID={secrets['username']};"
            f"PWD={secrets['password']};"
        )

        # Establish a connection to the SQL Server database using pyodbc
        connection = pyodbc.connect(connection_string)
        return connection
    except Exception as e:
        st.error(f"Error: Unable to connect to the database. {e}")
        st.stop()

def test_database_connection(server,database,username,password):
    try:
        # Construct the SQL Server connection string
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
        )

        # Establish a connection to the SQL Server database using pyodbc
        connection = pyodbc.connect(connection_string)
        st.success("connection was successful")
        st.balloons()
        return True
    except Exception as e:
        st.error(f"Error: Unable to connect to the database. {e}")
        st.stop()        