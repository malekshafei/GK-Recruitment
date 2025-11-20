import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
import io
import warnings
warnings.filterwarnings('ignore')
from datetime import datetime, timedelta

# if 'last_change_time' not in st.session_state:
#     st.session_state.last_change_time = datetime.min
# if 'last_league' not in st.session_state:
#     st.session_state.last_league = ''
# if 'last_name' not in st.session_state:
#     st.session_state.last_name = ''
# # if 'last_season' not in st.session_state:
# #     st.session_state.last_season = ''


# if 'position_group1' not in st.session_state:
#     st.session_state.position_group1 = 'CBs'
# if 'league1' not in st.session_state:
#     st.session_state.league1 = 'NWSL'
# if 'name1' not in st.session_state:
#     st.session_state.name1 = 'Abby Erceg'
# if 'season1' not in st.session_state:
#     st.session_state.season1 = '2024'





file_name = 'GKs-Jan5.parquet'
df = pd.read_parquet(file_name)
df = df.drop_duplicates(subset = ['Player Name', 'Team Name', 'Competition Name', 'Season']).sort_values(by = ['Season', 'Minutes Played'], ascending= [False, False])

df['Ovr'] = (0.6 * df['Shot Stopping']) + (0.1 * df['Coming Out']) + (0.1 * df['Cross Stopping']) + (0.1 * df['Short Distribution']) + + (0.1 * df['Long Distribution'])
print('reading file')
st.set_page_config( 
    page_title="Racing Recruitment",
    page_icon=":checkered_flag:",
    layout="centered",
    initial_sidebar_state="expanded"   
    
)
df.fillna(0, inplace=True)

regular_font_path = 'Montserrat-Regular.ttf'
bold_font_path = 'Montserrat-Bold.ttf'

custom_css = f"""
<style>
@font-face {{
    font-family: 'Montserrat';
    src: url('file://{regular_font_path}') format('truetype');
    font-weight: normal;
}}
@font-face {{
    font-family: 'Montserrat';
    src: url('file://{bold_font_path}') format('truetype');
    font-weight: bold;
}}
html, body, [class*="css"] {{
    font-family: 'Montserrat', sans-serif;
    background-color: #C00C0D;
    color: #ffffff;
}}
.sidebar .sidebar-content {{
    background-color: #C00C0D;
}}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

#st.title(f"Racing Recruitment")

#st.dataframe(df)

sorted_competitions = sorted(df['Competition Name'].unique())


mode = st.selectbox("Select Mode", options=['Player Overview', 'Player Rankings', 'Multi Player Dot Graph'])

if mode == 'Player Overview':


    # file_name = 'InternationalWomensData.xlsx'
    # df = pd.read_excel(file_name)
    

    
    #df['Position Group'] = df['pos_group']




    
    radar = True
    compare = "No"
    # league1 = st.selectbox("Select League", options=['NWSL', 'Mexico', 'Brazil','England', 'Spain', 'Germany', 'Sweden', 'France', 'Colombia', 'Portugal', 'Japan','Australia', 'Italy', 'Norway', 'Denmark', 'Belgium', 'Switzerland','Russia','Ukraine', 'Scotland', 'Iceland', 'USL', 'MLS Next Pro', 'USL League One' ])
    # name1 = st.selectbox("Select Player", options=df[(df['Position Group'] == position_group1) & (df['Competition Name'] == league1)]['Player Name'].unique())
    # season1 = st.selectbox("Select Season", options=sorted(df[(df['Competition Name'] == league1) & (df['Position Group'] == position_group1) & (df['Player Name'] == name1)]['Season'].unique(), reverse=True))
    col1, col2, col3 = st.columns(3)
    

    with col1:
        league1 = st.selectbox(
            'Select League',
            sorted_competitions
        )

    # Place the second selectbox in the second column
    with col2:
        #player_options = df[df['Competition Name'] == st.session_state.league1]['Player Name'].unique()
        name1 = st.selectbox(
            'Select Player',
            df[(df['Competition Name'] == league1)]['Player Name'].unique(),
            #player_options
            
        )

    # Place the third selectbox in the third column
    with col3:
        #season_options = sorted(df[(df['Competition Name'] == st.session_state.league1) & (df['Player Name'] == st.session_state.name1)]['Season'].unique(), reverse=True)
        season1 = st.selectbox(
            'Select Season',
            sorted(df[(df['Competition Name'] == league1) & (df['Player Name'] == name1)]['Season'].unique(), reverse=True),
            #season_options
        )

    col1, col2 = st.columns(2)
    with col1:

        mode1 = st.selectbox("Select Radar Type", options=["Basic", 'Detailed'])

    
 
    

    if radar == True:
        with col2:
            compare = st.selectbox("Compare with another player?", options=["No", 'Yes'])


        if compare == 'Yes':
            col1, col2, col3 = st.columns(3)
            with col1: league2 = st.selectbox("Select other League", options=sorted_competitions)
            with col2: name2 = st.selectbox("Select other Player", options=df[(df['Competition Name'] == league2)]['Player Name'].unique())
            with col3: season2 = st.selectbox("Select other season", options=sorted(df[(df['Competition Name'] == league2) & (df['Player Name'] == name2)]['Season'].unique(), reverse=True))

        ws_leagues = [
            'Albania','Algeria','Andorra','Argentina','Argentina2','Argentina3','ArgentinaCopa','Armenia','Austria2','Azerbaijan',
            'Belgium2','Benin','Bolivia','Bosnia','Brazil PaulistaU20','Brazil3','BrazilU17','BrazilU20','Bulgaria',
            'CAF Champions League','CAF Confederation Cup','Canada','Chile2','Colombia2','Copa Libertadores','Costa Rica','Croatia','Croatia2','Cyprus','Czech2','CzechU19',
            'Denmark3','Denmark4','DenmarkU15','DenmarkU17','DenmarkU172','DenmarkU19','DenmarkU192','Dominican Republic',
            'Ecuador','Ecuador2','El Salvador','England5','England6','EnglandU21','Estonia',
            'Faroe Islands','Finland','Finland2','FinlandU17','France3','France4',
            'Georgia','Germany3','Germany4','GermanyU17','GermanyU19','Ghana','Guatemala',
            'Honduras','Hungary','Hungary2',
            'Iceland','Iceland2','Ireland','Ireland2','Israel','Italy3',
            'Jamaica','Japan2','Japan3',
            'Kazakhstan','Korea2','Korea3','Kosovo',
            'Latvia','Lithuania',
            'Macedonia','Mexico','Mexico2','MexicoU19','MexicoU23','Moldova','Montenegro','Morocco','Netherlands3',
            'Nicaragua','Northern Ireland','Norway2','Norway3','NorwayU17','NorwayU172','NorwayU19','NorwayU192',
            'Panama','Paraguay','Peru','Poland2','Poland3','Portugal2','Portugal3','PortugalU17','PortugalU19','PortugalU23','Romania','Romania2',
            'Scotland2','Scotland3','Serbia','Serbia2','SerbiaU17','SerbiaU19','Slovakia','Slovakia2','SlovakiaU19','Slovenia','Slovenia2','South Africa','Spain3','Spain4','Sweden2','Sweden3','SwedenU17','SwedenU19','Switzerland2','Switzerland3','SwitzerlandU17','SwitzerlandU19',
            'Tunisia','Turkey2','U15 Conmebol','U16 Friendlies','U17 AFCON','U17 Asian Cup','U17 Concacaf','U17 Conmebol','U17 Euros','U17 Euros Qualification','U17 Friendlies','U17 World Cup',
            'U19 Euros','U19 Euros Qualification',
            'U20 AFCON','U20 Asian Cup','U20 Concacaf','U20 Conmebol','U20 Libertadores','U20 World Cup',
            'U21 Euros','U21 Euros Qualification','U23 AFCON','U23 Asian Cup','U23 Conmebol','UEFA Youth League',
            'USA2','USA3','USA4','Ukraine','Ukraine2','Ukraine3','UkraineU19','Uruguay','Uzbekistan','Venezuela'
            ]

        
        # Radar Chart Code
        unavail_metrics = ""
        if mode1 == 'Basic':
                
            ShotStopping = df.loc[df.index[(df['Player Name'] == name1) & (df['Competition Name'] == league1) & (df['Season'] == season1)][0], 'Shot Stopping']
            CrossStopping = df.loc[df.index[(df['Player Name'] == name1) & (df['Competition Name'] == league1) & (df['Season'] == season1)][0], 'Cross Stopping']
            ComingOut = df.loc[df.index[(df['Player Name'] == name1) & (df['Competition Name'] == league1) & (df['Season'] == season1)][0], 'Coming Out']
            ShortDistribution = df.loc[df.index[(df['Player Name'] == name1) & (df['Competition Name'] == league1) & (df['Season'] == season1)][0], 'Short Distribution']
            LongDistribution = df.loc[df.index[(df['Player Name'] == name1) & (df['Competition Name'] == league1) & (df['Season'] == season1)][0], 'Long Distribution']


            

            data1 = [ShotStopping, CrossStopping, ComingOut, ShortDistribution, LongDistribution]
            #if league1 in ws_leagues: data1 = [0, Heading,  BallRetention, ProgressivePassing, DefAccuracy, DefEngage, 0]
            metrics = ['Shot Stopping', 'Cross Stopping','Coming Out', 'Short Distribution', 'Long Distribution']
            metric_names = ['Shot Stopping', 'Cross Stopping','Coming Out', 'Short Distribution', 'Long Distribution']
            unavail_metrics = "Set Piece and Defending High"
            if compare == 'Yes':
                ShotStopping2 = df.loc[df.index[(df['Player Name'] == name2) & (df['Competition Name'] == league2) & (df['Season'] == season2)][0], 'Shot Stopping']
                CrossStopping2 = df.loc[df.index[(df['Player Name'] == name2) & (df['Competition Name'] == league2) & (df['Season'] == season2)][0], 'Cross Stopping']
                ComingOut2 = df.loc[df.index[(df['Player Name'] == name2) & (df['Competition Name'] == league2) & (df['Season'] == season2)][0], 'Coming Out']
                ShortDistribution2 = df.loc[df.index[(df['Player Name'] == name2) & (df['Competition Name'] == league2) & (df['Season'] == season2)][0], 'Short Distribution']
                LongDistribution2 = df.loc[df.index[(df['Player Name'] == name2) & (df['Competition Name'] == league2) & (df['Season'] == season2)][0], 'Long Distribution']



                data2 = [ShotStopping2, CrossStopping2, ComingOut2, ShortDistribution2, LongDistribution2]
                #if league2 in ws_leagues: data2 = [0, Heading2, BallRetention2, ProgressivePassing2, DefAccuracy2, DefEngage2, 0]



        angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
        data1 += data1[:1]  # Repeat the first value to close the polygon
        angles += angles[:1]  # Repeat the first angle to close the polygon

        if compare == 'Yes':
            data2 += data2[:1]

        fig, ax = plt.subplots(figsize=(16, 9), subplot_kw=dict(polar=True, facecolor='#C00C0D'))
        fig.patch.set_facecolor('#C00C0D')
        fig.set_facecolor('#C00C0D')

        ax.set_facecolor('#C00C0D')


        ax.spines['polar'].set_visible(False)


        ax.plot(angles, [100] * len(angles), color='white', linewidth=2.25, linestyle='-')
        ax.plot(angles, [75] * len(angles), color='white', linewidth=0.7, linestyle='-')
        ax.plot(angles, [50] * len(angles), color='white', linewidth=0.7, linestyle='-')
        ax.plot(angles, [25] * len(angles), color='white', linewidth=0.7, linestyle='-')

        if compare == 'No':
            ax.plot(angles, data1, color='green', linewidth=0.4, linestyle='-', marker='o', markersize=3)
            ax.fill(angles, data1, color='green', alpha=0.95)

        if compare == 'Yes':
            ax.plot(angles, data1, color='blue', linewidth=2.5, linestyle='-', marker='o', markersize=3)
            ax.fill(angles, data1, color='blue', alpha=0.7)

            ax.plot(angles, data2, color='yellow', linewidth=2.5, linestyle='-', marker='o', markersize=3)
            ax.fill(angles, data2, color='yellow', alpha=0.55)



        ax.set_xticks(angles[:-1])
        metrics = ["" for i in range(len(metrics))]
        ax.set_xticklabels(metrics)

        ax.set_yticks([])
        ax.set_ylim(0, 100)

        ax.plot(0, 0, 'ko', markersize=4, color='#C00C0D')
        #fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        #fig.subplots_adjust(left=0.25, right=0.75, top=0.75, bottom=0.25)
        fig.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.15)



        #ax.set_xticklabels(metrics, color='white', size=12)


        #plt.savefig(save_path + file_name + '.png')
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0,facecolor=fig.get_facecolor())
        #fig.savefig("PIctestjuly3", format='png', bbox_inches='tight', pad_inches=0)

        buf.seek(0)

        # # Open the image using PIL
        # image = Image.open(buf)

        # # Create a new canvas with desired dimensions and background color
        # final_canvas = Image.new('RGB', (1600, 900), (64, 1, 121))

        image = Image.open(buf).convert("RGBA")

        # Create a new canvas with desired dimensions and background color
        final_canvas = Image.new('RGBA', (1600, 900), (192, 12, 13, 255))


        resize_factor = 1.07
        new_size = (int(image.size[0] * resize_factor), int(image.size[1] * resize_factor))
        image = image.resize(new_size)
        image = image.rotate(18, expand=True)
        #image = image.rotate(13)


        # Calculate the position to paste, centering the image
        x = (final_canvas.width - image.width) // 2
        y = (final_canvas.height - image.height) // 2

        # Paste the matplotlib generated image onto the canvas
        final_canvas.paste(image, (x, y+85), image)

        final_canvas = final_canvas.convert("RGB")

        # plt.figure(figsize=(16, 9))  # Adjust figure size as needed
        # plt.imshow(final_canvas)
        # plt.axis('off')  # Turns off axes.


        fig_canvas, ax_canvas = plt.subplots(figsize=(16, 9))
        ax_canvas.imshow(final_canvas)

        ax_canvas.axis('off')
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        plt.tight_layout(pad=0)
        plt.margins(0, 0)


        if len(metric_names) == 5:
            x_list = [1135,800,455,570,1000,]
            y_list = [445,180,445,865,865,]
            orient_list = ['left', 'center', 'right', 'center', 'center']


            for i in range(5):
                plt.text(x_list[i], y_list[i], metric_names[i], ha = orient_list[i], fontsize=30, color = 'white')#,fontname='Avenir')



        club = df.loc[df.index[(df['Player Name'] == name1) & (df['Competition Name'] == league1) & (df['Season'] == season1)][0], 'Team Name']
        mins = int(df.loc[df.index[(df['Player Name'] == name1) & (df['Competition Name'] == league1) & (df['Season'] == season1)][0], 'Minutes Played'])

        #print(unavail_metrics)
        

        if compare == 'No':
            plt.text(800,70,f"{name1}",ha = 'center', fontsize=45, color = 'white', fontweight = 'bold')
            plt.text(800,120,f"{club} - {season1} {league1} - {mins} Minutes",ha = 'center', fontsize=30, color = 'white')#, fontname='Avenir')
            plt.text(30,880,f"Data compared to {league1}",ha = 'left', fontsize=16, color = 'white')#, fontname='Avenir')
            if league1 in ws_leagues and len(unavail_metrics) > 0: plt.text(1570,880,f"{unavail_metrics}\ndata unavailable for {league1}",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir') 
            # if league1 in ws_leagues and mode1 == 'Basic' and position_group1 in ['CBs','WBs']: plt.text(1570,880,f"Defending High data unavailable for {league1}",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir')
            # if league1 in ws_leagues and mode1 == 'Basic' and position_group1 == 'CMs': plt.text(1570,880,f"Pressing data unavailable for {league1}",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir')

        if compare == 'Yes':
            club2 = df.loc[df.index[(df['Player Name'] == name2) & (df['Competition Name'] == league2) & (df['Season'] == season2)][0], 'Team Name']
            mins2 = int(df.loc[df.index[(df['Player Name'] == name2) & (df['Competition Name'] == league2) & (df['Season'] == season2)][0], 'Minutes Played'])
            


            plt.text(40,65,f"{name1}",ha = 'left', fontsize=35, color = 'blue', fontweight = 'bold')
            #plt.text(40,110,f"{club} - {season1} {league1}",ha = 'left', fontsize=30, color = 'green', fontname='Avenir')
            #plt.text(40,150,f"{mins} Minutes - {detailed_pos}",ha = 'left', fontsize=30, color = 'green', fontname='Avenir')
            plt.text(40,110,f"{club}",ha = 'left', fontsize=30, color = 'blue')#, fontname='Avenir')
            plt.text(40,150,f"{season1} {league1}",ha = 'left', fontsize=30, color = 'blue')#, fontname='Avenir')
            plt.text(40,190,f"{mins} Mins ",ha = 'left', fontsize=30, color = 'blue')#, fontname='Avenir')
        
            plt.text(1560,65,f"{name2}",ha = 'right', fontsize=35, color = 'yellow', fontweight = 'bold')
            #plt.text(1560,110,f"{club2} - {season2} {league2}",ha = 'right', fontsize=30, color = 'red', fontname='Avenir')
            #plt.text(1560,150,f"{mins2} Minutes - {detailed_pos2}",ha = 'right', fontsize=30, color = 'red', fontname='Avenir')
            plt.text(1560,110,f"{club2}",ha = 'right', fontsize=30, color = 'yellow')#, fontname='Avenir')
            plt.text(1560,150,f"{season2} {league2}",ha = 'right', fontsize=30, color = 'yellow')#, fontname='Avenir')
            plt.text(1560,190,f"{mins2} Mins",ha = 'right', fontsize=30, color = 'yellow')#, fontname='Avenir')
            plt.text(30,880,f"Data compared to in player's league",ha = 'left', fontsize=15, color = 'white')#, fontname='Avenir')

            if league1 in ws_leagues and league2 in ws_leagues: plt.text(1570,880,f"{unavail_metrics}\ndata unavailable",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir') 
            if league1 in ws_leagues and league2 not in ws_leagues: plt.text(1570,880,f"{unavail_metrics}\ndata unavailable for {league1}",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir') 
            if league1 not in ws_leagues and league2 in ws_leagues: plt.text(1570,880,f"{unavail_metrics}\ndata unavailable for {league2}",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir') 



            # if league1 in ws_leagues and league2 in ws_leagues and mode1 == 'Basic' and position_group1 in ['CBs','WBs']: plt.text(1570,880,f"Defending High data unavailable",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir')
            # elif league1 in ws_leagues and mode1 == 'Basic' and position_group1 in ['CBs','WBs']: plt.text(1570,880,f"Defending High data unavailable for {league1}",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir')
            # elif league2 in ws_leagues and mode1 == 'Basic' and position_group1 in ['CBs','WBs']: plt.text(1570,880,f"Defending High data unavailable for {league2}",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir')
            
            # if league1 in ws_leagues and league2 in ws_leagues and mode1 == 'Basic' and position_group1 == 'CMs': plt.text(1570,880,f"Pressing data unavailable",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir')
            # elif league1 in ws_leagues and mode1 == 'Basic' and position_group1 == 'CMs': plt.text(1570,880,f"Pressing data unavailable for {league1}",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir')

            # elif league2 in ws_leagues and mode1 == 'Basic' and position_group1 == 'CMs': plt.text(1570,880,f"Pressing data unavailable for {league2}",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir')
            
        #streamlit run streamlit.py


        # plt.subplots_adjust(left=0, right=1, top=1, bottom=0) 
        # plt.margins(0,0) 

        # plt.tight_layout(pad=0)
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
        #fig.savefig("PIctestjuly3", format='png', bbox_inches='tight', pad_inches=0)

        buf.seek(0)


        # plt.savefig("PIctestjuly3.png")

        #st.pyplot(plt)

            
        st.image(buf, use_container_width=True)


    



if  mode == 'Multi Player Dot Graph':
#     pos_list = ['CBs', 'WBs', 'CMs', 'AMs', 'Ws', 'STs']
#     #df['Position Group'] = df['pos_group']




    # st.session_state['league2'] = ''
    # st.session_state['name2'] = ''
    # st.session_state['season2'] = ''

    # st.session_state['league3'] = ''
    # st.session_state['name3'] = ''
    # st.session_state['season3'] = ''
    # league1 = 'NA'
    # player1 = 'NA'
    # season1 = 'NA'

    # league2 = 'NA'
    # player2 = 'NA'
    # season2 = 'NA'

    # league3 = 'NA'
    # player3 = 'NA'
    # season3 = 'NA'

    # league4 = 'NA'
    # player4 = 'NA'
    # season4 = 'NA'

    # league5 = 'NA'
    # player5 = 'NA'
    # season5 = 'NA'

    file_name = 'GKs-Jan5.parquet'
    df = pd.read_parquet(file_name)

    if 'league2' not in st.session_state:
        st.session_state.league2 = ''
    if 'name2' not in st.session_state:
        st.session_state.name2 = ''
    if 'season2' not in st.session_state:
        st.session_state.season2 = ''

    
    

    # league1 = st.selectbox("Select League", options=['NWSL', 'Mexico', 'Brazil','England', 'Spain', 'Germany', 'Sweden', 'France', 'Colombia', 'Portugal', 'Japan','Australia', 'Italy', 'Norway', 'Denmark', 'Belgium', 'Switzerland','Russia','Ukraine', 'Scotland', 'Iceland', 'USL', 'MLS Next Pro', 'USL League One' ])
    # name1 = st.selectbox("Select Player", options=df[(df['Position Group'] == position_group1) & (df['Competition Name'] == league1)]['Player Name'].unique())
    # season1 = st.selectbox("Select Season", options=sorted(df[(df['Competition Name'] == league1) & (df['Position Group'] == position_group1) & (df['Player Name'] == name1)]['Season'].unique(), reverse=True))

    col1, col2, col3 = st.columns(3)
    with col1:
        league1 = st.selectbox(
            'Select League #1',
            sorted_competitions
        )

    # Place the second selectbox in the second column
    with col2:
        name1 = st.selectbox(
            'Select Player #1',
            df[(df['Competition Name'] == league1)]['Player Name'].unique()
        )

    # Place the third selectbox in the third column
    with col3:
        season1 = st.selectbox(
            'Select Season #1',
            sorted(df[(df['Competition Name'] == league1) & (df['Player Name'] == name1)]['Season'].unique(), reverse=True)
        )


    col1, col2, col3 = st.columns(3)
    with col1:
        league2 = st.selectbox(
            'Select League #2',
            sorted_competitions
        )

    # Place the second selectbox in the second column
    with col2:
        name2 = st.selectbox(
            'Select Player #2',
            df[(df['Competition Name'] == league2)]['Player Name'].unique()
        )

    # Place the third selectbox in the third column
    with col3:
        season2 = st.selectbox(
            'Select Season #2',
            sorted(df[(df['Competition Name'] == league2) & (df['Player Name'] == name2)]['Season'].unique(), reverse=True)
        )

    col1, col2, col3 = st.columns(3)
    with col1:
        league3 = st.selectbox(
            'Select League #3',
            sorted_competitions
        )

    # Place the second selectbox in the second column
    with col2:
        name3 = st.selectbox(
            'Select Player #3',
            df[(df['Competition Name'] == league3)]['Player Name'].unique()
        )

    # Place the third selectbox in the third column
    with col3:
        season3 = st.selectbox(
            'Select Season #3',
            sorted(df[(df['Competition Name'] == league3) & (df['Player Name'] == name3)]['Season'].unique(), reverse=True)
        )
    
    
    col1, col2, col3 = st.columns(3)
    with col1:
        league4 = st.selectbox(
            'Select League #4',
            sorted_competitions
        )

    # Place the second selectbox in the second column
    with col2:
        name4 = st.selectbox(
            'Select Player #4',
            df[ (df['Competition Name'] == league4)]['Player Name'].unique()
        )

    # Place the third selectbox in the third column
    with col3:
        season4 = st.selectbox(
            'Select Season #4',
            sorted(df[(df['Competition Name'] == league4) & (df['Player Name'] == name4)]['Season'].unique(), reverse=True)
        )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        league5 = st.selectbox(
            'Select League #5',
            sorted_competitions
        )

    # Place the second selectbox in the second column
    with col2:
        name5 = st.selectbox(
            'Select Player #5',
            df[(df['Competition Name'] == league5)]['Player Name'].unique()
        )

    # Place the third selectbox in the third column
    with col3:
        season5 = st.selectbox(
            'Select Season #5',
            sorted(df[(df['Competition Name'] == league5) & (df['Player Name'] == name5)]['Season'].unique(), reverse=True)
        )

    # data = {
    #     'Player Name': ['Turner', 'Silva', 'Jheniffer', 'Tanaka', 'Ludmila'],
    #     'League': ['NWSL', 'Portugal', 'NWSL', 'Greece', 'NWSL'],
    #     'Season': ['2024', '2023/24', '2023/24', '2023/24', '2023/24'],
    #     'Poaching': [70, 90, 80, 50, 85],
    #     'Finishing': [60, 75, 85, 70, 90],
    #     'Defensive Output 1': [50, 55, 40, 65, 70],
    #     'Chance Creation': [45, 60, 80, 85, 70],
    #     'Defensive Output 2': [5, 50, 45, 70, 80]
    # }


    # df = pd.DataFrame(data)




    df = df[((df['Competition Name'] == league1) & (df['Player Name'] == name1) & (df['Season'] == season1)) | 
            ((df['Competition Name'] == league2) & (df['Player Name'] == name2) & (df['Season'] == season2)) | 
            ((df['Competition Name'] == league3) & (df['Player Name'] == name3) & (df['Season'] == season3)) | 
            ((df['Competition Name'] == league4) & (df['Player Name'] == name4) & (df['Season'] == season4)) |
            ((df['Competition Name'] == league5) & (df['Player Name'] == name5) & (df['Season'] == season5))]

    df['unique_label'] = df.apply(lambda row: f"{row['Player Name']}\n{row['Competition Name']} - {row['Season']}", axis=1)

                
    #print(df)
    # Plotting

    metrics = ['Shot Stopping', 'Cross Stopping','Coming Out', 'Short Distribution', 'Long Distribution']
    metrics.reverse()
    

    #metrics = metrics[::-1]

    #players = [player1, player2, player3, player4, player5 ]
    #players = df['Player Name']
    players = df['unique_label']
    colors = ['purple', 'red', 'green', 'orange', 'black', 'yellow']
    #fig, ax = plt.subplots(figsize=(10, 6))
    fig, ax = plt.subplots(figsize=(16, 9))
    fig.patch.set_facecolor('#C00C0D')
    fig.set_facecolor('#C00C0D')

    ax.set_facecolor('#C00C0D')
    #fig, ax = plt.subplots(figsize=(16, 9))


    # Plot lines for each metric
    for i in range(len(metrics)):
        y = len(metrics) - i
        metric = metrics[i]

        ax.plot([0, 100], [y, y], color='white', linewidth=0.8)



        for x in np.arange(0, 101, 10):
            #ax.axvline(x, ymin=y - 0.05, ymax=y + 0.05, color='black', linewidth=0.5)
            ax.vlines(x, ymin=y-0.1, ymax=y+0.1, color='white', linewidth=0.6, zorder= 1)

        for j in range(len(players)):
            row = df.iloc[j]
            unique_label = row['unique_label']
            player = row['Player Name']
            league = row['Competition Name']
            season = row['Season']

            #x = df.loc[j, metric]
            x = row[metric]
            print(player, season, metric, x)
            #ax.scatter(x, i+1, s = 950, color=colors[j], label=player if i == 0 else "", zorder = 3)
            ax.scatter(x, i + 1, s=950, color=colors[j], label=unique_label if i == 0 else "", zorder=3)





    # Customizing the plot

    ax.set_xticks(np.arange(0, 101, 10))
    ax.set_xticklabels(np.arange(0, 101, 10), size = 22, color = 'white')#,fontname='Avenir',
    ax.set_xlabel(f'Rankings vs GKs in their League', size = 20,  color = 'white')#,fontname='Avenir',
    ax.set_title('Player Comparison\n ', size = 30, color = 'white')#fontname='Avenir'

    # for label in ax.get_yticklabels():
    #     label.set_x(-0.05)  # Adjust the value as needed to create more space

    #ax.yaxis.set_tick_params(pad=60)

    for label in ax.get_yticklabels():
        label.set_bbox(dict(facecolor='#C00C0D', edgecolor='None', alpha=0.65, pad=5))

    ax.set_yticks(np.arange(1, len(metrics) + 1))
    ax.set_yticklabels(metrics, size = 23, ha='right', color = 'white')#, fontname='Avenir')




    # Adding legend
    # handles, labels = ax.get_legend_handles_labels()
    # by_label = dict(zip(labels, handles))
    # ax.legend(by_label.values(), by_label.keys(), loc='upper center', bbox_to_anchor=(0.5, -0.15), fontsize='large', ncol=5)
    handles, labels = ax.get_legend_handles_labels()
    #legend_labels = [f'{label}\n{df.loc[df["Player"] == label, "Competition"].iloc[0]} - {df.loc[df["Player"] == label, "Season"].iloc[0]}\n{int(df.loc[df["Player"] == label, 'Minutes Played'].iloc[0])} Minutes' for label in labels]
    legend_labels = [f'{label}\n{int(df.loc[df["unique_label"] == label, "Minutes Played"].iloc[0])} Minutes' for label in labels]

 
    by_label = dict(zip(labels, handles))
    legend = ax.legend(by_label.values(), legend_labels, facecolor = '#C00C0D', loc='upper center', bbox_to_anchor=(0.5, -0.2), fontsize=16, ncol=len(players))
     
    for text in legend.get_texts():
        text.set_color('white')
    # from matplotlib import font_manager as fm

    # for text in legend.get_texts():
    #     text.set_color('white')
    #     lines = text.get_text().split('\n')
    #     text.set_text('')  # Clear the current text

    # # Create Text objects with different font sizes
    #     for i, line in enumerate(lines):
    #         if i == 0:
    #             font_properties = fm.FontProperties(size=20)  # Larger font for the first line
    #         else:
    #             font_properties = fm.FontProperties(size=16)  # Normal font for other lines
    #         text_line = plt.Text(0, 0, line, fontproperties=font_properties)
    #         text_line.set_fontproperties(font_properties)

    #         # Append each line with appropriate font size to the text
    #         text._text += text_line.get_text() + '\n'




        
    

    #plt.subplots_adjust(left=0.3, right=0.95, top=0.9, bottom=0.1)
    #plt.axis('off')
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.2)
    #fig.savefig("PIctestjuly3", format='png', bbox_inches='tight', pad_inches=0)

    buf.seek(0)


    # plt.savefig("PIctestjuly3.png")

    #st.pyplot(plt)

        
    st.image(buf, use_container_width=True)
    radar = True
    position_group1 = 'NA'
   
if mode == 'Player Rankings':
    import matplotlib.font_manager as font_manager
    from matplotlib import font_manager, rcParams

    font_manager.fontManager.addfont(regular_font_path)
    font_manager.fontManager.addfont(bold_font_path)
    rcParams['font.family'] = 'Montserrat'
    mode1 = 'Basic'

    

    value_cols = ['Ovr', 'Shot Stopping', 'Cross Stopping','Coming Out', 'Short Distribution', 'Long Distribution']
    
    for col in value_cols:
        
        if col == 'Ovr': df[col] = round(df[col],1)
        else:
            df=df.fillna(0) 
            df[col] = df[col].astype(int)




    #df = df[pd.notna(df['Team']) & (df['Team'] != 0) & (df['Team'] != '0') ]
    col1, col2, col3 = st.columns(3)

    with col1: 
        leagues = st.multiselect("Select Leagues", sorted(df['Competition Name'].unique()), default=['Denmark'])
        df = df[df['Competition Name'].isin(leagues)]
    
        age_range = st.slider("Age Range", 15, 40, (24,32))
        df = df[((df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])) | (pd.isna(df['Age']))]

        
            


        create_ratings = st.segmented_control("Customize Rating Weights?", ["Yes", "No"], default = "No")


    with col2: 
        
        df = df[~df['Season'].str.contains('-', na=False)]
        seasons = ['2025', '25/26']
        df = df[df['Season'].isin(seasons)]
        
        minutes_range = st.slider("Minutes Played Range", 0, max(df['Minutes Played']), (600, max(df['Minutes Played'])))
        df = df[(df['Minutes Played'] >= minutes_range[0]) & (df['Minutes Played'] <= minutes_range[1])]


    with col3: 
        
    
        num_shown = st.segmented_control("# Players to Show", ["10", "15", "25", "All"],default = "15" )

        
        
    
    if create_ratings == 'Yes':
        ratings= ['Shot Stopping', 'Cross Stopping','Coming Out', 'Short Distribution', 'Long Distribution']
        

            
        weights = {}
        col1, col2, col3 = st.columns(3)
        ind = 0
        with col1:
            for x in ratings[::3]:
                #xx = st.slider(x,0,100,value = 50, key=x)
                weights[x] = st.slider(x,0,100,value = 50)
                ind+=1
        with col2:
            for x in ratings[1::3]:
                #xx = st.slider(x,0,100,value = 50, key=x)
                weights[x] = st.slider(x,0,100,value = 50)
                ind+=1
        with col3:
            for x in ratings[2::3]:
                #xx = st.slider(x,0,100,value = 50, key=x)
                weights[x] = st.slider(x,0,100,value = 50)
                ind+=1


        print(weights)
        total = sum(weights.values())
        normalized = {k: v / total * 100 for k, v in weights.items()}
        df['Ovr'] = round(sum(df[col] * (normalized[col]*.01) for col in normalized),1)
        df = df.sort_values(by = 'Ovr', ascending=False)

    df.insert(0, "Rank", range(1, len(df) + 1))

    df['Team'] = df['Team Name']
    df['League'] = df['Competition Name']
    df['Mins'] = df['Minutes Played']

    data_copy = df.copy(deep=True)


            
            
            
        
    

    

    

    if num_shown == "5": df = df.head(5)
    elif num_shown == "10": df = df.head(10)
    elif num_shown == "15": df = df.head(15)
    elif num_shown == "25": df = df.head(25)
    elif num_shown == "All": df = df.copy(deep=True)
    
    #st.write(df)

    
    columns = ["Rank","Player Name", "Team", "League", "Age","Mins",  "Ovr"]
    
    

    def create_football_table(data, columns):
        # ---- Figure & layout (fixes: subtitle whitespace) ----
        fig, ax = plt.subplots(figsize=(14, 12))
        # We'll control margins explicitly; avoid tight_layout which can add unpredictable gaps with tables.
        fig.set_constrained_layout(False)
        fig.subplots_adjust(left=0.02, right=0.98, bottom=0.06, top=0.90)

        # Titles sit in the top figure margin; table lives entirely inside the axes.
        title = f'Top GKs - Data Ranking'

        subtitle = f"{', '.join(map(str, set(leagues)))} | {', '.join(map(str, set(seasons)))} | Age: {age_range[0]}-{age_range[1]} | Minutes: {minutes_range[0]}-{minutes_range[1]}"


        fig.suptitle(title, fontsize=24, fontweight='bold', y=0.965)
        fig.text(0.5, 0.92, subtitle, ha='center', va='center', fontsize=14, color='black')

        ax.axis('off')

        data_df = pd.DataFrame(data, columns=columns)

        # ---- Table ----
        table = ax.table(
            cellText=data_df.values,
            colLabels=data_df.columns,
            cellLoc='center',
            loc='center',
            bbox=[0.00, 0.00, 1.00, 1.00]  # Fill the axes; margins come from subplots_adjust above
        )

        # Basic styling
        table.auto_set_font_size(False)
        table.set_fontsize(14)
        table.scale(1, 2)

        # Remove borders
        for _, cell in table.get_celld().items():
            cell.set_linewidth(0)
            cell.set_edgecolor('none')


        

        # Header styling
        ncols = len(data_df.columns)
        for j in range(ncols):
            cell = table[(0, j)]
            cell.set_facecolor('#E8E8E8')
            cell.set_text_props(weight='bold', color='black')
            cell.set_height(0.08)

        # Data rows
        nrows = len(data_df)
        for i in range(1, nrows + 1):
            for j in range(ncols):
                c = table[(i, j)]
                c.set_facecolor('white')
                if j == ncols - 1:
                    c.set_facecolor('#E6E1F0')  # last column
                if j == 1:
                    c.set_text_props(ha='left')
                    #c.get_text().set_x(0.15)  # space for logo

                    # if nrows < 4:
                    #     table[(i, 1)].PAD = 0.45
                    # elif nrows < 8:
                    #     table[(i, 1)].PAD = 0.35
                    # elif nrows < 12:
                    #     table[(i, 1)].PAD = 0.3
                    # else: table[(i, 1)].PAD = 0.25

                c.set_height(0.06)
                c.set_text_props(color='black')

       
        col_widths = {
            "Rank": 0.1,
            "Player Name": 0.35,
            "Team": 0.3,
            "League": 0.15,
           
            "Mins": 0.10,
            "Age": 0.10,
            "Ovr": 0.12
        }
        
        # Apply widths to all cells in that column
        for j, col in enumerate(data_df.columns):
            for i in range(nrows + 1):  # +1 to include header row
                cell = table[(i, j)]
                cell.set_width(col_widths.get(col, 0.1))

        # Force draw to get real positions
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()

       
        # ---- Row separators (fixes: incorrect placement/omissions) ----
        # Draw a thin line under every data row except the last, using each row's true bottom y.
        # We'll align lines to the full table width (from first to last column).
        first_left_disp = table[(1, 0)].get_window_extent(renderer).x0
        last_right_disp = table[(1, ncols - 1)].get_window_extent(renderer).x1
        left_fig = fig.transFigure.inverted().transform((first_left_disp, 0))[0]
        right_fig = fig.transFigure.inverted().transform((last_right_disp, 0))[0]

        for i in range(1, nrows):  # separators between data rows
            row_bottom_fig_y = table[(i, 0)].get_window_extent(renderer)
            row_bottom_fig_y = row_bottom_fig_y.transformed(fig.transFigure.inverted()).y0
            line = plt.Line2D([left_fig, right_fig],
                            [row_bottom_fig_y, row_bottom_fig_y],
                            color='#DDDDDD', linewidth=0.9, alpha=0.9,
                            transform=fig.transFigure, zorder=2)
            fig.add_artist(line)

        # ---- Footer ----
        # ax.text(0.98, 0.01, "Test", transform=ax.transAxes,
        #         ha='right', va='bottom', fontsize=10, color='gray')

        return fig, ax, table


    

    # Create the table
    fig, ax, table = create_football_table(df, columns)
    #plt.show()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.2)
    #fig.savefig("PIctestjuly3", format='png', bbox_inches='tight', pad_inches=0)

    buf.seek(0)
        
    st.image(buf, use_container_width=True)
    
    
    
    ratings = ['Shot Stopping', 'Cross Stopping','Coming Out', 'Short Distribution', 'Long Distribution']
        
        
    selected_cols =  ["Rank","Player Name", "Team Name", "Competition Name", "Minutes Played", "Age", "Ovr"] + ratings
    data_copy = data_copy[selected_cols]
   # st.write(data_copy, ind)
    st.write("")
    st.write("")
    st.dataframe(data_copy, hide_index=True)


def get_columns_to_compare(row):
    columns = ['Shot Stopping', 'Cross Stopping','Coming Out', 'Short Distribution', 'Long Distribution']
    return columns

def normalize(series):
    series = pd.to_numeric(series, errors='coerce')  # Convert to numeric, forcing non-numeric values to NaN
    min_val = series.min()
    max_val = series.max()
    if pd.isna(min_val) or pd.isna(max_val) or min_val == max_val:
        return pd.Series(1, index=series.index)  # All values are the same or all NaN
    return (series - min_val) / (max_val - min_val)

def cosine_sim(a, b):
    a = np.array(a).reshape(1, -1)
    b = np.array(b).reshape(1, -1)
    return np.dot(a, b.T) / (np.linalg.norm(a) * np.linalg.norm(b))




if mode == 'Player Overview':
    med_mins = 0
    col1, col2 = st.columns(2)
    with col1:
        BestPlayers = df[(df['Competition Name'] == league1)]

        BestPlayers['Season'] = BestPlayers['Season'].astype(str)
        #filtered_seasons = BestPlayers['Season'][BestPlayers['Season'].str.len() < 8]
        
        BestPlayers = BestPlayers[(BestPlayers['Season'] == season1) & (BestPlayers['Season'].str.len() < 8)]
        max_season = season1



        st.write(f"Best GKs in {season1} {league1}")
                
        med_mins = np.median(BestPlayers['Minutes Played'])
        BestPlayers = BestPlayers[BestPlayers['Minutes Played'] > med_mins].sort_values(by = 'Ovr', ascending=False)[:10]
        i = 1
        for _, row in BestPlayers.iterrows():
            st.write(f"{i}. {row['Player Name']}  \n({row['Team Name']} - {round(row['Age'],1)} - {int(row['Minutes Played'])} mins)")
            i += 1
    
    
    with col2:
        #print('hiii')
        # Assuming you have position_group2 and league2 defined similarly to col1
        player_row = df[(df['Season'] == season1) & (df['Competition Name'] == league1) & (df['Player Name'] == name1)]
        AllPlayers = df[(df['Competition Name'] == league1) & (df['Minutes Played'] > med_mins)]
        

        #print(len(AllPlayers))

        # Filter for the most recent season
        AllPlayers['Season'] = AllPlayers['Season'].astype(str)
        #max_season_order = AllPlayers['Season Order'].max()
        AllPlayers = AllPlayers[(AllPlayers['Season'] == season1) & (AllPlayers['Season'].str.len() < 8)]
        AllPlayers = pd.concat([AllPlayers, player_row]).drop_duplicates(subset=['Player Name', 'Season'])
        max_season = AllPlayers['Season'].values[0]
        # print(len(AllPlayers))
        # print(max_season)

        st.write(f"Most Similar GKs to {name1} in {max_season} {league1}")

        AllPlayers['columns_to_compare'] = AllPlayers.apply(get_columns_to_compare, axis=1)

        def calculate_similarity(player1, player2):
            columns = list(set(player1['columns_to_compare']) & set(player2['columns_to_compare']))
            if not columns:
                return 0
            values1 = player1[columns].values
            values2 = player2[columns].values
            values1_norm = normalize(pd.Series(values1))
            values2_norm = normalize(pd.Series(values2))
            
            return cosine_sim(values1_norm, values2_norm)[0][0]

        
        
        def get_most_similar_players(player_name, n=10):
            player_rows = AllPlayers[AllPlayers['Player Name'] == player_name]
            if player_rows.empty:
                st.error(f"Player {player_name} not found in the dataset.")
                return pd.DataFrame()
            
            player = player_rows.iloc[0]
            
            # Check for NAs in the player's data
            na_columns = player[player['columns_to_compare']].isna().sum()
            if na_columns > 0:
                st.warning(f"Player {player_name} has {na_columns} NA values in their data.")
            
            similarities = AllPlayers.apply(lambda x: calculate_similarity(player, x), axis=1)
            similar_indices = similarities.sort_values(ascending=False).index[1:n+1]  # Exclude the player itself
            similar_players = AllPlayers.loc[similar_indices]
            return pd.DataFrame({
                'Player Name': similar_players['Player Name'],
                'Similarity': similarities[similar_indices],
                'Team': similar_players['Team Name'],
                'Age': similar_players['Age'],
                'Minutes Played': similar_players['Minutes Played']
            })
        

       
        similar_players = get_most_similar_players(name1)
        
        for i, (_, row) in enumerate(similar_players.iterrows(), 1):
            similarity_percentage = round(row['Similarity'] * 100, 2)
            st.write(f"{i}. {row['Player Name']} (Similarity: {similarity_percentage}%)  \n"
                    f"({row['Team']} - {round(row['Age'],1)} - {int(row['Minutes Played'])} mins)")
            
        player = AllPlayers[AllPlayers['Player Name'] == name1].iloc[0] 
    



        
if mode == 'Player Overview':
    st.write("Metric Definitions:")
    st.write("Shot Stopping: Goals Prevented (xGOT - Goals Allowed) and Save %")
    st.write("Cross Stopping: % of Crosses Claimed")
    st.write("Coming Out: # Defensive Actions outside Box")
    st.write("Short Distribution: Passes Completed & Accuracy for less than 40m")
    st.write("Long Distribution: Passes Completed & Accuracy for more than 40m")

#streamlit run streamlit.py