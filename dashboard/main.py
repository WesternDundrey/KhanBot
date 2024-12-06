import streamlit as st

from frontend.st_utils import auth_system


def main():
    # readme section
    st.markdown("# KhanBot")
    st.markdown(
        "KhanBot is a comprehensive cryptocurrency trading automation platform that combines strategy configuration, backtesting capabilities, and performance analysis in a user-friendly interface. "
       
        
    )
    st.markdown( "CURRENTLY ONLY AVAILABLE FOR MACOS AND LINUX SUBSYSTEMS.")
    st.markdown("[Khanbot](https://github.com/WesternDundrey/KhanBot)")
auth_system()
main()
