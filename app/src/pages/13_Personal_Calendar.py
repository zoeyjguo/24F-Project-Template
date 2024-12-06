import logging
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import get_nav_config
from streamlit_navigation_bar import st_navbar
from datetime import date, datetime, timedelta
import calendar

logger = logging.getLogger(__name__)

if "authenticated" not in st.session_state:
    st.switch_page("Home.py")

# \navigation bar setup
pages, styles, logo, options = get_nav_config(show_home=False)
page = st_navbar(pages, selected="Calendar", styles=styles, logo_path=logo, options=options)

if page == "Update Location":
    st.switch_page('pages/11_Update_Location.py')

if page == "Group Chat":
    st.switch_page('pages/14_Winston_GroupChat.py')

if page == "Logout":
    del st.session_state["role"]
    del st.session_state["authenticated"]
    st.switch_page("Home.py")

# styling for group chat box
st.markdown(
    """
    <style>
    .group-chat {
        margin-top: 1px;
        padding: 1px;
    }
    .group-chat h3 {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .group-chat-item {
        display: flex;
        align-items: center;
        margin-bottom: 15px;
        padding: 10px;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 1px 1px 4px rgba(0,0,0,0.1);
    }
    .group-chat-item img {
        border-radius: 10px;
        height: 60px;
        width: 60px;
        margin-right: 15px;
    }
    .group-chat-item div {
        font-size: 14px;
        flex: 1;
    }
    .group-chat-item div strong {
        display: block;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# fetch group chats and events
fetch_groupchats = requests.get('http://api:4000/u/users/1002/groupchats').json()
group_chats = []
events_fetch = requests.get("http://api:4000/u/users/1002/events").json()
events = {}

# add data from the fetch
for groupchat in fetch_groupchats:
    group_chats.append({"name": groupchat["Name"], "id": groupchat["GroupChatId"]})


for event in events_fetch:
    start_datetime_string = event.get("StartTime")
    end_datetime_string = event.get("EndTime") 

    start_date = datetime.strptime(start_datetime_string, "%a, %d %b %Y %H:%M:%S %Z")
    end_date = datetime.strptime(end_datetime_string, "%a, %d %b %Y %H:%M:%S %Z") if end_datetime_string else start_date

    current_date = start_date
    while current_date <= end_date:
        event_day = int(current_date.strftime("%d"))

        if event_day not in events:
            events[event_day] = []

        events[event_day].append({"day": event_day,"name": event.get("Title"),"color": event.get("color", "#AEC6CF")})

        # increment to the next day
        current_date += timedelta(days=1)


# create columns for layout
col1, col2 = st.columns([1,3])

# initialize the session state
if "selected_chat_id" not in st.session_state:
    st.session_state.selected_chat_id = 399

# group chats section in the left column
with col1:
    st.markdown("### Group Chats")
    for chat in group_chats:
        if st.button(chat['name']):
            st.session_state["selected_chat_id"] = chat['id']
            st.switch_page('pages/14_Winston_GroupChat.py')
            st.rerun()


# create the calender grid
def create_calendar(year, month, events):
    html_content = """
    <style>
    .calendar-container {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 5px;
    }
    .calendar-day {
        border: 1px solid #ddd;
        padding: 20px;
        border-radius: 5px;
        background-color: #f9f9f9;
        text-align: center;
        position: relative;
        min-height: 100px;
    }
    .day-number {
        font-weight: bold;
        margin-bottom: 5px;
    }
    .event {
        font-size: 0.8rem;
        padding: 5px;
        margin-top: 10px;
        border-radius: 3px;
        color: white;
    }
    </style>
    """

    _, num_days = calendar.monthrange(year, month)
    first_day = date(year, month, 1)
    start_weekday = first_day.weekday()

    html_content += f"<h3 style='text-align: center;'>{calendar.month_name[month]} {year}</h3>"
    days_of_week = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    html_content += "<div class='calendar-container'>" + "".join(
        [f"<div style='font-weight: bold;'>{day}</div>" for day in days_of_week]
    ) + "</div>"

    blank_days = ["<div></div>" for _ in range(start_weekday)]
    calendar_days = blank_days

    for day in range(1, num_days + 1):
        day_events = events.get(day, [])
        event_divs = "".join(
            [
                f"<div class='event' style='background-color: {event['color']};'>{event['name']}</div>"
                for event in day_events
            ])
        calendar_days.append(
            f"""
            <div class='calendar-day'>
                <div class='day-number'>{day}</div>
                {event_divs}
            </div>
            """
        )

    html_content += (
        "<div class='calendar-container'>" + "".join(calendar_days) + "</div>"
    )
    return html_content

# render the calendar
with col2:
    html_calendar = create_calendar(2024, 12, events)
    st.components.v1.html(html_calendar, height=1000, scrolling=False)