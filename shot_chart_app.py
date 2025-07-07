import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail

# Helper to find player id

def get_player_id(player_name: str):
    result = players.find_players_by_full_name(player_name)
    if result:
        return result[0]['id']
    return None

@st.cache_data(ttl=60 * 60 * 24)
def load_shotchart(player_id: int, season: str):
    shots = shotchartdetail.ShotChartDetail(
        team_id=0,
        player_id=player_id,
        season_nullable=season,
        context_measure_simple='FGA'
    )
    return shots.get_data_frames()[0]

# Matplotlib hexbin plot

def plot_matplotlib_hex(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(6,5))
    hb = ax.hexbin(df['LOC_X'], df['LOC_Y'], gridsize=30, cmap='inferno', mincnt=1)
    ax.set_facecolor('white')
    ax.set_xlim(-250, 250)
    ax.set_ylim(-50, 450)
    ax.set_xlabel('Court X')
    ax.set_ylabel('Court Y')
    ax.set_title('Hex Shot Chart')
    fig.colorbar(hb, ax=ax, label='Shot Frequency')
    st.pyplot(fig)

# Plotly heatmap approximation

def plot_plotly_hex(df: pd.DataFrame):
    fig = px.density_heatmap(
        df, x='LOC_X', y='LOC_Y', nbinsx=30, nbinsy=30,
        color_continuous_scale='inferno')
    fig.update_layout(
        title='Shot Density (Plotly)',
        xaxis=dict(range=[-250, 250]),
        yaxis=dict(range=[-50, 450], scaleanchor='x', scaleratio=1)
    )
    st.plotly_chart(fig, use_container_width=True)

def main():
    st.title('NBA Player Hex Shot Chart')
    player_name = st.text_input('Player Name', 'Stephen Curry')
    season = st.text_input('Season (e.g. 2022-23)', '2022-23')

    if st.button('Generate Chart'):
        player_id = get_player_id(player_name)
        if player_id is None:
            st.error('Player not found')
            return
        df = load_shotchart(player_id, season)
        if df.empty:
            st.error('No data returned')
            return
        plot_type = st.radio('Visualization Library', ['Matplotlib', 'Plotly'])
        if plot_type == 'Matplotlib':
            plot_matplotlib_hex(df)
        else:
            plot_plotly_hex(df)

if __name__ == '__main__':
    main()
