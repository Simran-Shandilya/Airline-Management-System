import pandas as pd
import psycopg2
import streamlit as st
from configparser import ConfigParser

"# AIRLINE MANAGEMENT SYSTEM"


@st.cache
def get_config(filename="./database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)
    return {k: v for k, v in parser.items(section)}


@st.cache
def query_db(sql: str):
    # print(f"Running query_db(): {sql}")

    db_info = get_config()

    # Connect to an existing database
    conn = psycopg2.connect(**db_info)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a command: this creates a new table
    cur.execute(sql)

    # Obtain data
    data = cur.fetchall()

    column_names = [desc[0] for desc in cur.description]

    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()

    df = pd.DataFrame(data=data, columns=column_names)

    return df


def fetchDetails(traveler_id, trip_id):
    sql_search_query = f'select T.fname First_Name, T.lname Last_Name, T.phone Contact_Number from traveller T where T.id = \'{traveler_id}\' and T.trip_id = \'{trip_id}\';'
    data = query_db(sql_search_query)
    return data


def findItenerary(traveler_id, trip_id):
    sql_search_query = f'Select ft.departure_airport, ft.depart_time, ft.arrival_airport, ft.arrival_time, ft.airplane_no From Traveller t, Flight_Trip ft Where T.id = \'{traveler_id}\' And T.trip_id= \'{trip_id}\' And T.trip_id=ft.trip_id;'
    data = query_db(sql_search_query)
    return data


def findHalts(traveler_id, trip_id):
    sql_search_query = f'Select a.airport_name halt,stop.arrival_time, stop.depart_time From Traveller t, Flight_Trip ft, stop,airport a Where T.id= \'{traveler_id}\' And T.trip_id= \'{trip_id}\' And T.trip_id=ft.trip_id And stop.stop_id=ft.stop_id And a.airport_id=stop.airport_id;'
    data = query_db(sql_search_query)
    return data


def findUser(user_type):
    sql_user_search = f'Select user_type, count(*) From Users Where user_type = \'{user_type}\' Group by user_type;'
    data = query_db(sql_user_search)
    return data


def findUserDetail(user_type):
    sql_user_search = f'Select aa.airnines_name, count(*) From flight_trip ft, users u, airplane_airline aa Where ft.trip_id=u.trip_id And ft.airplane_no=aa.airplane_no and u.user_type=\'{user_type}\' Group by aa.airnines_name;'
    data = query_db(sql_user_search)
    return data


def findData(airplane):
    sql_user_search = f' Select seat.location seat_position, count(*) availability From seat Where seat.airplane_no = \'{airplane}\' and seat.availability=True Group by seat.location;'
    data = query_db(sql_user_search)
    return data


def findAirline(selectedAirline):
    sql_user_search = f' Select aa.airnines_name, count(*) From Airplane_Airline aa Where aa.airnines_name = \'{selectedAirline}\' Group by aa.airnines_name;'
    data = query_db(sql_user_search)
    return data


def findFare(selectedAirline):
    sql_airport_search = f'Select distinct ft.airplane_no, aa.airnines_name airlines_name, fare.final_amount From Flight_trip ft, fare, airplane_airline aa Where ft.trip_id=fare.trip_id And aa.airplane_no=ft.airplane_no and airnines_name = \'{selectedAirline}\' order by fare.final_amount, ft.airplane_no;'
    data = query_db(sql_airport_search)
    return data


def main():
    from PIL import Image
    image = Image.open('airport.jpg')
    st.image(image)
    menu = ['Homepage', 'Airline Details', 'User Details',
            'Seat Availability', 'Flight Fares']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Homepage':
        st.subheader('Traveller Info')
        st.write(
            'This page displays the traveller details given an Traveller ID and a Trip ID.')
        traveler_id = st.number_input(
            'Enter Traveler ID', max_value=120, min_value=1)
        trip_id = st.number_input(
            'Enter Trip ID', max_value=220, min_value=101)
        submit = st.button('Submit')
        if submit:
            res = (fetchDetails(traveler_id, trip_id))
            iti = (findItenerary(traveler_id, trip_id))
            halts = (findHalts(traveler_id, trip_id))
            df3 = pd.DataFrame(res)
            if df3.shape[0] > 0:
                st.dataframe(df3)
                st.success("Successfull")
            else:
                st.error(
                    'No details found for this user for the selected Traveller ID and Trip ID')
            st.subheader('Itenerary')
            with st.expander("Expand to View Full Itinerary"):
                df = pd.DataFrame(iti)
                if df.shape[0] > 0:
                    st.dataframe(df)
                    st.success("Successfull")
                else:
                    st.error('No itinerary found for the user.')
            st.subheader('Layovers')
            with st.expander("Expand to View Layovers"):
                df1 = pd.DataFrame(halts)
                if df1.shape[0] > 0:
                    st.dataframe(df1)
                    st.success("Successfull")
                else:
                    st.error('No layover for this flight.')

    elif choice == 'Airline Details':
        st.subheader('Airline Details')
        st.write(
            'This page displays the number of airplanes operating for a selected airline')
        sql_find_rest = 'select distinct airnines_name from Airplane_Airline order by airnines_name;'
        try:
            airlinedata = query_db(sql_find_rest)
            selectedAirline = st.selectbox(
                "Choose an Airline", airlinedata['airnines_name'].tolist())
            st.dataframe(findAirline(selectedAirline))
            st.success("Successfull")
        except Exception as e:
            st.write(e)
            st.write('Something went wrong.')

    elif choice == 'User Details':
        st.subheader('User Details')
        st.write('This page displays the number of tickets booked by user type, which can be an agency or a traveller himself.')
        user_type = st.selectbox('What type of user are you?', [
                                 'traveller', 'agency'])
        submit = st.button('Submit')
        st.success("Successfull")
        if submit:
            usr = (findUser(user_type))
            usrdtl = (findUserDetail(user_type))
            st.write(usr)
            st.subheader('Details')
            with st.expander("Expand to View List of airlines booked by User Type"):
                st.success("Successfull")
                df2 = pd.DataFrame(usrdtl)
                st.dataframe(df2)

    elif choice == 'Seat Availability':
        st.subheader('Seat Availability')
        st.write(
            'This page displays the number of seats available per seat type for the selected airplane number.')
        airplane_no = 'select distinct airplane_no from AIRPLANE_AIRLINE order by airplane_no;'
        try:
            airplanedata = query_db(airplane_no)
            selectedAirplane = st.selectbox(
                "Choose an Airplane", airplanedata['airplane_no'].tolist())
            st.dataframe(findData(selectedAirplane))
        except Exception as e:
            st.write(e)
            st.write('Something went wrong.')

    elif choice == 'Flight Fares':
        st.subheader('Fare Details')
        st.write(
            'This page displays the fare for a given airlines')
        airline_name = 'select distinct airnines_name from AIRPLANE_AIRLINE order by airnines_name;'
        try:
            airlinedata = query_db(airline_name)
            selectedAirline = st.selectbox(
                "Choose an Airline", airlinedata['airnines_name'].tolist())
            fare = (findFare(selectedAirline))
            df4 = pd.DataFrame(fare)
            if df4.shape[0] > 0:
                st.dataframe(df4)
                st.success("Successfull")
            else:
                st.error('No seats available in this flight')
        except Exception as e:
            st.write(e)
            st.write('Something went wrong.')


if __name__ == '__main__':
    main()
