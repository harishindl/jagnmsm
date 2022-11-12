import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import tweepy
from langdetect import detect
from PIL import Image
import tweepy
import re
from time import time, sleep
import time
import datetime


keyowrd = "JaganannaMosam"
im = Image.open("icon.ico")
st.set_page_config(
    page_title="#JaganannaMosam Realtime Analysis",
    page_icon=im,
    layout="wide",
)


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.markdown("<h1 style='text-align: center; color: Red;'>#JaganannaMosam Realtime Analysis</h1>", unsafe_allow_html=True)

url = "JaganannaMosam_citywise.csv"
df_assembly = pd.read_csv(url)
df_assembly[['latitude', 'longitude']] = df_assembly['coords'].str.split(',', n=1, expand=True)

url = "JaganannaMosam_all_tweets.csv"
df_all = pd.read_csv(url)
df_all_filtered = df_all[df_all.Username != "JanaSenaParty"]
df_all_Janasenaparty = df_all[df_all.Username == "JanaSenaParty"]
#userdf = df_all.drop_duplicates(subset=['Username'])
#TotalReach = userdf['followers'].sum()  
url = "JaganannaMosam_all_tweets_inclretweets.csv"
df_reach = pd.read_csv(url)
userdf = df_reach.drop_duplicates(subset=['Username'])
TotalReach = userdf['followers'].sum()  


def human_format(num):
    num = float('{:.4g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'Million', 'Billion', 'Trillion'][magnitude])
    
    
TotalReach_humanreadable = human_format(TotalReach)




#convert time column to a list, sort it and get count time wise
#df_all['Date'] = df_all['Date'].apply(lambda x: sorted(literal_eval(x)))
uniquetweetlist = df_all['Date'].values.tolist()
uniquetweetlist.sort()
count = 0
countlist = []
adjusted_timezone = []
for element in uniquetweetlist:
    clean_timestamp = datetime.datetime.strptime(element, '%Y-%m-%d %H:%M:%S%z')
    local_timestamp = clean_timestamp + datetime.timedelta(hours=5.5)
    final_timestamp = datetime.datetime.strftime(local_timestamp, '%Y-%m-%d %H:%M:%S%z')
    count += 1
    adjusted_timezone.append(final_timestamp)
    countlist.append(count)

#count likes, retweets and replies        
TotalRetweets = df_all['Likes'].sum()
TotalLikes = df_all['retweets'].sum()      
TotalReplies = df_all['replies'].sum()  
TotalTweets = TotalRetweets+count+TotalReplies
#TotalReach = TotalRetweets+count+TotalReplies + TotalLikes
totinklreplies = int(count+TotalReplies)


#sort tweets by likes and replies from Janasenaparty

popularbylikes_jsp_df_sorted = df_all_Janasenaparty.sort_values(by=['Likes'], ascending=False)
jspuniquetweetlist = popularbylikes_jsp_df_sorted['Date'].values.tolist()
jspadjusted_timezone = []
for element in jspuniquetweetlist:
    jspclean_timestamp = datetime.datetime.strptime(element, '%Y-%m-%d %H:%M:%S%z')
    jsplocal_timestamp = jspclean_timestamp + datetime.timedelta(hours=5.5)
    jspfinal_timestamp = datetime.datetime.strftime(jsplocal_timestamp, '%Y-%m-%d %H:%M:%S%z')
    jspadjusted_timezone.append(jspfinal_timestamp)
popularbylikes_jsp_df_sorted['date'] = jspadjusted_timezone
popularbylikes_jsp_df_sorted['date'] = popularbylikes_jsp_df_sorted['date'].str.slice(0,16)
popularbylikes_jsp_df = popularbylikes_jsp_df_sorted[['Username', 'Tweet', 'Likes', 'retweets', 'replies', 'date']]
#popularbyretweets_jsp_df = df_all_Janasenaparty.sort_values(by=['retweets'], ascending=False)

#sort tweets by likes and replies
popularbylikes_df = df_all_filtered.sort_values(by=['Likes'], ascending=False)
popularbyretweets_df = df_all_filtered.sort_values(by=['retweets'], ascending=False)

#create new dataframe only with tweets and usernames
popularbylikes_df_new = popularbylikes_df[['Username', 'Tweet', 'Likes']]
popularbyretweets_df_new = popularbyretweets_df[['Username', 'Tweet', 'retweets']]

        

query = "#JaganannaMosam"
client = tweepy.Client("AAAAAAAAAAAAAAAAAAAAAGWQdAEAAAAATwVFp%2F8bcVxHisSiMnJ%2FukElwXs%3D2uvxeEZp4FznlpGaOV4n3Adx5Yi5s84XM2c1nkbGMHqPsDJyC7")
counts = client.get_recent_tweets_count(query=query, start_time= "2022-11-10T00:00:00.000Z", granularity='hour')
hour = []
tweet_count = []
minutes = []
timearray = []
hour1 = []
tweet_count1 = []
minutes1 = []
timearray1 = []
hour2 = []
tweet_count2 = []
minutes2 = []
timearray2 = []

for i in counts.data:
    hr = re.search('T(.*?):', i["start"])
    hr = int(hr.group(1))+5
    if(hr >= 24): hr = hr-24
    #if(hr ==3): hr = 0
    minute = re.search(':(.*?):', i["start"])
    minute = int(minute.group(1))
    minute = minute + 30
    if(minute >= 60):                                
        minute = minute-60 
        hr = hr+1
    #if(minute == 60): minute = "00"
    #print(hr, i["tweet_count"])
    hour.append(hr)
    minutes.append(minute)
    time = str(hr) + ":" + str(minute)
    time_new = i["start"]
    clean_timestamp = datetime.datetime.strptime(i["start"], '%Y-%m-%dT%H:%M:%S.%f%z')
    local_timestamp = clean_timestamp + datetime.timedelta(hours=5.5)
    final_timestamp = datetime.datetime.strftime(local_timestamp, '%Y-%m-%dT%H:%M:%S.%f%z')
    #final_timestamp = datetime.datetime.strptime(i["start"], '%Y-%m-%dT%H:%M:%S.%f%z').astimezone(ZoneInfo('Asia/Hyderabad')).datetime.datetime.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    #offset_hours = +5.5 #offset in hours for EST timezone

    #account for offset from UTC using timedelta                                
    #local_timestamp = clean_timestamp + datetime.timedelta(hours=offset_hours)

    #final_timestamp =  datetime.datetime.strftime(local_timestamp, 
    #                '%Y-%m-%d %I:%M:%S %p')  
    print(final_timestamp)
    timearray2.append(final_timestamp)
    timearray.append(time)
    #print(time + ',' + str(i["tweet_count"]))
    tweet_count.append(i["tweet_count"])
    total = sum(tweet_count)
    #print(counts.data)


df = pd.DataFrame(list(zip((timearray), tweet_count)),
            columns =['Time', 'Volume'])
df_with_time = pd.DataFrame(list(zip((timearray2), tweet_count)),
            columns =['Time', 'Volume'])
st.title('Tweet Volume Till Now (Including Retweets):  ' + str(int(TotalTweets)))
st.title('Potential Reach:  ' + str(TotalReach_humanreadable))
fig7 = go.Figure()
fig7.add_trace(go.Scatter(x=timearray2, y=tweet_count, marker_color='indianred', text="counts", fill='tozeroy'))
fig7.update_layout(plot_bgcolor='rgba(255,255,255,0)')
fig7.update_layout({
                "xaxis": {"title":"Day"},
                "yaxis": {"title":"Total tweets"},
                "showlegend": False}, height = 500)
st.plotly_chart(fig7, use_container_width=True)

df.to_csv("JaganannaMosam_Tweetvolume_03092022.csv")
df_with_time.to_csv("JaganannaMosam_Tweetvolume_with_date.csv")


#print(uniquetweetlist)
#print(countlist)
st.title('Tweet Volume Till Now (Only Unique Tweets inkl. replies):  ' + str(totinklreplies))
fig8 = go.Figure()
fig8.add_trace(go.Scatter(x=adjusted_timezone, y=countlist, marker_color='red', text="counts", fill='tozeroy'))
fig8.update_layout(plot_bgcolor='rgba(255,255,255,0)')
fig8.update_layout({
                "xaxis": {"title":"Day"},
                "yaxis": {"title":"Total tweets"},
                "showlegend": False}, height = 500)
st.plotly_chart(fig8, use_container_width=True)

#piechart
labels = ['Likes', 'Retweets', 'Replies' ]
values = [str(TotalLikes), str(TotalRetweets), str(TotalReplies)]
fig9 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
#fig9.update_traces(textinfo=values)
fig9.update_traces(hoverinfo='label+percent', textinfo='label + value', textfont_size=20)
fig9.update_layout(showlegend=False)
st.plotly_chart(fig9, use_container_width=True)


st.title('Top Tweets By Retweets')
fig10 = go.Figure(data=[go.Table(
    header=dict(values=list(popularbyretweets_df_new.columns),
                fill_color='red',
                font=dict(color='white', family="Lato", size=20),
                align='left'),
    cells=dict(values=[popularbyretweets_df_new.Username.head(10),  popularbyretweets_df_new.Tweet.head(10), popularbyretweets_df_new.retweets.head(10)],
               fill_color='white',
               align='left'))
])
st.plotly_chart(fig10, use_container_width=True)
#########################################
st.title('Top Tweets By Likes')
fig11 = go.Figure(data=[go.Table(
    header=dict(values=list(popularbylikes_df_new.columns),
                fill_color='red',
                font=dict(color='white', family="Lato", size=20),
                align='left'),
    cells=dict(values=[popularbylikes_df_new.Username.head(10),  popularbylikes_df_new.Tweet.head(10), popularbylikes_df_new.Likes.head(10)],
               fill_color='white',
               align='left'))
])
st.plotly_chart(fig11, use_container_width=True)
#########################################
st.title('Top Tweets By Official Handle')
fig11 = go.Figure(data=[go.Table(
    header=dict(values=list(popularbylikes_jsp_df.columns),
                fill_color='red',
                font=dict(color='white', family="Lato", size=20),
                align='left'),
    cells=dict(values=[popularbylikes_jsp_df.Username.head(10),  popularbylikes_jsp_df.Tweet.head(10), popularbylikes_jsp_df.Likes.head(10), popularbylikes_jsp_df.retweets.head(10), popularbylikes_jsp_df.replies.head(10), popularbylikes_jsp_df.date.head(10)],
               fill_color='white',
               align='left'))
])
st.plotly_chart(fig11, use_container_width=True)


df_assembly['placetemp'] = df_assembly['place']
df_assembly1 = pd.DataFrame()
df_assembly2 = pd.DataFrame()

df_assembly1 = df_assembly["place"].value_counts().rename_axis('citycount').reset_index(name='counts')
df_assembly2 = df_assembly.groupby('placetemp').nth(0)

df_assembly2['tweetcount'] = df_assembly["placetemp"].value_counts()
df_assembly2 = df_assembly2.sort_values(by=['tweetcount'], ascending=False)

df_assembly3 = df_all.groupby('Username').nth(0)
df_assembly3['tweetcount'] = df_all['Username'].value_counts()
df_assembly3 = df_assembly3.sort_values(by=['tweetcount'], ascending=False)
df_assembly3 = df_assembly3.reset_index()
#df_assembly3_filtered = df_all[df_all.Username != "JanaSenaParty"]

#print(df_assembly3.head(10))




#df_assembly2.to_csv('test.csv')
#print(df_assembly2.head(50))
#print(df_assembly["place"].value_counts().head(50))



fig_city1 = px.density_mapbox(df_assembly2, lat='latitude', lon='longitude', radius=20,hover_name="place", hover_data=['tweetcount'],
                        center=dict(lat=18, lon=80), zoom=5,
                        mapbox_style="open-street-map")
                        
fig_city2 = px.scatter_mapbox(df_assembly2, lat="latitude", lon="longitude", hover_name="place", hover_data=['tweetcount'],
                        color_discrete_sequence=["fuchsia"], center=dict(lat=18, lon=80), zoom=5)
fig_city2.update_layout(mapbox_style="open-street-map")
fig_city2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

fig_city3 = px.scatter_geo(df_assembly2, lat="latitude", lon="longitude", color="tweetcount",
                     hover_name="place", size="tweetcount",
                     projection="natural earth2")
fig_city4 = px.bar(df_assembly2, y='tweetcount', x='place',color="tweetcount", color_continuous_scale=px.colors.sequential.Rainbow)



st.title('Assembly wise tweets (Geocoded tweets)')
mapselect = st.selectbox('Pick assembly',["Bar graph", "Scatter Map", "Tweet Density Map", "Bubble Map"])


if(mapselect == "Bar graph"):
    st.plotly_chart(fig_city4, use_container_width=True)
elif(mapselect == "Scatter Map"):
    st.plotly_chart(fig_city2, use_container_width=True)
elif(mapselect == "Tweet Density Map"):
    st.plotly_chart(fig_city1, use_container_width=True)
elif(mapselect == "Bubble Map"):
    st.plotly_chart(fig_city3, use_container_width=True)
elif(mapselect == "Bar graph"):
    st.plotly_chart(fig_city4, use_container_width=True)
    




    
st.markdown("<h1 style='text-align: center; color: Green;'>TOP 10 By Tweet Counts</h1>", unsafe_allow_html=True) 
col1, col2, col3 = st.columns(3)
#print(df_assembly2.head(10))
df_topassemblies = df_assembly2[['place']]
#print(df_topassemblies.head(10))

fig15 = go.Figure(data=[go.Table(
    header=dict(values=list(df_topassemblies),
                fill_color='red',
                font=dict(color='white', family="Lato", size=20),
                align='center'),
    cells=dict(values=[df_topassemblies.place.head(10)],
               font=dict(color='black', family="Lato", size=10),
               fill_color='white',
               align='center'))
])

#print(df_assembly3.head(10))
df_toptweeters = df_assembly3[['Username']]
df_toptweeters_filtered = df_toptweeters[df_toptweeters.Username != "JanaSenaParty"]
print(df_toptweeters.head(10))

fig16 = go.Figure(data=[go.Table(
    header=dict(values=list(df_toptweeters_filtered),
                fill_color='red',
                font=dict(color='white', family="Lato", size=20),
                align='center'),
    cells=dict(values=[df_toptweeters_filtered.Username.head(10)],
               font=dict(color='black', family="Lato", size=10),
               fill_color='white',
               align='center'))
])

   
col1, col2= st.columns(2)


with col1:
    st.markdown("<h1 style='text-align: center; color: red;'>Top 10 Assemblies</h1>", unsafe_allow_html=True)
    st.plotly_chart(fig15, use_container_width=True)

with col2:
    st.markdown("<h1 style='text-align: center; color: red;'>Top 10 Tweeters</h1>", unsafe_allow_html=True)
    st.plotly_chart(fig16, use_container_width=True)





















#for count in tweet_count:
#    y = np.random.random()
#    fig = plt.scatter(timearray, tweet_count)
#    plt.pause(0.05)
#
#st.pyplot(fig)




#Get Trends and display them

# initialize api instance
consumer_key= "XUupwjsza5gFrB0DRtNYCrIm2"
consumer_secret= "iNhjQy5HTpjnCy0NpNDb0qSVU5QQuJLcbAUGv5arDOaKpeNBqo"
access_token="2567031788-Rkkd80XwQfEMYady39aAKIZmq38FFAlfYV5tBjZ"
access_token_secret ="KzoKMtZ5Lx3M8Ej1GlT6IN96NHljhEUaU7x7VevmZWnDl"

#Connect to Twitter through the API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
auth.set_access_token(access_token, access_token_secret) 
api = tweepy.API(auth,wait_on_rate_limit=True)

#{'name': 'Worldwide',
#'placeType': {'code': 19, 'name': 'Supername'},
#'url': 'http://where.yahooapis.com/v1/place/1',
#'parentid': 0,
#'country': '',
#'woeid': 2295237,
#'countryCode': None}


#st.title("Rythubharosa Realtime Analysis")    
#st.header("All Tweets")               
placeholder = st.empty()



for val in api.available_trends():
    if val['country'] == 'India':
        pass
        #print(val.values())
        
def get_woeid(place):
    '''Get woeid by location'''
    try:
        trends = api.available_trends()
        for val in trends:
            if (val['name'].lower() == place.lower()):
                return(val['woeid']) 
        print('Location Not Found')
    except Exception as e:
        print('Exception:',e)
        return(0)
def get_trends_by_location(loc_id,count):
    '''Get Trending Tweets by Location'''
    import iso639
    try:
        trends = api.get_place_trends(loc_id)
        df = pd.DataFrame([trending['name'],  trending['tweet_volume'], iso639.to_name(detect(trending['name']))] for trending in trends[0]['trends'])
        df.columns = ['Trends','Volume','Language']
        #df = df.sort_values('Volume', ascending = False)
        return(df[:count])
    except Exception as e:
        print("Error please refresh",e)
        
        

df_india_trends = get_trends_by_location(23424848, 200)
#df_india_trends = api.get_place_trends(23424848)

col1, col2 = st.columns(2)



st.title("Trending Now")
df_trending = df_india_trends


st.title("Top 10 trending hashtags now") 
st.write(df_trending['Trends'].head(50))

#st.title("Top Tweets by retweets")
if df_trending['Trends'].str.contains('JaganannaMosam').any():
    #st.markdown("<h1 style='text-align: center; color: Green;'>Is Trending Now</h1>", unsafe_allow_html=True)
    #rank = len(df_trending[df_trending["Trends"]=="Jaganannamosam"].values)
    trends_list = df_trending['Trends'].tolist()
    rank = trends_list.index("#JaganannaMosam")
    
    st.markdown("""
  #### "Is trending now with India wide rank: <span style="color:blue">{temp1}</span>"   
""".format(temp1=rank))
else:
    st.text(" ")
    st.text(" ")
    st.text(" ")
    st.text(" ")
    st.text(" ")
    st.text(" ")
    st.text(" ")
    st.text(" ")
    st.text(" ")
    st.text(" ")
    st.text(" ")
    st.text(" ")
    st.markdown("<h1 style='text-align: center; color: Orange;'>#JaganannaMosam</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: Red;'>Hashtag Not Trending Yet</h1>", unsafe_allow_html=True)
 
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.markdown('Proudly created for Janasena✊')
