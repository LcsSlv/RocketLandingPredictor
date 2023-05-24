# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', 
                                            options=[{'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}],
                                            value='ALL',
                                            placeholder='Select a Launch Site here',
                                            searchable=True,
                                            ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                value=[min_payload, max_payload],
                                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
            Input(component_id='site-dropdown', component_property='value'),
            )
def get_pie_chart(entered_value):
    if entered_value == 'ALL':
        df = spacex_df
        values= df['class']
        labels= df['Launch Site']
        title='Success Rate of each site'
    else:
        df = spacex_df[spacex_df['Launch Site'] == entered_value]
        success_count = df['class'].sum()
        failure_count = len(df) - success_count
        labels = ['Success', 'Failure']
        values = [success_count, failure_count]
        title= 'Success Rate for' + entered_value

    pie_chart = px.pie(df, values=values, names=labels, title=title)
    return pie_chart

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
            Input(component_id='payload-slider', component_property='value'),
            Input(component_id='site-dropdown', component_property='value'),
            )

def get_scatter_chart(payload_mass, launch_site):
    if launch_site == 'ALL':
        df=spacex_df
    else:
        df = spacex_df[spacex_df['Launch Site'] == launch_site]

    condition = (df['Payload Mass (kg)'] >= payload_mass[0]) & (df['Payload Mass (kg)'] <= payload_mass[1])
    df = df[condition]
    x = 'Payload Mass (kg)'
    y = 'class'
    point_color = 'Booster Version Category'
    scatter_chart = px.scatter(df, x=x, y=y, color=point_color)

    return scatter_chart

# Run the app
if __name__ == '__main__':
    app.run_server()
