import mysql.connector 
import pandas as pd
#import psycopg2
import streamlit as st
import PIL 
from PIL import Image
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import requests
import geopandas as gpd
# connect to the database
import mysql.connector
import seaborn as sns
from matplotlib.animation import FuncAnimation
#establishing the connection
conn = mysql.connector.connect(user='root', password='password', host='127.0.0.1', database="database")

# create a cursor object
cursor = conn.cursor()


#with st.sidebar:
SELECT = option_menu(
    menu_title = None,
    options = ["About","Home","Basic insights","Contact"],
    icons =["bar-chart","house","toggles","at"],
    default_index=2,
    orientation="horizontal",
    styles={"container": {"padding": "0!important", "background-color": "white","size":"cover", "width": "100%"},
        "icon": {"color": "red", "font-size": "20px"},
        "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "orange"},
        "nav-link-selected": {"background-color": "green"}})
     

#---------------------Basic Insights -----------------#


if SELECT == "Basic insights":
    st.title("BASIC INSIGHTS")
    #st.write("SAMUELS PROJECT")
    st.subheader("Let's know some basic insights about the data")
    options = ["--select--",
               "Top 10 states based on year and amount of transaction",
               "List 10 states based on type and amount of transaction",
               "Top 5 Transaction_Type based on Transaction_Amount",
               "Top 10 Registered-users based on States and District",
               "Top 10 Districts based on states and Count of transaction",
               "List 10 Districts based on states and amount of transaction",
               "List 10 Transaction_Count based on Districts and states",
               "Top 10 RegisteredUsers based on states and District"]
    
               #1
               
    select = st.selectbox("Select the option",options)
    if select=="Top 10 states based on year and amount of transaction":
        cursor.execute("SELECT DISTINCT State, Year, SUM(Transaction_amount) AS Total_Transaction_Amount FROM top_trans_pin GROUP BY State, Year ORDER BY Total_Transaction_Amount DESC LIMIT 10");
        
        df = pd.DataFrame(cursor.fetchall(), columns=['States','Transaction_Year', 'Transaction_Amount'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            #st.title("Top 10 states and amount of transaction - Line Chart")
            st.line_chart(data=df.set_index('States')['Transaction_Amount'])
            
            #2
            
    elif select=="List 10 states based on type and amount of transaction":
        cursor.execute("SELECT DISTINCT State, SUM(Transaction_count) as Total FROM top_trans_pin GROUP BY State ORDER BY Total ASC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns=['State','Total_transaction'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            #st.title("List 10 states based on type and amount of transaction - Custom Plot")
            plt.figure(figsize=(10, 6))
            sns.barplot(data=df, x='State', y='Total_transaction', palette='coolwarm')
            plt.xticks(rotation=45, ha='right')
            plt.xlabel('States')
            plt.ylabel('Total Transaction')
            st.pyplot(plt)


            
            #3
            
    elif select == "Top 5 Transaction_Type based on Transaction_Amount":
        cursor.execute("SELECT DISTINCT Transaction_type, SUM(Transaction_amount) AS Amount FROM agg_trans GROUP BY Transaction_type ORDER BY Amount DESC LIMIT 5")
        df = pd.DataFrame(cursor.fetchall(), columns=['Transaction_Type', 'Transaction_Amount'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.bar_chart(data=df, y="Transaction_Type", x="Transaction_Amount")
  
            
            
           #4
            
    elif select=="Top 10 Registered-users based on States and District":
        cursor.execute("SELECT DISTINCT State, District, SUM(Registered_users) AS Users FROM top_user_dist GROUP BY State, District ORDER BY Users DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns=['State','District','RegisteredUsers'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            fig = px.treemap(df, path=['State', 'District'], values='RegisteredUsers')
            st.plotly_chart(fig)
            

            #5
            
    elif select=="Top 10 Districts based on states and Count of transaction":
        cursor.execute("SELECT DISTINCT State,District,SUM(Transaction_count) AS Counts FROM top_trans_dist GROUP BY State,District ORDER BY Counts DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns=['State','District','Transaction_count'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            #st.title("Top 10 Districts based on states and Count of transaction")
            fig = px.sunburst(df, path=['State', 'District'], values='Transaction_count')
            fig.update_traces(textinfo='label+percent entry')
            fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
            st.plotly_chart(fig)


            
            #6
            
    elif select=="List 10 Districts based on states and amount of transaction":
        cursor.execute("SELECT DISTINCT State, year,SUM(Transaction_amount) AS Amount FROM agg_trans GROUP BY State, year ORDER BY Amount ASC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns=['State','year','Transaction_amount'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            #st.title("Least 10 Districts based on states and amount of transaction")
            plt.figure(figsize=(10, 6))
            sns.barplot(data=df, x='State', y='Transaction_amount', ci=None, estimator=min)
            plt.xlabel('State')
            plt.ylabel('Transaction Amount')
            plt.title('Least 10 Districts Based on States and Transaction Amount')
            plt.legend(title='District', loc='upper right')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(plt)


            
            
           #7
            
    elif select=="List 10 Transaction_Count based on Districts and states":
        cursor.execute("SELECT DISTINCT State, District, SUM(Transaction_count) AS Counts FROM map_trans GROUP BY State,District ORDER BY Counts DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns=['States','District','Transaction_Count'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            plt.figure(figsize=(8, 8))
            plt.pie(df.groupby('States')['Transaction_Count'].sum(), labels=df['States'].unique(), autopct='%1.1f%%', shadow=True)
            plt.title('Top 10 Transaction Counts Based on States')
            plt.tight_layout()
            st.pyplot(plt)

            
            
            
            #8
             
    elif select=="Top 10 RegisteredUsers based on states and District":
        cursor.execute("SELECT DISTINCT State,District, SUM(Registered_users) AS Users FROM map_user GROUP BY State,District ORDER BY Users DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns = ['States','District','RegisteredUsers'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            #st.title("Top 10 RegisteredUsers based on states and District")
            plt.figure(figsize=(10, 6))
            sns.barplot(data=df, x='States', y='RegisteredUsers', hue='District')
            plt.xlabel('States')
            plt.ylabel('Registered Users')
            plt.legend(title='District', loc='upper right')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(plt)



#----------------Home----------------------#
cursor = conn.cursor()

# execute a SELECT statement
cursor.execute("SELECT * FROM agg_trans")

# fetch all rows
rows = cursor.fetchall()
from streamlit_extras.add_vertical_space import add_vertical_space

if SELECT == "Home":
    col1,col2, = st.columns(2)
    #col1.image(Image.open("C:\Users\morle\Downloads\phonepe-logo.png"), width = 500)#C:\Users\morle\Downloads\phonepe-logo.png
    col1.image(Image.open("C:\\Users\\morle\\Downloads\\phonepe-logo.png"), width=500)

    with col1:
        st.subheader("PhonePe  is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. It is owned by Flipkart, a subsidiary of Walmart.")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.video("C:\\Users\\morle\\Downloads\\PhonePe_bike_insurance_ah_verum_1.50_roobaiku_perunga.__VJ32fT89sJI_247.webm")
        
    st.subheader(':blue[Registered Users Hotspots - States]')


    

    
      
      
    Data_Aggregated_Transaction_df= pd.read_csv(r'C:\phonepe\Phonepe_Pulse_Data_Visualization/Data_Aggregated_Transaction_Table.csv')
    Data_Aggregated_User_Summary_df= pd.read_csv(r'C:\phonepe\Phonepe_Pulse_Data_Visualization/Data_Aggregated_User_Summary_Table.csv')
    Data_Aggregated_User_df= pd.read_csv(r'C:\phonepe\Phonepe_Pulse_Data_Visualization/Data_Aggregated_User_Table.csv')
    Scatter_Geo_Dataset =  pd.read_csv(r'C:\phonepe\Phonepe_Pulse_Data_Visualization/Data_Map_Districts_Longitude_Latitude.csv')
    Coropleth_Dataset =  pd.read_csv(r'C:\phonepe\Phonepe_Pulse_Data_Visualization/Data_Map_IndiaStates_TU.csv')
    Data_Map_Transaction_df = pd.read_csv(r'C:\phonepe\Phonepe_Pulse_Data_Visualization/Data_Map_Transaction_Table.csv')
    Data_Map_User_Table= pd.read_csv(r'C:\phonepe\Phonepe_Pulse_Data_Visualization/Data_Map_User_Table.csv')
    Indian_States= pd.read_csv(r'C:\phonepe\Phonepe_Pulse_Data_Visualization/Longitude_Latitude_State_Table.csv')
    
    c1,c2=st.columns(2)
    with c1:
        Year = st.selectbox(
                'Please select the Year',
                ('2018', '2019', '2020','2021','2022'))
    with c2:
        Quarter = st.selectbox(
                'Please select the Quarter',
                ('1', '2', '3','4'))
    year=int(Year)
    quarter=int(Quarter)
    
    Transaction_scatter_districts=Data_Map_Transaction_df.loc[(Data_Map_Transaction_df['Year'] == year ) & (Data_Map_Transaction_df['Quarter']==quarter) ].copy()
    Transaction_Coropleth_States=Transaction_scatter_districts[Transaction_scatter_districts["State"] == "india"]
    Transaction_scatter_districts.drop(Transaction_scatter_districts.index[(Transaction_scatter_districts["State"] == "india")],axis=0,inplace=True)
    # Dynamic Scattergeo Data Generation
    
    Transaction_scatter_districts = Transaction_scatter_districts.sort_values(by=['Place_Name'], ascending=False)
    Scatter_Geo_Dataset = Scatter_Geo_Dataset.sort_values(by=['District'], ascending=False) 
    Total_Amount=[]
    for i in Transaction_scatter_districts['Total_Amount']:
        Total_Amount.append(i)
    Scatter_Geo_Dataset['Total_Amount']=Total_Amount
    Total_Transaction=[]
    for i in Transaction_scatter_districts['Total_Transactions_count']:
        Total_Transaction.append(i)
    Scatter_Geo_Dataset['Total_Transactions']=Total_Transaction
    Scatter_Geo_Dataset['Year_Quarter']=str(year)+'-Q'+str(quarter)
    # Dynamic Coropleth
    
    Coropleth_Dataset = Coropleth_Dataset.sort_values(by=['state'], ascending=False)
    Transaction_Coropleth_States = Transaction_Coropleth_States.sort_values(by=['Place_Name'], ascending=False)
    Total_Amount=[]
    for i in Transaction_Coropleth_States['Total_Amount']:
        Total_Amount.append(i)
    Coropleth_Dataset['Total_Amount']=Total_Amount
    Total_Transaction=[]
    for i in Transaction_Coropleth_States['Total_Transactions_count']:
        Total_Transaction.append(i)
    Coropleth_Dataset['Total_Transactions']=Total_Transaction 
    
    
    
    
    #scatter plotting the states codes 
    Indian_States = Indian_States.sort_values(by=['state'], ascending=False)
    Indian_States['Registered_Users']=Coropleth_Dataset['Registered_Users']
    Indian_States['Total_Amount']=Coropleth_Dataset['Total_Amount']
    Indian_States['Total_Transactions']=Coropleth_Dataset['Total_Transactions']
    Indian_States['Year_Quarter']=str(year)+'-Q'+str(quarter)
    fig=px.scatter_geo(Indian_States,
                        lon=Indian_States['Longitude'],
                        lat=Indian_States['Latitude'],                                
                        text = Indian_States['code'], #It will display district names on map
                        hover_name="state", 
                        hover_data=['Total_Amount',"Total_Transactions","Year_Quarter"],
                        )
    fig.update_traces(marker=dict(color="white" ,size=0.3))
    fig.update_geos(fitbounds="locations", visible=False,)
    # scatter plotting districts
    Scatter_Geo_Dataset['col']=Scatter_Geo_Dataset['Total_Transactions']
    fig1=px.scatter_geo(Scatter_Geo_Dataset,
                        lon=Scatter_Geo_Dataset['Longitude'],
                        lat=Scatter_Geo_Dataset['Latitude'],
                        color=Scatter_Geo_Dataset['col'],
                        size=Scatter_Geo_Dataset['Total_Transactions'],     
                    #text = Scatter_Geo_Dataset['District'], #It will display district names on map
                        hover_name="District", 
                        hover_data=["State", "Total_Amount","Total_Transactions","Year_Quarter"],
                        title='District',
                        size_max=22)
    
    fig1.update_traces(marker=dict(color="green" ,line_width=1))    #rebeccapurple
#coropleth mapping india
    fig_ch = px.choropleth(
                        Coropleth_Dataset,
                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',                
                        locations='state',
                        color="Total_Transactions",                                       
                        )
    fig_ch.update_geos(fitbounds="locations", visible=False,)
#combining districts states and coropleth
    fig_ch.add_trace( fig.data[0])
    fig_ch.add_trace(fig1.data[0])
    st.write("### **:blue[PhonePe India Map]**")
    colT1,colT2 = st.columns([8,4])
    with colT1:
        st.plotly_chart(fig_ch, use_container_width=True)
    with colT2:
        st.info(
        """
        Details of Map:
        - The darkness of the state color represents the total transactions
        - The Size of the Circles represents the total transactions dictrict wise
        - The bigger the Circle the higher the transactions
        - Hover data will show the details like Total transactions, Total amount
        """
        )
        st.info(
        """
        Important Observations:
        - User can observe Transactions of PhonePe in both statewide and Districtwide.
        - We can clearly see the states with highest transactions in the given year and quarter
        - We get basic idea about transactions district wide
        """
        )
# -----------------------------------------------FIGURE2 HIDDEN BARGRAPH------------------------------------------------------------------------
    Coropleth_Dataset = Coropleth_Dataset.sort_values(by=['Total_Transactions'])
    fig = px.bar(Coropleth_Dataset, x='state', y='Total_Transactions',title=str(year)+" Quarter-"+str(quarter))
    with st.expander("See Bar graph for the same data"):
        st.plotly_chart(fig, use_container_width=True)
        st.info('**:blue[The above bar graph showing the increasing order of PhonePe Transactions according to the states of India, Here we can observe the top states with highest Transaction by looking at graph]**')

    
    
#----------------About-----------------------#

if SELECT == "About":
    col1,col2 = st.columns(2)
    with col1:
        st.video("C:\\Users\\morle\\Downloads\\PhonePe BikeInsurance Tamil.mkv")
    with col2:
        st.image(Image.open("C:\\Users\\morle\\Downloads\\phonepe-logo.png"),width = 500)
        st.write("---")
        st.subheader("The Indian digital payments story has truly captured the world's imagination."
                 " From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones, mobile internet and states-of-the-art payments infrastructure built as Public Goods championed by the central bank and the government."
                 " Founded in December 2015, PhonePe has been a strong beneficiary of the API driven digitisation of payments in India. When we started, we were constantly looking for granular and definitive data sources on digital payments in India. "
                 "PhonePe Pulse is our way of giving back to the digital payments ecosystem.")
    st.write("---")
    col1,col2 = st.columns(2)
    with col1:
        st.title("THE BEAT OF PHONEPE")
        st.write("---")
        st.subheader("Phonepe became a leading digital payments company")
        st.image(Image.open("C:\\phonepe\\Phonepe_Pulse_Data_Visualization//top.jpeg"),width = 400)
        with open("C:\phonepe\Phonepe_Pulse_Data_Visualization/annual report.pdf","rb") as f:
            data = f.read()
        st.download_button("DOWNLOAD REPORT",data,file_name="annual report.pdf")
    with col2:
        st.image(Image.open("C:\\phonepe\\Phonepe_Pulse_Data_Visualization//report.jpeg"),width = 800)

        st.caption("Made 🤩 by @samuelsamraj")
#----------------------Contact---------------#


if SELECT == "Contact":
    name = "Samuel Samraj"
    mail = (f'{"Mail :"}  {"morlensamuels@gmail.com"}')
    description = "An Aspiring DATA-SCIENTIST..!"
    social_media = {
        
        "GITHUB": "https://github.com/Samuelsamraj/phone_pulse#phone_pulse",
        "LINKEDIN": "https://www.linkedin.com/in/samuel-samraj-28a25a241"}
        
    
    col1, col2 = st.columns(2)
    
    with col2:
        st.title('Phonepe Pulse data visualisation')
        st.write("The goal of this project is to extract data from the Phonepe pulse Github repository, transform and clean the data, insert it into a MySQL database, and create a live geo visualization dashboard using Streamlit and Plotly in Python. The dashboard will display the data in an interactive and visually appealing manner, with at least 10 different dropdown options for users to select different facts and figures to display. The solution must be secure, efficient, and user-friendly, providing valuable insights and information about the data in the Phonepe pulse Github repository.")
        st.write("---")
        st.subheader(mail)
    st.write("#")
    cols = st.columns(len(social_media))
    for index, (platform, link) in enumerate(social_media.items()):
        cols[index].write(f"[{platform}]({link})")


