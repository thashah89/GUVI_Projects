import streamlit as st
import mysql.connector
import pandas as pd
import re
import math

# To use the width of the page
st.set_page_config(layout="wide")

# Streamlit app title
st.title("Redbus Data Scrapper")

# Function to connect to MySQL and fetch data
def fetch_data(inp):
    try:
        # Establish the MySQL connection
        mydb = mysql.connector.connect(
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
    except mysql.connector.Error as e:
        st.write(f"An error occurred: {e}")
        return None

    finally:
        # To close the connection after operation
        if mydb.is_connected():
            cursor.close()
            mydb.close()

# Fetch data from MySQL and display it in Streamlit
query = 'SELECT * FROM bus_routes order by id asc'
data = fetch_data(query)

if data is not None:
    state = st.sidebar.selectbox("State Filter:",fetch_data('select distinct state from bus_routes'),index=0)
    route_name = st.sidebar.selectbox("Select Bus Type:",fetch_data(f"select distinct bus_route_name from bus_routes where state = '{state}'"))
    depart_time = st.sidebar.radio("Select your preferred start time:",["All","Mid-night to 06:00 AM", "06:00 AM to 12:00 PM","12:00 PM to 05:00 PM", "05:00 PM to 10:00 PM", "10 PM to Mid-night"])
    
    def display_stars(rating):
        # Number of filled and empty stars
        filled_stars = int(rating)
        empty_stars = 5 - filled_stars
        stars = "★" * filled_stars + "☆" * empty_stars
        return stars
    
    star_options = [5, 4, 3, 2, 1]
    star_labels = [f"{display_stars(x)} {x} star & below" if x <= 1 else f"{display_stars(x)} up to {x} stars" for x in star_options]

    star = st.sidebar.radio("Select filter based on star rating:", star_labels, index=0)
    star_num = re.search(r'\d',star)

    if star_num:
        star_num = int(star_num.group())

    pf = int(data['price'].max())
    price_options = [i for i in range(0,pf+1,100)]
    price_filter = st.sidebar.select_slider("Select to filter bus based on price:",options=price_options,value=(0,pf))

    sa = int(math.ceil(data['seat_availability'].max()/10)*10)
    seat_options = [i for i in range(0,sa+1)]
    seat_filter = st.sidebar.select_slider("Select to filter bus based on seat availability:",options=seat_options,value=(0,sa))

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

        st.markdown(f"<span style='font-size: 40px; color: red; weight: bold;'>{total_count}</span> <span style='font-size: 25px;'> buses available for selected filter:</span>", unsafe_allow_html=True)
        st.dataframe(data[['bus_name','bus_type','depart_time','duration','reach_time',
                            'star_rating','price','seat_availability']].sort_values('depart_time',ascending=True),height=600, use_container_width=True,hide_index=True)
    except:
        st.warning("No buses available for the selected filter.")
else:
    st.write("No data to display.")
