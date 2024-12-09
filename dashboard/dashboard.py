import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style="dark")

# helpful function
def create_hr_df(hour_df):
    hr_users_df = hour_df.groupby('hr')[['registered','casual']].mean()
    hr_users_df = hr_users_df.reset_index()
    hr_users_df.rename(columns={
        "registered": "registered_user",
        "casual": "casual_user"
    }, inplace=True)

    return hr_users_df

def create_weekday_df(hour_df):
    weekday_users_df = hour_df.groupby('weekday').agg({
        "cnt": "sum"
    })
    weekday_users_df = weekday_users_df.reset_index()
    weekday_users_df.rename(columns={
        "cnt": "total_user"
    }, inplace=True)

    return weekday_users_df

# load dataset

all_df = pd.read_csv("https://raw.githubusercontent.com/faz024/bike-sharing/refs/heads/main/dashboard/hour_data_clean.csv")

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Data Filter
min_date_hour = all_df["dteday"].min()
max_date_hour = all_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://joyride.city/wp-content/uploads/2022/06/Joyride-e-bike-rental-software-scaled.jpg")
    st.link_button("Logo Source", "https://joyride.city/")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label="Time Filter",min_value=min_date_hour,
        max_value=max_date_hour,
        value=[min_date_hour, max_date_hour]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

# st.dataframe(main_df)
hr_users_df = create_hr_df(main_df)
weekday_users_df = create_weekday_df(main_df)

st.title(":chart_with_upwards_trend: Bike Share Dashboard")
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    total_all_rent = main_df["cnt"].sum()
    st.metric("Total Bike Share", value=total_all_rent)
with col2:
    total_registered_rent = main_df["registered"].sum()
    st.metric("Total Registered Users", value=total_registered_rent)
with col3:
    total_casual_rent = main_df["casual"].sum()
    st.metric("Total Casual Users", value=total_casual_rent)

st.markdown("---")

# Performance
st.subheader(":one: Performance of Bike Share Usage")

fig, ax = plt.subplots(1,2,figsize=(15, 4))

sns.lineplot(x='mnth',y='registered',data=main_df, label='Registered', marker='o', ax=ax[0])
sns.lineplot(x='mnth',y='casual',data=main_df, label='Casual', marker='o', ax=ax[0])

ax[0].set_title('Casual and Registered of Month')
ax[0].set_xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Des'])
ax[0].set_xlabel(None)
ax[0].set_ylabel("Average Registered and Casual Users")

sns.lineplot(x='mnth',y='cnt',data=main_df, hue='yr', marker='o', ax=ax[1])

ax[1].set_title('Bike Share Performance in Recent Years')
ax[1].set_xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Des'])
ax[1].set_xlabel(None)
ax[1].set_ylabel("Average of All Users")

year_dict = {0: 2011, 1: 2012}
handles, labels = ax[1].get_legend_handles_labels()
plt.legend(handles, [year_dict[int(label)] for label in labels])
st.pyplot(fig)

# Daily use

# Season
st.subheader(":two: Highest and Lowest Bike Share by Season")

fig, ax = plt.subplots(1,2,figsize=(15,4))

sns.countplot(x='season', data=main_df, ax=ax[0], palette=['#91C8E4','#91C8E4','#4682A9','#91C8E4'], width=0.5)

ax[0].set_title('Total Bike Share by Season')
ax[0].set_xticks([0 ,1, 2, 3], ['Spring', 'Summer', 'Fall', 'Winter'])  
ax[0].set_xlabel(None)
ax[0].set_ylabel(None)

sns.barplot(x='season',y='registered',data=main_df, label='Registered', color='#355C7D', ax=ax[1], width=0.5, errorbar=None)
sns.barplot(x='season',y='casual',data=main_df, label='Casual', color='#F67280', ax=ax[1], width=0.5, errorbar=None)

ax[1].set_title('Average Number of Bike Share by Season')
ax[1].set_xticks([0 ,1, 2, 3], ['Spring', 'Summer', 'Fall', 'Winter'])  
ax[1].set_xlabel(None)
ax[1].set_ylabel(None)

plt.legend()
st.pyplot(fig)

# Work day and Holiday
st.subheader(":three: Weekday and Holiday User Patterns")

fig, ax = plt.subplots(1,2,figsize=(15,4))

sns.barplot(x='workingday',y='registered',data=main_df, label='Registered', color='#355C7D', ax=ax[0], width=0.5, errorbar=None)
sns.barplot(x='workingday',y='casual',data=main_df, label='Casual', color='#F67280', ax=ax[0], width=0.5, errorbar=None)
ax[0].set_title('Casual and Registered on Working Day')
ax[0].set_xticks([0, 1], ['No', 'Working Day']) 
ax[0].set_xlabel(None)
ax[0].set_ylabel(None)

sns.barplot(x='holiday',y='registered',data=main_df, label='Registered', color='#355C7D', ax=ax[1], width=0.5, errorbar=None)
sns.barplot(x='holiday',y='casual',data=main_df, label='Casual', color='#F67280', ax=ax[1], width=0.5, errorbar=None)
ax[1].set_title('Casual and Registered on Holiday')
ax[1].set_xticks([0, 1], ['No', 'Holiday']) 
ax[1].set_xlabel(None)
ax[1].set_ylabel(None)

plt.legend()
st.pyplot(fig)

# Weekday
st.subheader(":four: The Most Crowded Day for Bike Share")

fig, ax = plt.subplots(1,2,figsize=(15,4))

sns.barplot(x='weekday', y='total_user', data=weekday_users_df, ax=ax[0], palette=['#91C8E4','#91C8E4','#91C8E4','#91C8E4','#91C8E4','#4682A9','#91C8E4'], width=0.5)

ax[0].set_title('Total Bike Share on Weekday')
ax[0].set_xticks([0 ,1, 2, 3, 4, 5, 6], ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])  
ax[0].set_xlabel(None)
ax[0].set_ylabel(None)

sns.barplot(x='weekday',y='registered',data=main_df, label='Registered', color='#355C7D', ax=ax[1], width=0.5, errorbar=None)
sns.barplot(x='weekday',y='casual',data=main_df, label='Casual', color='#F67280', ax=ax[1], width=0.5, errorbar=None)

ax[1].set_title('Average Number of Bike Share on Weekday')
ax[1].set_xticks([0 ,1, 2, 3, 4, 5, 6], ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])  
ax[1].set_xlabel(None)
ax[1].set_ylabel(None)

plt.legend(loc='upper left', fontsize=8)
st.pyplot(fig)

# Daily use
st.subheader(":five: Daily Use of Bike Share")

fig, ax = plt.subplots(figsize=(15,4))

sns.lineplot(x='hr', y='registered_user', data=hr_users_df, marker='o', label='Registered', ax=ax)
sns.lineplot(x='hr', y='casual_user', data=hr_users_df, marker='o', label='Casual', ax=ax)

ax.set_xticks(range(24))
ax.set_xticklabels(range(24))

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.set_title('Average Number of Bike Share by Time')

st.pyplot(fig)
