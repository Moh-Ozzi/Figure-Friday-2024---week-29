import dash
from dash import html, dcc, Output, Input
import plotly.express as px
import pandas as pd
from PIL import Image
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc


df = pd.read_csv('standings.csv')
df['team_name'] = df['team_name'].str.rsplit(' ', n=1).str[0]
filtered_df = df.loc[(df['season'].isin(['2023-2024', '2022-2023', '2021-2022'])) & (df['division'].isin(["Women's Super League (WSL)", "FA Women's Super League (WSL)"]))]


app = dash.Dash(
    __name__, suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP]
)


app.layout = dbc.Container(
    [
        html.H3("Impact of Goal Difference on Points in the Women's Super League WSL", className='mt-1'),
        dmc.Select(
            label="Select season",
            id="season",
            value="2023-2024",
            data=['2023-2024', '2022-2023', '2021-2022'],
            style={'width' : '300px'},
            className='mb-0'
        ),
        dcc.Graph(id='graph', config={'displayModeBar': False}, className='mt-0')
    ],
    fluid=True
)
@app.callback(Output('graph', 'figure'), Input('season', 'value'))
def update_figure(input):
    df = filtered_df.copy()
    df = df.loc[df['season'] == input]
    fig = px.scatter(df, x="goal_difference", y="points",
                     hover_data=['team_name', 'position'], hover_name='team_name')

    for i, row in df.iterrows():
        team = row['team_name']
        fig.add_layout_image(
            dict(
                source=Image.open(f"GB1/{team}.png"),
                xref="x",
                yref="y",
                xanchor="center",
                yanchor="middle",
                x=row["goal_difference"],
                y=row["points"],
                sizex=7,
                sizey=7,
                sizing="contain",
                opacity=1,
                layer="above"
            )
        )

    fig.update_layout(height=600, width=1400, plot_bgcolor="#FAF8FA", margin=dict(l=10, r=10, t=10, b=10), hoverlabel=dict(
        bgcolor="white",
        font_size=13,
        font_family="Arial"
    ))

    return fig

if __name__ == "__main__":
    app.run_server()