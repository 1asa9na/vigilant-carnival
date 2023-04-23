import streamlit as st
import pydeck as pdk
import pandas as pd


def main():
    df = load_data()
    page = st.sidebar.selectbox("Choose a page", ["Homepage", "Exploration"])
    
    if page == "Homepage":
        st.header("This is your data explorer.")
        st.write("Please select a page on the left.")
        st.write(df)
        st.write("# Features description")
        st.write(
            """
            Data describes taxi trip duration based on pickup and dropoff coordinates and passenger count.
            Original datased had few more fields like pickup time and dropoff time, but it was totally useless.

            Field names are pretty exhaustive, no description needed.
            """
        )
    elif page == "Exploration":
        st.title("Data Exploration")
        st.pydeck_chart(pdk.Deck(
            map_style=None,
            initial_view_state=pdk.ViewState(
                longitude=df['pickup_longitude'].mean(),
                latitude=df['pickup_latitude'].mean(),
                zoom=11,
            ),
            layers=pdk.Layer(
                "ColumnLayer",
                data=df,
                get_position=["pickup_longitude", "pickup_latitude"],
                elevation_scale=100,
                radius=50,
            )
        ))


@st.cache_data
def load_data():
    df = pd.read_csv('df_test.csv', sep=';')
    return df


if __name__ == "__main__":
    main()
