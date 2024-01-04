import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('./dataset/airline_delay.csv')
#set display option
pd.set_option('display.max_columns',None)
df.dropna(inplace=True)

class PageState:
    def __init__(self):
        self.current_page = 'Main'


def sidebar():
    page_state = PageState()
    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            background-color: #f8f9fa;
        }
        .sidebar .sidebar-list {
            color: #333;
            font-weight: bold;
        }
        .sidebar .sidebar-list:hover {
            background-color: #e9ecef;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.sidebar.header('Menu')
    selected_page = st.sidebar.radio(
        'Go To', ('Total Arrive', 'Cancel Flight', 'Delay Over 15 Minutes', 'Delay Categories', 'About'))

    page_state.current_page = selected_page

    # Define the content for each page
    if page_state.current_page == 'Total Arrive':
        total_arrive()
    elif page_state.current_page == 'Cancel Flight':
        cancel()
    elif page_state.current_page == 'Delay Over 15 Minutes':
        delay_over15()    
    elif page_state.current_page == 'Delay Categories':
        delay_categories()        
    elif page_state.current_page == 'About':
        about()


def about():
    st.title('About this project')
    st.markdown('')
    st.markdown('''
        #### Airline Delay
        Project ini dibuat untuk memenuhi **tugas besar** dari mata kuliah **Visualisasi Data (IF-44-PIL-PJJ)** Universitas Telkom

        #### Dataset
        [Airline Delay](https://www.kaggle.com/datasets/eugeniyosetrov/airline-delays)

        #### Author
        M.Taufik Anugrah - 1301218696

    ''')


def delay_categories():
    # Calculate delays by category for each carrier and year
    delay_categories = df.groupby(['carrier_name', 'year'])[['carrier_delay', 'weather_delay', 'nas_delay', 'security_delay', 'late_aircraft_delay']].sum().reset_index()
    delay_categories = pd.melt(delay_categories, id_vars=['carrier_name', 'year'], value_vars=['carrier_delay', 'weather_delay', 'nas_delay', 'security_delay', 'late_aircraft_delay'], var_name='delay_category', value_name='total_delay')

    # Create selectboxes for year and delay category
    year_choice = st.selectbox('Pilih tahun:', ['2019', '2020', 'Keduanya'])
    delay_category_choice = st.selectbox('Pilih kategori penundaan:', ['Seluruhnya', 'carrier_delay', 'weather_delay', 'nas_delay', 'security_delay', 'late_aircraft_delay'])

    # Filter data based on selected year and category
    if year_choice != 'Keduanya':
        delay_categories = delay_categories[delay_categories['year'] == int(year_choice)]
    if delay_category_choice != 'Seluruhnya':
        delay_categories = delay_categories[delay_categories['delay_category'] == delay_category_choice]

    # Create the bar plot
    fig, ax = plt.subplots(figsize=(12, 8))
    plot = sns.barplot(x='carrier_name', y='total_delay', hue='delay_category', data=delay_categories, ci=None, ax=ax)

    # Customize the plot
    plt.xlabel('Carriers', fontsize=12)
    plt.ylabel('Total Delay Time', fontsize=12)
    plt.title('Carriers with the Highest Delays by Category (2019-2020)', fontsize=14)
    plt.xticks(rotation=45, fontsize=10)
    plt.legend(title="Delay Category", loc="upper left", fontsize=10)
    plt.tight_layout()

    # Display the plot in the Streamlit app
    st.pyplot(fig)

    

def total_arrive():
    # Calculate flight counts for each carrier and year
    flight_count = df.groupby(['carrier_name', 'year'])['arr_flights'].sum().reset_index()

    # Create a selectbox to choose the year
    year_choice = st.selectbox('Pilih tahun:', ['2019', '2020', 'Keduanya'])

    # Filter data based on selected year
    if year_choice != 'Keduanya':
        flight_count = flight_count[flight_count['year'] == int(year_choice)]

    # Create the bar plot
    fig, ax = plt.subplots(figsize=(6, 8))
    sns.set(style="whitegrid")
    sns.barplot(y='carrier_name', x='arr_flights', hue='year', data=flight_count, orient='h', ax=ax)

    # Customize the plot
    plt.ylabel('Carriers', fontsize=8)
    plt.xlabel('Total Number of Flights', fontsize=8)
    plt.title("Total Number of Flights by Carrier (December 2019 and 2020)", fontsize=8)
    plt.yticks(rotation=45, fontsize=8)
    plt.legend(title="Year", loc="upper right", fontsize=8)
    plt.tight_layout()

    # Display the plot in the Streamlit app
    st.pyplot(fig)

def delay_over15():
    # Calculate flight delays for each carrier and year
    flight_delay = df.groupby(['carrier_name', 'year'])['arr_del15'].sum().reset_index()

    # Create a selectbox to choose the year
    year_choice = st.selectbox('Pilih tahun:', ['2019', '2020', 'Keduanya'])

    # Filter data based on selected year
    if year_choice != 'Keduanya':
        flight_delay = flight_delay[flight_delay['year'] == int(year_choice)]

    # Create the bar plot
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x='carrier_name', y='arr_del15', data=flight_delay, hue='year', ax=ax)

    # Customize the plot
    plt.xlabel('Carriers', fontsize=8)
    plt.ylabel('No of Delayed Flights > 15mins', fontsize=8)
    plt.title('Total No of Delayed Flights Over 15 Minutes (2019-2020)', fontsize=8)
    plt.xticks(rotation=45, fontsize=8)
    plt.legend(title="Year", loc="upper left", fontsize=8)
    plt.tight_layout()

    # Display the plot in the Streamlit app
    st.pyplot(fig)

def cancel():
    # Calculate cancelled flights for each carrier and year
    cancelled_flights = df.groupby(['carrier_name', 'year'])['arr_cancelled'].sum().reset_index()

    # Create a selectbox to choose the year
    year_choice = st.selectbox('Pilih tahun:', ['2019', '2020', 'Keduanya'])

    # Filter data based on selected year
    if year_choice != 'Keduanya':
        cancelled_flights = cancelled_flights[cancelled_flights['year'] == int(year_choice)]

    # Create the bar plot
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x='carrier_name', y='arr_cancelled', data=cancelled_flights, hue='year', ax=ax)

    # Customize the plot
    plt.xlabel('Carriers', fontsize=8)
    plt.ylabel('No of Cancelled Flights', fontsize=8)
    plt.title('Total No of Cancelled Flights (2019-2020)', fontsize=8)
    plt.xticks(rotation=45, fontsize=8)
    plt.legend(title="Year", loc="upper left", fontsize=8)
    plt.tight_layout()

    # Display the plot in the Streamlit app
    st.pyplot(fig)

def main():
    sidebar()


main()
