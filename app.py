import streamlit as st
import plotly.express as px
import pandas as pd
import requests
from PIL import Image
import io
import base64



@st.experimental_memo
def get_chart_dist(response_dic):
    dist_player1 = response_dic['distance']["last_frame_distance_player1"]
    dist_player2 = response_dic['distance']["last_frame_distance_player2"]

    stages = ["Running Distance"]
    df_mtl = pd.DataFrame(dict(number=[dist_player1], stage=stages))
    df_mtl['Player'] = 'Player 1'
    df_toronto = pd.DataFrame(dict(number=[dist_player2], stage=stages))
    df_toronto['Player'] = 'Player 2'
    df = pd.concat([df_mtl, df_toronto], axis=0)
    fig = px.funnel(df, x='number', y='stage', color='Player')

    tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
    with tab1:
        st.plotly_chart(fig, theme="streamlit")
    with tab2:
        st.plotly_chart(fig, theme=None)

@st.experimental_memo
def get_chart_strokes(response_dic):
    services_player1 = response_dic.get('stroke_counts').get("Service/Smash")
    backhand_player1 = response_dic.get('stroke_counts').get("Backhand")
    forehand_player1 = response_dic.get('stroke_counts').get("Forehand")
    services_player2 = response_dic.get('stroke_counts').get("Service/Smash")
    backhand_player2 = response_dic.get('stroke_counts').get("Backhand")
    forehand_player2 = response_dic.get('stroke_counts').get("Forehand")

    stages = ["Services", "Forehands", "Backhands"]
    df_mtl = pd.DataFrame(dict(number=[services_player1, forehand_player1, backhand_player1], stage=stages))
    df_mtl['Player'] = 'Player 1'
    df_toronto = pd.DataFrame(dict(number=[services_player2, forehand_player2, backhand_player2], stage=stages))
    df_toronto['Player'] = 'Player 2'
    df = pd.concat([df_mtl, df_toronto], axis=0)
    fig = px.funnel(df, x='number', y='stage', color='Player')

    tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
    with tab1:
        st.plotly_chart(fig, theme="streamlit")
    with tab2:
        st.plotly_chart(fig, theme=None)




'''
# Tennis vision
'''

st.markdown('''
*The future of tennis*

Full profesionnal stats on your phone!
''')

'''
## Please download your video here

'''
video_file = st.file_uploader("Choose a 🎾 mp4 video file ", type=["mp4", "avi", "mov", "mkv"])

if video_file is not None:
    files = {"file": video_file.getvalue()}
    res = requests.post('http://104.155.13.104:8000/savefile', files=files)
    if res.ok:
        response = res.json()
        video_data = response.get('video', '')
        if video_data:
            # Decode base64 encoded video data
            video_bytes = base64.b64decode(video_data)
            # Create a download button
            st.download_button(label="Download video",
                               data=video_bytes,
                               file_name='output_video.mp4',
                               mime='video/mp4')
        #get images data
        heatmap_data = response.get('heatmap', '')
        graph_data = response.get('graph', '')

        # Decode base64 encoded images data
        heatmap_bytes = base64.b64decode(heatmap_data)
        graph_bytes = base64.b64decode(graph_data)

        # Create images
        heatmap_img = Image.open(io.BytesIO(heatmap_bytes))
        graph_img = Image.open(io.BytesIO(graph_bytes))
        st.write(response['result_json'])
        '''
        ## Statistics

        '''
        '''
        ### Players running distance

        '''
        get_chart_dist(response['result_json'])
        '''
        ### Players strokes

        '''
        st.write(response['result_json'])
        get_chart_strokes(response['result_json'])

        '''
        ### Player heatmap

        '''
        st.image(heatmap_img, use_column_width=True)




    else:
        st.error("Failed to convert the video.")

#st.image(graph_img, caption="Players and ball movement on y axis", use_column_width=True)
