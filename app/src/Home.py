##################################################
# This is the main/entry-point file for the 
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar

# streamlit supports reguarl and wide layout (how the controls
# are organized/displayed on the screen).
st.set_page_config(layout = 'wide', initial_sidebar_state="collapsed")

# If a user is at this page, we assume they are not 
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false. 
st.session_state['authenticated'] = False

# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel. 
# IMPORTANT: ensure src/.streamlit/config.toml sets
# showSidebarNavigation = false in the [client] section
#SideBarLinks(show_home=True)

pages, styles, logo, options = get_nav_config(show_home=True)
page = st_navbar(pages, styles=styles, logo_path=logo, options=options)

# ***************************************************
#    The major content of this page
# ***************************************************

# set the title of the page and provide a simple prompt. 
logger.info("Loading the Home page of the app")
st.title('CoLink')
st.write('\n\n')
st.write('### Hello! As which user would you like to log in?')

# For each of the user personas for which we are implementing
# functionality, we put a button on the screen that the user 
# can click to MIMIC logging in as that mock user. 

if st.button("Act as Kali, a student co-oping in the US", 
            type = 'primary', 
            use_container_width=True) or page == "Kali":
    # when user clicks the button, they are now considered authenticated
    st.session_state['authenticated'] = True
    # we set the role of the current user
    st.session_state['role'] = 'us_coop_student'
    # we add the first name of the user (so it can be displayed on 
    # subsequent pages). 
    st.session_state['first_name'] = 'Kali'
    # finally, we ask streamlit to switch to another page, in this case, the 
    # landing page for this particular user type
    logger.info("Logging in as Kali Linux")
    st.switch_page('pages/00_US_Student_Home.py')

if st.button('Act as Winston, a student co-oping abroad', 
            type = 'primary', 
            use_container_width=True) or page == "Winston":
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'abroad_coop_student'
    st.session_state['first_name'] = 'Winston'
    st.switch_page('pages/10_Abroad_Student_Home.py')

if st.button('Act as Chloe, a System Administrator', 
            type = 'primary', 
            use_container_width=True) or page == "Chloe":
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'administrator'
    st.session_state['first_name'] = 'Chloe'
    st.switch_page('pages/20_Admin_Home.py')

if st.button('Act as Joey, a Data Analyst',
             type = 'primary',
             use_container_width = True) or page == "Joey":
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'data_analyst'
        st.session_state['first_name'] = 'Joey'
        st.switch_page('pages/30_Data_Analyst_Home.py')