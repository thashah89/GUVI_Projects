# Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit

## Project Overview

The **Redbus Data Insight Teacker with Selenium & Dynamic Filtering using Streamlit** project provides a solution for collecting, analyzing, and visualizing bus travel data. The project uses **Selenium** to scrape detailed bus information from the Redbus website, including routes, schedules, prices, and seat availability. The scraped data is stored in a SQL database and presented in an interactive **Streamlit** application with dynamic filtering capabilities.

## Skills Acquired

- Web Scraping using **Selenium** and **Python**
- Interactive Web Applications with **Streamlit**
- SQL Database design and interaction
- Data Analysis and Filtering using SQL queries
- Python programming best practices

## Technologies Used

- **Python**
- **Selenium** for web scraping
- **Streamlit** for creating interactive applications
- **SQL** for data storage

## Domain

- Transportation

## Problem Statement

This project aims to streamline the collection of bus travel data from the Redbus platform and provide powerful tools for analyzing and filtering the data. By scraping the data using **Selenium**, this project helps in gaining insights about bus routes, prices, and seat availability, improving operational efficiency in the transportation business.

## Business Use Cases

- **Travel Aggregators**: Providing real-time bus schedules and seat availability.
- **Market Analysis**: Analyzing travel patterns and market trends.
- **Customer Service**: Enhancing user experience by offering tailored travel options.
- **Competitor Analysis**: Comparing pricing and service levels across operators.

## Approach

### Data Scraping

- **Selenium** is used to automate the extraction of bus route data, schedules, prices, and seat availability from the **Redbus** website.

### Data Storage

- The scraped data is stored in a **SQL** database to ensure structured and efficient access.

### Streamlit Application

- A **Streamlit** application is created to display the scraped data, with filters for easy exploration.
- Filters include bus type, route, price range, star rating, and seat availability.

### Data Filtering & Analysis

- **SQL** queries are used to filter and retrieve relevant data based on user inputs.
- The **Streamlit** interface allows users to dynamically apply filters to view different bus services.

## Results & Goals

- Have Scraped data for 12 government state bus routes and private bus information.
- Store the scraped data in a structured **SQL** database.
- Develop an interactive **Streamlit** application to filter and explore the data.
- Ensure a user-friendly experience with efficient performance.

## Project Evaluation Metrics

- **Data Scraping Accuracy**: Completeness and correctness of the scraped data.
- **Database Design**: Effectiveness of the database schema.
- **Application Usability**: User experience of the **Streamlit** application.
- **Filter Functionality**: Responsiveness and effectiveness of the filters.
- **Code Quality**: Adherence to best practices in code quality.

## Dataset

- **Source**: Data scraped from the [Redbus website](https://www.redbus.in/).
- **Format**: Stored in a **SQL** database.
- **Required Fields**:
  - Bus route link
  - Bus route name
  - Bus name
  - Bus type (Sleeper/Seater)
  - Departure time
  - Duration of the journey
  - Reaching time
  - Star rating
  - Price
  - Seat availability

### Dataset Breakdown:

- **Bus Routes Name**: Start and end locations of each bus journey.
- **Bus Routes Link**: Link to detailed information for the bus route.
- **Bus Name**: Name of the bus or service provider.
- **Bus Type**: Type of bus (e.g., Sleeper/Seater).
- **Departing Time**: Time of departure.
- **Duration**: Duration of the journey.
- **Reaching Time**: Expected arrival time.
- **Star Rating**: Rating based on user feedback.
- **Price**: Ticket cost.
- **Seat Availability**: Available seats at the time of scraping.

## Database Schema

Table: `bus_routes`

| Column Name       | Data Type  | Description                                    |
|-------------------|------------|------------------------------------------------|
| id                | INT        | Primary Key (Auto-increment)                   |
| route_name        | TEXT       | Bus Route information for each state transport|
| route_link        | TEXT       | Link to the route details                      |
| busname           | TEXT       | Name of the bus                               |
| bustype           | TEXT       | Type of the bus (e.g., Sleeper/Seater)        |
| departing_time    | TIME       | Departure time                                |
| duration          | TEXT       | Duration of the journey                       |
| reaching_time     | TIME       | Arrival time                                  |
| star_rating       | FLOAT      | Rating of the bus                             |
| price             | DECIMAL    | Price of the ticket                           |
| seats_available   | INT        | Number of seats available                     |

## Project Deliverables

- **Git Hub Link**: https://github.com/thashah89/GUVI_Projects 

