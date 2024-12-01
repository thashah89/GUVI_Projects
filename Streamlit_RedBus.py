import streamlit as st
import pymysql
import pandas as pd
import re
import math
from streamlit_option_menu import option_menu

# To use the width of the page
st.set_page_config(page_title="Red Bus Insight Tracker", layout="wide")

def home():
    st.markdown("<span style='font-size: 50px; color: red; weight: bold;'>**Welcome to Redbus Data Insight Tracker with Selenium & Dynamic Filtering using Streamlit**</span>", unsafe_allow_html=True)
    st.image("C:/Users/Shahul_Desktop/OneDrive/Desktop/GUVI_Projects/Redbus Cover.webp")

def about():
    st.markdown("<span style='font-size: 50px; color: red; weight: bold;'>**About the Red Bus Insight Tracker**</span>", unsafe_allow_html=True)
    
    st.write("""
    Welcome to the **Red Bus Insight Tracker**, an advanced data-driven platform designed to provide a seamless experience for exploring bus travel information. This project leverages cutting-edge technologies and intuitive features to empower users to make informed travel decisions. Whether you're a traveler, a data enthusiast, or a professional in the transportation industry, this tool is tailored to meet your needs.
    """)

    st.subheader("Project Overview")
    st.write("""
    The Red Bus Insight Tracker simplifies the process of searching, filtering, and analyzing bus routes across states in India. With this platform, users can explore various aspects of bus travel, including route details, schedules, pricing, and seat availability. It combines robust backend technologies, an intuitive frontend, and efficient data handling to deliver real-time insights.
    """)

    st.subheader("Key Features")
    st.markdown("""
    - **Dynamic Filtering Options**: 
        - Select a specific state and bus route to narrow your search.
        - Filter buses by departure time ranges, ratings, price, and seat availability.
    - **Interactive User Interface**: 
        - Developed using **Streamlit**, ensuring a responsive and user-friendly experience.
        - Real-time data visualization in an organized, tabular format.
    - **Rating Visualization**:
        - Star ratings are visually represented, making it easy to evaluate service quality at a glance.
    - **Real-Time Updates**: 
        - Integrated with a **MySQL database** to fetch and display the most up-to-date bus route and service information.
    - **Customizable Filters**: 
        - Multi-dimensional filters allow users to personalize their search based on travel preferences.
    """)

    st.subheader("Technologies and Tools Used")
    st.markdown("""
    1. **Frontend**:
       - **Streamlit**: Provides an intuitive, fast, and interactive web interface for displaying data and taking user inputs.
    2. **Backend**:
       - **Python**: The core programming language used for application logic, data processing, and interaction with the database.
       - **pymysql**: A Python library used to establish a seamless connection between the application and the MySQL database.
    3. **Database**:
       - **MySQL**: A relational database used to store and manage bus route data, including states, routes, prices, availability, and ratings.
    4. **Data Analysis**:
       - **Pandas**: A powerful library for data manipulation and analysis, used to process and display query results efficiently.
    5. **Other Libraries**:
       - **Math**: Used for rounding and calculating ranges for filters like seat availability.
       - **re (Regular Expressions)**: Enables text-based filtering and extraction for processing user inputs.
    6. **Deployment**:
       - Compatible with deployment on cloud platforms (e.g., **Heroku**, **Streamlit Community Cloud**) or local servers for ease of access.
    """)

    st.subheader("Workflow")
    st.markdown("""
    1. **Data Storage**: The MySQL database serves as the backbone, storing detailed records about bus routes, including attributes like state, route name, departure time, price, seat availability, and ratings.
    2. **User Interaction**: Users interact with the Streamlit interface to select filters such as state, route, departure time, price range, and ratings.
    3. **Data Processing**: The application processes these inputs and dynamically queries the database to fetch relevant results.
    4. **Real-Time Results**: The fetched data is displayed in an interactive table with highlights for the selected filters, enabling users to explore results effectively.
    5. **Feedback Loop**: Users can modify filters and instantly see updated results without any page reloads, thanks to Streamlit's real-time rendering capabilities.
    """)

    st.subheader("Benefits")
    st.markdown("""
    - **Ease of Use**: An intuitive interface ensures that even non-technical users can navigate and extract insights effortlessly.
    - **Scalability**: The use of MySQL and Python ensures that the platform can handle large datasets and complex queries.
    - **Efficiency**: Automated data retrieval and filtering save users significant time compared to manual searches.
    - **Customizability**: The platform is built to be easily extendable for additional features like booking integration, payment gateways, or API access for third-party use.
    """)

    st.subheader("Who Is It For?")
    st.markdown("""
    - **Travelers**: Find the best bus routes, timings, and fares effortlessly.
    - **Travel Agencies**: Optimize recommendations for clients with detailed insights.
    - **Data Analysts**: Explore travel patterns, ratings, and other data points for research and reporting.
    - **Developers**: Gain inspiration for building similar data-driven applications.
    """)

    st.write("This project exemplifies how modern technologies can come together to solve real-world problems in a seamless, efficient, and user-friendly manner.")



def InsightTracker():

    # Streamlit app title
    st.markdown(f"<span style='font-size: 50px; color: red; weight: bold;'>**Red Bus Insight Tracker**</span>", unsafe_allow_html=True)

    # Function to connect to MySQL and fetch data
    def fetch_data(inp):
        try:
            # Establish the MySQL connection
            mydb = pymysql.connect(
                host='127.0.0.1',
                user='root',       
                password='ShahulSqL2024',
                database='redbus'
            )
            
            # Creating a cursor object to interact with the database
            cursor = mydb.cursor()

            # Execute the query
            cursor.execute(inp)

            # Fetch all rows from the executed query
            rows = cursor.fetchall()

            # Get column names from cursor.description
            columns = [desc[0] for desc in cursor.description]

            # Create a DataFrame using Pandas
            df = pd.DataFrame(rows, columns=columns)

            # Return the DataFrame
            return df
        
        # To handle error with database connect
        except pymysql.Error as e:
            st.write(f"An error occurred: {e}")
            return None

        finally:
            # To close the connection after operation
            if mydb.connect():
                cursor.close()
                mydb.close()

    # Fetch data from MySQL and display it in Streamlit
    query = 'SELECT * FROM bus_routes order by id asc'
    data = fetch_data(query)

    if data is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            state = st.selectbox("Select state:",fetch_data('select distinct state from bus_routes'),index=0)
        
        with col2:
            route_name = st.selectbox("Select route:",fetch_data(f"select distinct bus_route_name from bus_routes where state = '{state}'"))
        
        depart_time = st.sidebar.radio("Select preferred start time:",["All","Mid-night to 06:00 AM", "06:00 AM to 12:00 PM","12:00 PM to 05:00 PM", "05:00 PM to 10:00 PM", "10 PM to Mid-night"])
        
        def display_stars(rating):
            # Number of filled and empty stars
            filled_stars = int(rating)
            empty_stars = 5 - filled_stars
            stars = "★" * filled_stars + "☆" * empty_stars
            return stars
        
        star_options = [5, 4, 3, 2, 1]
        star_labels = [f"{display_stars(x)} {x} star & below" if x <= 1 else f"{display_stars(x)} up to {x} stars" for x in star_options]

        star = st.sidebar.radio("Filter based on star rating:", star_labels, index=0)
        star_num = re.search(r'\d',star)

        if star_num:
            star_num = int(star_num.group())

        price = int(math.ceil(data['price'].max()/10)*10)
        price_options = [i for i in range(0,price+1,100)]
        price_filter = st.sidebar.select_slider("Filter by price:",options=price_options,value=(0,price))

        seat = int(math.ceil(data['seat_availability'].max()/10)*10)
        seat_options = [i for i in range(0,seat+1)]
        seat_filter = st.sidebar.select_slider("Filter by seat availability:",options=seat_options,value=(0,seat))

        try:
            if depart_time == 'All':
                data = fetch_data(f"select * from bus_routes where state = '{state}' and bus_route_name = '{route_name}'and star_rating <= {star_num} and price >= {price_filter[0]} and price <= {price_filter[1]} and seat_availability >= {seat_filter[0]} and seat_availability <= {seat_filter[1]}")
                total_count = data['id'].count()
            elif depart_time == 'Mid-night to 06:00 AM':
                data = fetch_data(f"select * from bus_routes where state = '{state}' and bus_route_name = '{route_name}' and departing_time >= '00:00:00' and departing_time < '06:00:00' and star_rating <= {star_num} and price >= {price_filter[0]} and price <= {price_filter[1]} and seat_availability >= {seat_filter[0]} and seat_availability <= {seat_filter[1]}")
                total_count = data['id'].count()
            
            elif depart_time == '06:00 AM to 12:00 PM':
                data = fetch_data(f"select * from bus_routes where state = '{state}' and bus_route_name = '{route_name}' and departing_time >= '06:00:00' and departing_time < '12:00:00' and star_rating <= {star_num} and price >= {price_filter[0]} and price <= {price_filter[1]} and seat_availability >= {seat_filter[0]} and seat_availability <= {seat_filter[1]}")
                total_count = data['id'].count()
            
            elif depart_time == '12:00 PM to 05:00 PM':
                data = fetch_data(f"select * from bus_routes where state = '{state}' and bus_route_name = '{route_name}' and departing_time >= '12:00:00' and departing_time < '17:00:00' and star_rating <= {star_num} and price >= {price_filter[0]} and price <= {price_filter[1]} and seat_availability >= {seat_filter[0]} and seat_availability <= {seat_filter[1]}")
                total_count = data['id'].count()
            
            elif depart_time == '05:00 PM to 10:00 PM':
                data = fetch_data(f"select * from bus_routes where state = '{state}' and bus_route_name = '{route_name}' and departing_time >= '17:00:00' and departing_time < '22:00:00' and star_rating <= {star_num} and price >= {price_filter[0]} and price <= {price_filter[1]} and seat_availability >= {seat_filter[0]} and seat_availability <= {seat_filter[1]}")
                total_count = data['id'].count()
            
            else:
                data = fetch_data(f"select * from bus_routes where state = '{state}' and bus_route_name = '{route_name}' and departing_time >= '22:00:00' and departing_time < '00:00:00' and star_rating <= {star_num} and price >= {price_filter[0]} and price <= {price_filter[1]} and seat_availability >= {seat_filter[0]} and seat_availability <= {seat_filter[1]}")
                total_count = data['id'].count()

            data['depart_time'] = data['departing_time'].dt.components.apply(lambda x: f"{x['hours']:02}:{x['minutes']:02}:{x['seconds']:02}",axis=1)
            data['reach_time'] = data['reaching_time'].dt.components.apply(lambda x: f"{x['hours']:02}:{x['minutes']:02}:{x['seconds']:02}",axis=1)

            st.markdown(f"<span style='font-size: 40px; color: red; weight: bold;'>**{total_count}**</span> <span style='font-size: 25px;'> buses available for selected filter:</span>", unsafe_allow_html=True)
            st.dataframe(data[['bus_name','bus_type','depart_time','duration','reach_time',
                                'star_rating','price','seat_availability']].sort_values('depart_time',ascending=True),height=600, use_container_width=True,hide_index=True)
        except:
            st.warning("No buses available for the selected filter.")
    else:
        st.warning("No data to display.")

def main():

    #st.sidebar.title("Welcome to Red Bus Insight Tracker")
    with st.sidebar:
        page = option_menu(
        menu_title=None,  # Title for the menu (optional)
        options=["Home", "About", "Insight Tracker"],  # Menu options
        icons=["house", "info-circle", "gear"],  # Font Awesome icons
        menu_icon="cast",  # Icon for the menu
        default_index=0,  # Default selected option
        orientation="vertical",  # Change to "vertical" for a sidebar menu
        )

    if page == "Home":
        home()
    elif page == "About":
        about()
    elif page == "Insight Tracker":
        InsightTracker()

if __name__ == "__main__":
    main()