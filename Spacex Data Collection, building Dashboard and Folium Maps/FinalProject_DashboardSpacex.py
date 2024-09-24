# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

 ''' In this project, I developed a dashboard that allows users to analyze the number of successful landings for each launch site. 
The dashboard layout provides a clear overview of the total successful landings per site, offering users a quick way to compare performance across different locations. 
Additionally, I implemented a scatterplot that visualizes the relationship between the mass of the rocket at launch and the success rate of the landing. 
This plot helps in exploring whether there is any correlation between the launch mass and the likelihood of a successful landing. 
The combination of these visualizations provides a comprehensive tool for understanding key factors related to launch outcomes. '''

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
                                dcc.Dropdown(id='site-dropdown',
                                            options=[
                                            {'label': 'All Sites', 'value': 'ALL'},
                                            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},

                                        ],
                                        value='ALL',
                                        placeholder="Select a Launch Site here",
                                        searchable=True
                                        ),
                                html.Br(),

                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
            
                                dcc.RangeSlider(id='payload-slider',
                                        min=0, max=10000, step=1000,
                                        marks={0: '0',
                                            2500: '2500',
                                            5000: '5000',
                                            7500: '7500'},
                                        value=[min_payload, max_payload]),

                      
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
            Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches for ALL sites')
        return fig
    else:

        # Filter dataframe for the selected site
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        
        # Create a pie chart for the selected site
        fig = px.pie(filtered_df, 
        names = 'class',
        title=f'Total Success Launches for site {entered_site}')

        return fig
        # return the outcomes piechart for a selected site

# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
            Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value"))

def get_payload_scatter_chart(entered_site,payload_range):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & 
            (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    if entered_site == 'ALL':
        # Plot for all sites
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                        color="Booster Version Category",
                        title='Correlation between Payload and Success for all Sites',
                        labels={'class': 'Launch Outcome'})
        return fig
    else:
        # Filter the dataframe for the selected site
        site_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        # Plot for the specific site
        fig = px.scatter(site_df, x='Payload Mass (kg)', y='class',
                        color="Booster Version Category",
                        title=f'Correlation between Payload and Success for site {entered_site}',
                        labels={'class': 'Launch Outcome'})
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()

