
import streamlit as st
import pandas as pd
import bcrypt
from authenticationtoml import *
from ssc import * 
import extra_streamlit_components as stx

def hash_password(password):
    # Hash the password using bcrypt
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def main():
    
    if check_password():
        
        if stx.CookieManager().get('user_role') == "Admin":
            choice = st.sidebar.radio(
            label="Options",
            options=["setting","ETL","Modeling"])   
            if choice == "setting":

                        tab1, tab2, tab3 = st.tabs(["add connection", "add user", "connections"])
                        with tab1 :
                            st.title("Database Configuration and Secrets")

                            # Load existing secrets and users
                            existing_secrets = load_existing_secrets()
                            

                            # Display existing connections
                            st.write("### Existing Database Connections:")
                            
                            # Get the SQL Server connection details from the user
                            server = st.text_input("Enter SQL Server address:")
                            database = st.text_input("Enter database name:")
                            username = st.text_input("Enter database username:")
                            password = st.text_input("Enter database password:", type="password")
                            if st.button("test conection"):
                                   test_database_connection(server,database,username,password)
                                       
                            # Save secrets to toml file on button click
                                   
                            if st.button("Save Secrets"):
                                        if test_database_connection(server,database,username,password):
                                            secrets = {
                                                "server": server,
                                                "database": database,
                                                "username": username,
                                                "password": password
                                            }
                                            existing_secrets.append(secrets)
                                            save_secrets_to_toml(existing_secrets)
                                        else:
                                             st.warning("No Connection")    
                                

                            # register user information
                        with tab2:        
                            st.write("### Existing Users:")
                            existing_users = load_existing_users()
                            new_username = st.text_input("Enter new username:")
                            email = st.text_input("email")
                            new_password = st.text_input("Enter new password:", type="password")
                            new_role = st.selectbox(label="Choice a role",options=["Admin","User"])

                            # Save users to toml file on button click
                            if st.button("Save Users"):
                                save_credentials(new_username,new_password,email,new_role)
                        with tab3:
                            # Connect to the database using saved secrets
                            if existing_secrets:
                                selected_database = st.selectbox("Select a database:", [secrets['database'] for secrets in existing_secrets])
                            
                                # Find the selected secrets based on the database name
                                selected_secrets = next((secrets for secrets in existing_secrets if secrets['database'] == selected_database), None)

                                if selected_secrets:
                                    connection = get_database_connection(selected_secrets)

                                    # Example: Fetch data from a table and display it
                                    query = f"""
                                    
                                    select name from sys.tables
                                    order by name
                                    """
                                    try:
                                        # Execute the query and fetch the results
                                        cursor = connection.cursor()
                                        cursor.execute(query)
                                        results = cursor.fetchall()

                                        # Process the results as needed
                                    
                                        st.write("### tables Data from the Database:")
                                        selected_table = st.selectbox("Select a Table:", [table[0] for table in results])
                                        if selected_table:
                                            selected_table_function = st.selectbox("Select:", ["datatype","show top 10"])
                                            if selected_table_function == "show top 10": 
                                                table_query = f"select top 10 * from {selected_table}"
                                                df = pd.read_sql(table_query, connection)
                                                st.dataframe(df,hide_index=True)
                                            if selected_table_function == "datatype": 
                                                table_query = f"select top 10 * from {selected_table}"
                                                # Executar a query para obter os dados
                                                df = pd.read_sql(table_query, connection)

                                                # Obter os nomes das colunas e seus tipos de dados
                                                column_data_types = df.dtypes.reset_index()
                                                column_data_types.columns = ["Column Name", "Data Type"]

                                                # Exibir os tipos de dados para cada coluna
                                                st.write("### Data Types for Each Column:")
                                                st.dataframe(column_data_types,hide_index=True)


                                    except Exception as e:
                                        st.error(f"Error: Unable to execute the query. {e}")
                                        st.stop()

            if choice == "ETL":
                    st.header("ETL (Extract, Transform, Load)")
                    st.write("new one")
            if choice == "Modeling":
                    st.header("Modeling")
                

if __name__ == "__main__":
    main()
