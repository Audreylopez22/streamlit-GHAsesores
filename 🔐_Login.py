import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from datetime import datetime

st.set_page_config(page_title="Login", page_icon="👋", layout="wide")

with open("./config.yaml", "r") as file:
    config = yaml.load(file, Loader=SafeLoader)

for i, username in enumerate(config["credentials"]["usernames"]):
    config["credentials"]["passwords"][i] = st.secrets.paswords[username]

now = datetime.now()
now_day = now.day

if now_day >= 1 and now_day < 6:
    st.warning("Remember to pay your membership the first 5 days of the month.")


def main():
    if st.secrets.subscription.active:
        authenticator = stauth.Authenticate(
            config["credentials"]["names"],
            config["credentials"]["usernames"],
            config["credentials"]["passwords"],
            config["cookie"]["name"],
            config["cookie"]["key"],
            config["cookie"]["expiry_days"],
        )

        name, authentication_status, username = authenticator.login("Login", "main")

        if st.session_state["authentication_status"]:
            st.write(f'Welcome *{st.session_state["name"]}*')
            authenticator.logout("Logout", "main")
        elif st.session_state["authentication_status"] is False:
            st.error("Username/password is incorrect")
        elif st.session_state["authentication_status"] is None:
            st.warning("Please enter your username and password")
    else:
        st.warning(
            "Your subscription is inactive. Please make the monthly payment to access the application."
        )


if __name__ == "__main__":
    main()
