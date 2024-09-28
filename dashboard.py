import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_monthly_order(df):
    monthly_orders_df = df.resample(rule='M', on='dteday').agg({
    "cnt": "sum"
    })
    monthly_orders_df.index = monthly_orders_df.index.strftime('%Y-%m')
    monthly_orders_df = monthly_orders_df.reset_index()
    monthly_orders_df.rename(columns={
        "cnt": "order_count"
    }, inplace=True) 
    return monthly_orders_df

def create_weather(df):
    weather_df = df.groupby(by="weathersit").cnt.sum().reset_index()
    weather_df.rename(columns={
        "cnt": "order_count"
    }, inplace=True)
    
    return weather_df

day_df = pd.read_csv("Bike-sharing-dataset/day.csv")
hour_df = pd.read_csv("Bike-sharing-dataset/hour.csv")

datetime_columns = ["dteday"]
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)
 
for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

monthly_order_df = create_monthly_order(main_df)
weather_df = create_weather(main_df)


st.header('Dashboard Rental Sepeda :sparkles:')


st.subheader('Statistik rental per bulan')
 
col1, col2 = st.columns(2)
 
with col1:
    total_orders = monthly_order_df.order_count.sum()
    st.metric("Total orders", value=total_orders)
 
with col2:
    avarage_orders = monthly_order_df.order_count.mean()
    st.metric("Average orders", value=avarage_orders)
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_order_df["dteday"],
    monthly_order_df["order_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15, rotation=45)
 
st.pyplot(fig)


st.subheader("Pengaruh antara cuaca dengan performa rental")
fig, ax = plt.subplots(figsize=(20, 10))    
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
        y="order_count", 
        x="weathersit",
        data=weather_df.sort_values(by="order_count", ascending=False),
        palette=colors,
        ax=ax
    )
ax.set_title("Jumlah rental berdasarkan kondisi cuaca", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
ax.legend(
    handles=[
        plt.Line2D([0], [0], color="#90CAF9", lw=4),
        plt.Line2D([0], [0], color="#D3D3D3", lw=4),
        plt.Line2D([0], [0], color="#D3D3D3", lw=4)
    ],
    labels=['1: Cerah', '2: Kabut + Berawan', '3: Hujan Ringan + Salju'],
    title='Kondisi Cuaca',
    loc='upper right',
    fontsize=25
)
st.pyplot(fig)



st.subheader("Tren Waktu")
hour_df["time_period"] = hour_df.hr.apply(
    lambda x: "Pagi" if 6 <= x < 11 else (
    "Siang" if 11 <= x < 15 else (
    "Sore" if 15 <= x < 19 else 
    "Malam" if 19 <= x or x == 0 else 
    "Subuh" if x < 6 else "Tidak ada"
    )))
hour_df.groupby(by="time_period").cnt.sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(8, 8))

time_period_counts = hour_df.groupby(by="time_period").cnt.sum().sort_values(ascending=False)
# Create the pie chart
ax.pie(time_period_counts, labels=time_period_counts.index, autopct='%1.1f%%', startangle=90)
ax.set_title("Distribusi Rental Berdasarkan Waktu", fontsize=16)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

st.pyplot(fig)

