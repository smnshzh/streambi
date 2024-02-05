import streamlit as st
import hashlib
import toml
import extra_streamlit_components as stx
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
# Function to hash the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
def load_existing_users():
    try:
        with open("users.toml", "r") as toml_file:
            existing_users = toml.load(toml_file)
            return existing_users
    except FileNotFoundError:
        return {}  # Return an empty dictionary if the file doesn't exist
# Function to save user credentials to a TOML file
def save_credentials(username, password, email, role):
    try:
        # Input validation
        if not all([username, password, email, role]):
            raise ValueError("All input parameters must be provided")

        hashed_password = hash_password(password)
        new_user = {"username": username, "password": hashed_password, "email": email, "role": role}

        # Load existing users from TOML file
        try:
            with open("users.toml", "r") as toml_file:
                existing_users = toml.load(toml_file)
        except FileNotFoundError:
            existing_users = {}
        if username not in existing_users.keys():
            # Update existing user data with the new user
            existing_users[username] = new_user
            
            # Save the updated user list back to the TOML file
            with open("users.toml", "w") as toml_file:
                toml.dump(existing_users, toml_file)
            st.message(f"User {username} created successfully!")
            logging.info("User credentials saved successfully.")
            return True  # Indicate success
        else:
            st.error(f"Username '{username}' already exists. Please choose another username.")
            logging.warning("Failed to create user due to duplicate username.")
            return False  # Indicate failure
    
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return False  # Indicate failure
     


# Function to validate user credentials
def validate_credentials(username, password):
    try:
        # Input validation
        if not all([username, password]):
            raise ValueError("Username and password must be provided")

        hashed_password = hash_password(password)

        # Load existing users from TOML file
        existing_users = load_existing_users()

        # Check if the provided username and hashed password match any user in the list
        if username in existing_users and existing_users[username]["password"] == hashed_password:
            logging.info("User credentials validated successfully.")
            return True, existing_users[username]["role"]  # Return True and the user's role
        else:
            logging.info("User credentials validation failed.")
            return False, None  # Return False and None for role
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return False, None  # Return False and None for role in case of an error

# Function to check and authenticate user
def check_password():
    cookie = stx.CookieManager(key="MainCookie")
    if not cookie.get(cookie="autherized"):
        # First run or previous login attempt failed, show inputs for username + password.
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            # Validate credentials
            is_authenticated, user_role = validate_credentials(username, password)
            if is_authenticated:
                cookie.set("autherized", True, key="set_autherized")
                cookie.set("username", username, key="set_username")
                cookie.set("user_role", user_role, key="set_user_role")
                print("Logged in")
                st.success("😀 Login successful.")
                return True
            else:
                st.error("😕 User not known or password incorrect")
    else:
        # User is already logged in.
        st.success(f"Welcome {cookie.get('username')} (Role: {cookie.get('user_role')})")

        log_out = st.sidebar.button("Log out", key="logOut")
        if log_out:
            cookie.delete("autherized",key="delet_autherized")
            cookie.delete("username",key="delet_usernam")
            cookie.delete("user_role",key="delet_password")

        return True
