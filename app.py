from matplotlib import pyplot as plt
import streamlit as st
import pydeck as pdk
import pandas as pd
from PIL import Image
import json
from io import StringIO
import seaborn as sns
import pickle


def main():
    df = load_data()
    page = st.sidebar.selectbox("Choose a page", ["Homepage", "Data Exploration", "Data Prediction"])
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
    elif page == "Data Exploration":
        edited_df = pd.read_json(json.dumps(list(
            [{"path": i[0], "color": i[1], "name": f"trip duration: {i[2]}\npassenger count: {i[3]}"} for i in zip(df['coordinates'], df['color'], df['trip_duration'], df['passenger_count'])])))
        st.title("Data Exploration")
        st.pydeck_chart(pdk.Deck(
            initial_view_state=pdk.ViewState(df['pickup_longitude'].mean(), df['pickup_latitude'].mean(), zoom=10),
            layers = [pdk.Layer(
                type="PathLayer",
                data=edited_df,
                pickable=True,
                get_color="color",
                width_scale=20,
                width_min_pixels=1,
                get_path="path",
                get_width=1,
            ),
            pdk.Layer(
                type="ScatterplotLayer",
                data=df,
                pickable=True,
                opacity=0.8,
                filled=True,
                radius_scale=6,
                radius_min_pixels=5,
                radius_max_pixels=100,
                get_position="pickup_coordinates",
                get_radius="passenger_count",
                get_fill_color=[255, 140, 0],
            ),
                pdk.Layer(
                type="ScatterplotLayer",
                data=df,
                pickable=True,
                opacity=0.8,
                filled=True,
                radius_scale=6,
                radius_min_pixels=5,
                radius_max_pixels=100,
                get_position="dropoff_coordinates",
                get_radius="passenger_count",
                get_fill_color=[140, 0, 255],
            )], tooltip={"text": "{name}"})
        )
        fig, ax = plt.subplots()
        sns.heatmap(df[['passenger_count', 'pickup_longitude', 'pickup_latitude',
                    'dropoff_longitude', 'dropoff_latitude']].corr(), ax=ax)
        st.write(fig)
    elif page == "Data Prediction":
        st.title("Data Prediction")
        pickled_model = pickle.load(open('finalized_model.sav', 'rb'))
        uploaded_file = st.file_uploader("Choose a CSV file", accept_multiple_files=False)
        bytes_data = uploaded_file.read()
        s = str(bytes_data, 'utf-8')
        data = StringIO(s)
        df_uploaded = pd.read_csv(data)
        st.write(df)

        


@st.cache_data
def load_data():
    df = pd.read_csv('df_test.csv', sep=';')[:100]
    df['pickup_coordinates'] = list(
        zip(df['pickup_longitude'], df['pickup_latitude']))
    df['dropoff_coordinates'] = list(
        zip(df['dropoff_longitude'], df['dropoff_latitude']))
    df['coordinates'] = list(
        zip(df['pickup_coordinates'], df['dropoff_coordinates'])
    )
    img = Image.open('heatmap.jpg')
    pixels = img.load()
    width = img.size[0]
    max_dur = max(df['trip_duration'])
    df['color'] = list([pixels[int((i - 1) * width / max_dur), 0]
                       for i in df['trip_duration']])
    return df

if __name__ == "__main__":
    main()
