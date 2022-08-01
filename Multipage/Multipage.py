
import streamlit as st 
from pages.Interface_options import *


def main():
	#Page setting
    st.set_page_config(page_title = "BISON 2.0",
    					page_icon = ":ox:",
    					layout = "wide")

   	#---Page setup---
    st.text(logo)
    st.text('---Advanced FFXIV best-in-slot optimizer---')


    st.checkbox("Yes or No", key="Check_selection", on_change = ReadState)

    st.number_input("Select a num:", key ="num")

    st.write(st.session_state["Check_selection"])
    st.write(st.session_state["num"])

    #Configuration sidebar
    with st.sidebar:
        st.header('Navigation')

	
def ReadState():
    return None

if __name__ == '__main__':
	main()