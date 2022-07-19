_Debug = False

import streamlit as st
import json

from Interface_options import *


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


