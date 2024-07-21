import re
import pandas as pd

def preprocess(chat_content):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, chat_content)[1:]
    dates = re.findall(pattern, chat_content)

    df = pd.DataFrame({'User_message': messages, 'Date': dates})
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y, %H:%M - ')

    # seperate user and message
    users = []
    messages = []
    for message in df['User_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['User_message'], inplace=True)

    df['only_date'] = df['Date'].dt.date
    df['year'] = df['Date'].dt.year
    df['month_num'] = df['Date'].dt.month
    df['month'] = df['Date'].dt.strftime('%B')
    df['day'] = df['Date'].dt.day
    df['day_name'] = df['Date'].dt.day_name()
    df['hour'] = df['Date'].dt.hour
    df['minute'] = df['Date'].dt.minute

    return df




