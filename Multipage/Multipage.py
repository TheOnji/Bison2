
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

    #Configuration sidebar
    with st.sidebar:
        st.header('Navigation')

	

if __name__ == '__main__':
	main()