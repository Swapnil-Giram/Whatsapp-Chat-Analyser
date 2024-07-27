
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
from urlextract import URLExtract


def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # fetch no of msg
    num_messages = df.shape[0]

    # fetch no of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch no of media message
    num_media_messages = df[df['message'].str.strip() == '<Media omitted>'].shape[0]

    # fetch links shared in chat , first install the library from terminal
    # pip install urlextract
    extract = URLExtract()
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))


    return num_messages, len(words), num_media_messages, len(links)

def buesy_user(df):
    # for plot user
    dff = df[df['user']!='group_notification']
    x = dff['user'].value_counts().head()
    # for plot percent
    dff = round((dff['user'].value_counts()/dff.shape[0])*100,2).reset_index().rename(columns={'user':'name','count':'percent'})
    return x, dff

def create_wordcloud(Selected_user,df):
    with open('stop_hinglish.txt', 'r', encoding='utf-8') as f:
        stop_words = f.read().splitlines()
    stop_words = set(stop_words)

    if Selected_user != 'Overall':
        df = df[df['user'] == Selected_user]
    # define worldcloude
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):
    with open('stop_hinglish.txt', 'r', encoding='utf-8') as f:
        stop_words = f.read().splitlines()
    stop_words = set(stop_words)

    if selected_user!= 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month', 'month_num']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append((timeline['month'][i] + "-" + str(timeline['year'][i])))

    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    day_count = df['day_name'].value_counts().reset_index()
    return day_count

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    month_count = df['month'].value_counts().reset_index()
    return month_count

