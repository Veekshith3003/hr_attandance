import streamlit as st
import pandas as pd

st.title("Access Card Log Processor")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("Columns found:", df.columns.tolist())

    df['Date And Time'] = pd.to_datetime(df['Date And Time'])

    df = df.sort_values(by=['User ID', 'Date And Time'])

    first_entries = df.groupby('User ID').first().reset_index()
    last_entries = df.groupby('User ID').last().reset_index()

    first_entries['Entry Type'] = 'First Entry'
    last_entries['Entry Type'] = 'Last Entry'

    result = pd.concat([first_entries, last_entries]).sort_values(by=['User ID', 'Date And Time'])

    st.write("### Processed Data:")
    st.dataframe(result)

    @st.cache_data
    def convert_df(df):
        return df.to_excel(index=False, engine='openpyxl')

    st.download_button(
        label="Download Result Excel",
        data=convert_df(result),
        file_name="first_last_entries.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
