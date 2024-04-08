#Part A: Importing Statements and Downloading Data
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime
import plotly.express as px
from dash import dash_table
from dash_bootstrap_components import Card, CardBody, CardHeader
from dash import Dash, dcc, html, Input, Output, callback

FA = "https://use.fontawesome.com/releases/v5.8.1/css/all.css"
common_style = {
    'fontFamily': 'Arial, sans-serif',
    'fontSize': '16px',
    'textAlign': 'justify',
    'margin': '10px'
}

# Initialise the App
app = Dash(
    __name__, 
    external_stylesheets=[dbc.themes.LUX, FA],
    suppress_callback_exceptions=True  # Add this line
)
# Read the Excel file
realestateneconomic = pd.read_excel(
    r'C:\Users\Rohit\OneDrive\Desktop\Spring 2024\ISM 646 Data Visualization\Python_Assignment2\Assignment_Dash_App\RealEstateandEconomicIndicators.xlsx',
    sheet_name="RealEstate&MacroeconomicFacto"
)
differential_data = pd.read_excel(
    r'C:\Users\Rohit\OneDrive\Desktop\Spring 2024\ISM 646 Data Visualization\Python_Assignment2\Assignment_Dash_App\RealEstateandEconomicIndicators.xlsx',
    sheet_name='differential'
)
homeownership_data = pd.read_excel(  r'C:\Users\Rohit\OneDrive\Desktop\Spring 2024\ISM 646 Data Visualization\Python_Assignment2\Assignment_Dash_App\RealEstateandEconomicIndicators.xlsx',
    sheet_name="dataformaps"
)

# Mapping of state names to abbreviations
state_to_code = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
    'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
    'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
    'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
    'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY',
    'District of Columbia': 'DC'
}
# Filter for the states of interest
states_of_interest = ["North Carolina", "Texas", "Florida", "California"]
df_filtered = realestateneconomic[realestateneconomic["State"].isin(states_of_interest)]
#Part B: Data Preparation

leading_avg_data = realestateneconomic.groupby('Year')[['Zillow Home Value Index in Dollars', 'State minimum wage  Dollars per Hour']].mean().reset_index()
lagging_avg_data = realestateneconomic.groupby('Year')[['Unemployment Rate in Percent', 'State tax collection Millions of U.S. Dollars']].mean().reset_index()
homeownership_data.rename(columns={'State Name': 'State', 'Ownership Rate': 'Home Ownership Rate_Current'}, inplace=True)
homeownership_data['StateAbbrev'] = homeownership_data['State'].map(state_to_code)

# Custom sort order for the 'Range of House Prices'
custom_sort_order = ['$125K-$149K', ' $150K-$199K', ' $200K-$249K', ' $250K-$299K', '$300K-$399K', 
                     '$400K-$499K', '$500K-$749K', '$750K-Over']

# Ensure the 'Range of House Prices' column is a categorical type with the desired order
differential_data['Range of House Prices'] = pd.Categorical(
    differential_data['Range of House Prices'], 
    categories=custom_sort_order, 
    ordered=True
)

# Now, sort the DataFrame based on this categorical column
differential_data.sort_values('Range of House Prices', inplace=True)

# Part C: Main Layout with tabs
app.layout = dbc.Container([
    dcc.Location(id="url", refresh=False),
    dbc.Row([
        dbc.Col(html.Div("Bryan School of Business & Economics, UNCG", className="text-left medium font-weight-bold"), width=6, md=6, style=common_style),
        dbc.Col(html.Div(id="live-time", className="text-right medium"), width=4, md=8, style=common_style),
    ], className="align-items-center", style={'padding': '0 40px'}),

    dbc.Row([
        dbc.Col(html.H1("Navigating Economic Turbulence: Real Estate & Economic Indicators Amidst the Great Recession & Covid-19", className="text-center my-2"), width=12, style=common_style),
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Nav([
                
                dbc.NavLink([html.I(className="fas fa-home mr-2"), "Home Page"], href="/", active="exact", style=common_style),
                dbc.NavLink([html.I(className="fas fa-archive mr-2"), "Overview"], href="/overview", active="exact", style=common_style),
                dbc.NavLink([html.I(className="fas fa-building mr-2"), "Real Estate"], href="/real-estate", active="exact", style=common_style),
                dbc.NavLink([html.I(className="fas fa-chart-line mr-2"), "Economic Indicators"], href="/economic-indicators", active="exact", style=common_style),
                dbc.NavLink([html.I(className="fas fa-exchange-alt mr-2"), "Leading and Lagging Indicators"], href="/leading-lagging-indicators", active="exact", style=common_style),
                dbc.NavLink([html.I(className="fas fa-archive mr-2"), "Differential Impact"], href="/differential-impact", active="exact", style=common_style),
                
            ], vertical=True,
               pills=True,
               className="bg-light border-right flex-column align-items-start",
               style={"padding": "1rem", "height": "100vh"}),
        ], width=2, className="flex-grow-1"),
        
        dbc.Col(html.Div(id="page-content"), width=10),
        
    ]),
    dcc.Interval(id='interval-component', interval=1000, n_intervals=0),
], fluid=True, style={
    'backgroundImage': 'url(/assets/IM.JPG)',
    'backgroundSize': 'cover',
    'backgroundPosition': 'center center',
    'backgroundRepeat': 'no-repeat',
    'height': 'auto'
}
)

#Part D:Callback for page rendering
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return html.Div([
            dbc.Row(
                dbc.Col(
                    html.H2("Welcome to the Analysis Dashboard for Real Estate and Economic Factors!", className="text-center my-4"),
                    width=12
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.P([
                        "Explore comprehensive analyses and insights into the dynamic world of real estate and economic indicators during significant periods of economic turbulence, including the Great Recession and the Covid-19 pandemic. This dashboard offers interactive visualizations to help users understand the complex interplay between various economic factors and their impact on real estate markets across different states.",
                        html.Br(),
                        "Dive into our sections on Real Estate, Economic Indicators, Leading and Lagging Indicators, and the Differential Impact of economic downturns to gain a deeper understanding of market trends, policy implications, and strategic planning opportunities. Whether you're a student, researcher, policy maker, or enthusiast, our platform provides valuable data-driven insights to navigate economic challenges and opportunities."
                    ], style={'text-align': 'justify', 'font-size': '20px'}),
                    width={'size': 8, 'offset': 2}
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.Div(
                        html.Img(src='/assets/IM2.JPG', style={'width':'50%', 'height':'50%'}),
                        style={'textAlign':'center', 'marginTop': 20}
                    ),
                    width=12
                )
            )
        ], className="home-page-content", style={'padding': '20px'})
    # Page content for "Current Analysis"Current Analysis



    elif pathname == "/overview":
        homeownership_data['StateAbbrev'] = homeownership_data['State'].map(state_to_code)

    # Create the choropleth map for home ownership rates
        map_fig = px.choropleth(
        data_frame=homeownership_data,
        locationmode='USA-states',
        locations='StateAbbrev',
        scope="usa",
        color='Home Ownership Rate_Current',
        hover_name='State',
        color_continuous_scale=px.colors.sequential.Blues,
        title='Statewise Home Ownership Rate in North America',
        height=400
    )
        map_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    # Create the choropleth map for the Resident Population of the selected states
        df_filtered = realestateneconomic[realestateneconomic["State"].isin(states_of_interest)]
        df_grouped = df_filtered.groupby('State')['Resident Population, Thousands of Persons'].sum().reset_index()
        df_grouped['State'] = df_grouped['State'].map(state_to_code)

    # Create the resident population map figure
        resident_pop_fig = px.choropleth(df_grouped,
                                     locations='State', 
                                     locationmode="USA-states", 
                                     color='Resident Population, Thousands of Persons', 
                                     hover_name='State', 
                                     scope="usa",
                                     color_continuous_scale=px.colors.sequential.Plasma,
                                     labels={'Resident Population, Thousands of Persons': 'Resident Population'},
                                     title='Resident Population for Selected States')
        resident_pop_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    # Cards for text content and maps
        text_card1 = dbc.Card(
        dbc.CardBody([
            html.H4("Overview of Home Ownership Rate", className="card-title"),
            html.P("Detailed textual content 1..."),
        ]))
        text_card2 = dbc.Card(
        dbc.CardBody([
            html.H4("Residence data", className="card-title"),
            html.P("Detailed textual content 1..."),
        ]))
    

        map_card1 = dbc.Card(
        dbc.CardBody([
            html.H4("Home Ownership Rate Map", className="card-title"),
            dcc.Graph(figure=map_fig),
        ])
    )
        map_card2 = dbc.Card(
        dbc.CardBody([
            html.H4("Resident Population Map", className="card-title"),
            dcc.Graph(figure=resident_pop_fig),
        ])
    )

    # Organizing the layout into rows and columns
        content_layout = dbc.Container([
        dbc.Row([
            dbc.Col([text_card1], width=12, style=common_style),
            dbc.Col([map_card1], width=12),
        ]),
        dbc.Row([
            dbc.Col([text_card2], width=12, style=common_style),
            dbc.Col([map_card2], width=12)
        ])
    ])

        return content_layout


    # Page content for "Real Estate"
    elif pathname == "/real-estate":
        return html.Div([
            dcc.Tabs(id="tabs-real-estate", value='tab-home-ownership', children=[
                dcc.Tab(label="HomeOwnership Rate ", value="homeownership-rate"),
                dcc.Tab(label="House Price Index", value="house-price-index"),
                dcc.Tab(label="ZHVI", value="zillow-home-value-index"),
                dcc.Tab(label="Median Household Income", value="median-household-income"),
                dcc.Tab(label="Per Capita Personal Income", value="per-capita-personal-income"),
                dcc.Tab(label="Regional Price Parities", value="regional-price-parities-services-housing"),
                dcc.Tab(label="Resident Population", value="resident-population-thousands-of-persons"),
                dcc.Tab(label="New Houses Sold by Sales Price in USA", value="new-houses-sold-usa"),
                dcc.Tab(label="Insights", value="insights"),
                
            ]), 
            html.Div(id='tabs-content-real-estate')
         ])
        
    # Page content for "Economic Indicators"
    elif pathname == "/economic-indicators":
        return html.Div([
            dcc.Tabs(id="tabs-economic-indicators", value='tab-unemployment-rate',children=[
                
                dcc.Tab(label="Labor Force Participation Rate", value="labor-force-participation-rate"),
                dcc.Tab(label="Unemployment Rate", value="unemployment-rate-in-percent"),
                dcc.Tab(label="Employed persons", value="employed-persons"),
                dcc.Tab(label="State tax collection", value="state-tax-collection"),
                dcc.Tab(label="State minimum wage", value="state-minimum-wage"),
                dcc.Tab(label="Bachelor Degree or Higher", value="bachelor-degree-or-higher"),
                dcc.Tab(label="Economic Insights", value="Economic Insights"),
            ]),
            html.Div(id='tabs-content-economic-indicators')
         ])
    # Page content for "Leading and Lagging Indicators"
    
    elif pathname == "/leading-lagging-indicators":
        return html.Div([
        dcc.Tabs(id="tabs-leading-lagging", value='tab-leading', children=[
            dcc.Tab(label='Leading Indicators', value='tab-leading'),
            dcc.Tab(label='Lagging Indicators', value='tab-lagging'),
        ]),
        html.Div(id='tabs-content-leading-lagging'),
        
    ])


    # Page content for "Differential Impact"
    
       
    else:
        return html.P("404: Page not found. Please select an option from the menu.")



##updating Live Date and time feature
dcc.Interval(
    id='interval-component',
    interval=1*1000,  # in milliseconds, 1*1000 means 1 second
    n_intervals=0
),
@app.callback(
    Output('live-time', 'children'),
    [Input('interval-component', 'n_intervals')]
)
def update_time(n):
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Part E: Callback for House Price Index Leading and Lagging Indicators Content
# Define common styles for cards and titles for consistency
card_style = {
            'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.2)',
            'transition': '0.3s',
            'borderRadius': '5px',  # Rounded borders
            'margin': '10px',  # Margin around cards for spacing
        }
title_style = {**common_style, 'textAlign': 'center', 'marginBottom': '20px'}

#Callback for Real Estate
#Callback for HomeOwnership Rate
@app.callback(
    Output('tabs-content-real-estate', 'children'),
    [Input('tabs-real-estate', 'value')]
)
def render_real_estate_tab_content(tab_value):
    if tab_value == "house-price-index":
        

        # Define the layout for the House Price Index tab content
        content = html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.H5("Select States", className="card-title", style=title_style),
                            dcc.Dropdown(
                                id='state-dropdown-hpi',
                                options=[{'label': state, 'value': state} for state in realestateneconomic['State'].unique()],
                                value=realestateneconomic['State'].unique().tolist(),
                                multi=True,
                                placeholder="Select States",
                            ),
                        ]), style=card_style
                    ),
                ], width=6),
                
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.H5("Select Periods", className="card-title", style=title_style),
                            dcc.Dropdown(
                                id='period-dropdown-hpi',
                                options=[{'label': period, 'value': period} for period in realestateneconomic['Period'].unique()],
                                value=realestateneconomic['Period'].unique().tolist(),
                                multi=True,
                                placeholder="Select Periods",
                            ),
                        ]), style=card_style
                    ),
                ], width=6),
            ], className="mb-4", justify="center"),  # Center the row content
            
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.H5("House Price Index Analysis", className="card-title", style=title_style),
                            dcc.Graph(id='house-price-index-graph'),
                        ]), style=card_style
                    ),
                ], width=12),
            ], className="mb-4", justify="center"),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.H5("Analysis", className="card-title", style=title_style),
                            html.P("Here are some insights into the House Price Index:", style=common_style),
                            html.P("1. The House Price Index has shown significant growth in certain regions, indicating a robust real estate market.", style=common_style),
                            html.P("2. Factors contributing to this growth include low interest rates and an increase in remote working.", style=common_style),
                            # Add more paragraphs as needed
                        ]), style=card_style
                    ),
                ], width=12),
            ], className="mb-4", justify="center"),
        ])
        
        return content

#callback for Zillow home value index   
    elif tab_value == 'zillow-home-value-index':
    # Reuse the defined styles for consistency across tabs
        

    # Define the layout for the Zillow Home Value Index tab content
        content = html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Select States", className="card-title", style=title_style),
                        dcc.Dropdown(
                            id='state-dropdown-zhvi',
                            options=[{'label': state, 'value': state} for state in realestateneconomic['State'].unique()],
                            value=realestateneconomic['State'].unique().tolist(),
                            multi=True,
                            placeholder="Select States",
                        ),
                    ]), style=card_style
                ),
            ], width=6),

            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Select Periods", className="card-title", style=title_style),
                        dcc.Dropdown(
                            id='period-dropdown-zhvi',
                            options=[{'label': period, 'value': period} for period in realestateneconomic['Period'].unique()],
                            value=realestateneconomic['Period'].unique().tolist(),
                            multi=True,
                            placeholder="Select Periods",
                        ),
                    ]), style=card_style
                ),
            ], width=6),
        ], className="mb-4", justify="center"),  # Center the row content
        
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Zillow Home Value Index Analysis", className="card-title", style=title_style),
                        dcc.Graph(id='zillow-home-value-index-graph'),
                    ]), style=card_style
                ),
            ], width=12),
        ], className="mb-4", justify="center"),
        
        dbc.Row([
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.H5("Analysis", className="card-title", style=title_style),
                            html.P("Here are some insights into the Zillow Home Value Index:", style=common_style),
                            html.P("1. The House Price Index has shown significant growth in certain regions, indicating a robust real estate market.", style=common_style),
                            html.P("2. Factors contributing to this growth include low interest rates and an increase in remote working.", style=common_style),
                            # Add more paragraphs as needed
                        ]), style=card_style
                    ),
                ], width=12),
            ], className="mb-4", justify="center"),
    ])
    
        return content

#Callback for Median household income        
    elif tab_value == 'median-household-income':
        content = html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Select States", className="card-title", style=title_style),
                        dcc.Dropdown(
                            id='state-dropdown-mhi',  # Updated ID to reflect median household income
                            options=[{'label': state, 'value': state} for state in realestateneconomic['State'].unique()],
                            value=realestateneconomic['State'].unique().tolist(),
                            multi=True,
                            placeholder="Select States",
                        ),
                    ]), style=card_style
                ),
            ], width=6),

            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Select Periods", className="card-title", style=title_style),
                        dcc.Dropdown(
                            id='period-dropdown-mhi',  # Updated ID to reflect median household income
                            options=[{'label': period, 'value': period} for period in realestateneconomic['Period'].unique()],
                            value=realestateneconomic['Period'].unique().tolist(),
                            multi=True,
                            placeholder="Select Periods",
                        ),
                    ]), style=card_style
                ),
            ], width=6),
        ], className="mb-4", justify="center"),  # Center the row content
        
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Median Household Income Analysis", className="card-title", style=title_style),
                        dcc.Graph(id='median-household-income-graph'),
                    ]), style=card_style
                ),
            ], width=12),
        ], className="mb-4", justify="center"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Analysis", className="card-title", style=title_style),
                        html.P("Here are some insights into the Median Household Income:", style=common_style),
                        html.P("1. The Median Household Income has varied significantly across different states, reflecting economic diversity.", style=common_style),
                        html.P("2. Economic policies, employment opportunities, and demographic factors greatly influence median household income levels.", style=common_style),
                        # Add more paragraphs as needed
                    ]), style=card_style
                ),
            ], width=12),
        ], className="mb-4", justify="center"),
    ])
    
        return content
        
#callback for HomeOwnership Rate  
    elif tab_value == 'homeownership-rate':
        content = html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Select States", className="card-title", style=title_style),
                        dcc.Dropdown(
                            id='state-dropdown-hpi',  # Updated ID to reflect homeownership rate
                            options=[{'label': state, 'value': state} for state in realestateneconomic['State'].unique()],
                            value=realestateneconomic['State'].unique().tolist(),
                            multi=True,
                            placeholder="Select States",
                        ),
                    ]), style=card_style
                ),
            ], width=6),

            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Select Periods", className="card-title", style=title_style),
                        dcc.Dropdown(
                            id='period-dropdown-hpi',  # Updated ID to reflect homeownership rate
                            options=[{'label': period, 'value': period} for period in realestateneconomic['Period'].unique()],
                            value=realestateneconomic['Period'].unique().tolist(),
                            multi=True,
                            placeholder="Select Periods",
                        ),
                    ]), style=card_style
                ),
            ], width=6),
        ], className="mb-4", justify="center"),  # Center the row content

        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Homeownership Rate Analysis", className="card-title", style=title_style),
                        dcc.Graph(id='homeownership-rate-graph'),
                    ]), style=card_style
                ),
            ], width=12),
        ], className="mb-4", justify="center"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Analysis", className="card-title", style=title_style),
                        html.P("Here are some insights into the Homeownership Rate:", style=common_style),
                        html.P("1. Homeownership rates vary by state, reflecting differences in economic conditions, housing policies, and market dynamics.", style=common_style),
                        html.P("2. Trends in homeownership rates can indicate broader economic trends, such as the health of the real estate market and consumer confidence.", style=common_style),
                        # Add more paragraphs as needed
                    ]), style=card_style
                ),
            ], width=12),
        ], className="mb-4", justify="center"),
    ])
    
        return content

#callback for per-capita-personal-income   
    elif tab_value == 'per-capita-personal-income':
        content = html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Select States", className="card-title", style=title_style),
                        dcc.Dropdown(
                            id='state-dropdown-hpi',  # Ensure this ID matches the one used in your Dash app for per capita personal income
                            options=[{'label': state, 'value': state} for state in realestateneconomic['State'].unique()],
                            value=realestateneconomic['State'].unique().tolist(),
                            multi=True,
                            placeholder="Select States",
                        ),
                    ]), style=card_style
                ),
            ], width=6),

            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Select Periods", className="card-title", style=title_style),
                        dcc.Dropdown(
                            id='period-dropdown-hpi',  # Ensure this ID matches the one used in your Dash app for per capita personal income
                            options=[{'label': period, 'value': period} for period in realestateneconomic['Period'].unique()],
                            value=realestateneconomic['Period'].unique().tolist(),
                            multi=True,
                            placeholder="Select Periods",
                        ),
                    ]), style=card_style
                ),
            ], width=6),
        ], className="mb-4", justify="center"),  # Center the row content

        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Per Capita Personal Income Analysis", className="card-title", style=title_style),
                        dcc.Graph(id='per-capita-personal-income-graph'),
                    ]), style=card_style
                ),
            ], width=12),
        ], className="mb-4", justify="center"),
        
        # Analysis directly within the content, not in a card
        html.H5("Analysis", className="card-title", style=title_style),
        html.P("Here are some insights into the Per Capita Personal Income:", style=common_style),
        html.P("1. Per capita personal income varies widely across states, often reflecting the local cost of living and economic conditions.", style=common_style),
        html.P("2. This metric is crucial for understanding economic well-being at the individual level and can be influenced by factors such as industry composition and employment rates.", style=common_style),
        # Add more paragraphs as needed
    ])
    
        return content

#callback for regional price parities for housing 
    
    elif tab_value == 'regional-price-parities-services-housing':
        content = html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Select States", className="card-title", style=title_style),
                        dcc.Dropdown(
                            id='state-dropdown-hpi',  # Updated ID for regional price parities
                            options=[{'label': state, 'value': state} for state in realestateneconomic['State'].unique()],
                            value=realestateneconomic['State'].unique().tolist(),
                            multi=True,
                            placeholder="Select States",
                        ),
                    ]), style=card_style
                ),
            ], width=6),

            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Select Periods", className="card-title", style=title_style),
                        dcc.Dropdown(
                            id='period-dropdown-hpi',  # Updated ID for regional price parities
                            options=[{'label': period, 'value': period} for period in realestateneconomic['Period'].unique()],
                            value=realestateneconomic['Period'].unique().tolist(),
                            multi=True,
                            placeholder="Select Periods",
                        ),
                    ]), style=card_style
                ),
            ], width=6),
        ], className="mb-4", justify="center"),  # Center the row content

        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Regional Price Parities for Housing Analysis", className="card-title", style=title_style),
                        dcc.Graph(id='regional-price-parities-services-housing-graph'),
                    ]), style=card_style
                ),
            ], width=12),
        ], className="mb-4", justify="center"),
        
       
        html.H5("Analysis", className="card-title", style=title_style),
        html.P("Here are some insights into Regional Price Parities for SHousing:", style=common_style),
        html.P("1. Regional price parities (RPPs) vary significantly across states, highlighting differences in the cost of living, particularly in services and housing.", style=common_style),
        html.P("2. States with high RPPs for housing tend to have more expensive real estate markets and higher costs associated with services.", style=common_style),
        # Additional insights or paragraphs can be added here
    ])
    
        return content
#for resident populaiton
    elif tab_value == 'resident-population-thousands-of-persons':
        content = html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Select States", className="card-title", style=title_style),
                        dcc.Dropdown(
                            id='state-dropdown-hpi',  
                            options=[{'label': state, 'value': state} for state in realestateneconomic['State'].unique()],
                            value=realestateneconomic['State'].unique().tolist(),
                            multi=True,
                            placeholder="Select States",
                        ),
                    ]), style=card_style
                ),
            ], width=6),

            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Select Periods", className="card-title", style=title_style),
                        dcc.Dropdown(
                            id='period-dropdown-hpi', 
                            options=[{'label': period, 'value': period} for period in realestateneconomic['Period'].unique()],
                            value=realestateneconomic['Period'].unique().tolist(),
                            multi=True,
                            placeholder="Select Periods",
                        ),
                    ]), style=card_style
                ),
            ], width=6),
        ], className="mb-4", justify="center"),  # Center the row content

        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Resident Population Analysis for the Selected States", className="card-title", style=title_style),
                        dcc.Graph(id='resident-population-thousands-of-persons-graph'),
                    ]), style=card_style
                ),
            ], width=12),
        ], className="mb-4", justify="center"),
        
       
        html.H5("Analysis", className="card-title", style=title_style),
        html.P("The chart depicts how the resident population has been receiving a rising trend in North Carolina, California, Florida, and Texas during the period, with the population sizes in California being the highest. Texas and Florida even though trailed California a little they too have the same trends. On the other hand, North Carolina which had the lowest numbers all the times has shown a steady growth. The overall trend is a gradual and steady rise in the data of these states. Therefore, it can be concluded that these states have been able to conduct an economic expansion and administration system that is effective enough for their steadily growing populations which is a good indicator.", style=common_style),
    ])
        return content   
# for New houses sold data        
    elif tab_value == "new-houses-sold-usa":
        content = html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Select Period", className="card-title", style=title_style),
                        dcc.Dropdown(
                            id='period-dropdown-nhs',
                            options=[{'label': period, 'value': period} for period in differential_data['Period'].unique()],
                            value=differential_data['Period'].unique().tolist(),  # Assuming you want to allow multi-selection and have all periods selected by default
                            multi=True,
                            placeholder="Select Period",
                        ),
                    ]), style=card_style
                ),
            ], md=6),
        ], className="mb-4", justify="start"),  # Adjust justify to "start" to align with the left side

        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        dcc.Graph(id='new-houses-sold-usa-graph'),
                    ]), style=card_style
                ),
            ], width=12),
        ], className="mb-4"),
    ])

        return content

        # Call back for insights
    elif tab_value == 'insights':  # Ensure this matches your actual tab's value
        return html.Div([
        html.H3("Insights", style={'textAlign': 'center', 'fontSize': 30}),
        dbc.Row([
            dbc.Col(html.Div([
                html.Ul([
                    html.Li("While the sale of brand-new houses varied considerably, with observable changes in sales both in volume and price ranges during the pre-Covid, COVID-19, and post-Covid eras, the average homeownership rate nationwide is still very steady.", style={'fontSize': 22, 'textAlign': 'justify'}),
                    html.Li("The Great Recession had a major adverse effect on several aspects of the housing market, as demonstrated by the evident decline in the House Price Index, an increase in rental and home vacancy rates, the decline in the Zillow Home Value Index, and the decline in homeownership rates in the states which were included.", style={'fontSize': 22, 'textAlign': 'justify'}),
                    html.Li("The impact of the COVID-19 pandemic on real estate markets differed by state, as shown by these visualizations, which also illustrate variations in homeownership rates during the epidemic along with increases in property prices and rental vacancy rates.", style={'fontSize': 22, 'textAlign': 'justify'}),
                    html.Li("It demonstrates how different regions’ local housing service expenses and homeownership rates have been affected by both the Great Recession and COVID-19, with some obvious patterns being expanding service prices in California and changing homeownership rates, especially in Texas and North Carolina.", style={'fontSize': 22, 'textAlign': 'justify'}),
                    html.Li("These additionally show how the Great Crisis and COVID-19 altered the dynamics of the housing market, with sales of lower-priced homes declining significantly during the crisis and rising throughout higher price ranges following COVID.", style={'fontSize': 22, 'textAlign': 'justify'}),
                ])
            ]), width=12),
        ])
    ])

#Call for Economic Indicators content_state-tax-collection
@app.callback(
    Output('tabs-content-economic-indicators', 'children'),
    [Input('tabs-economic-indicators', 'value')]
)
def render_real_estate_tab_content(tab_value):
    if tab_value == "state-tax-collection":
        content = html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Select States", className="card-title", style=title_style),
                        dcc.Dropdown(
                            id='state-dropdown-hpi',  # Updated ID for state tax collection
                            options=[{'label': state, 'value': state} for state in realestateneconomic['State'].unique()],
                            value=realestateneconomic['State'].unique().tolist(),
                            multi=True,
                            placeholder="Select States",
                        ),
                    ]), style=card_style
                ),
            ], width=6),

            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Select Periods", className="card-title", style=title_style),
                        dcc.Dropdown(
                            id='period-dropdown-hpi',  # Updated ID for state tax collection
                            options=[{'label': period, 'value': period} for period in realestateneconomic['Period'].unique()],
                            value=realestateneconomic['Period'].unique().tolist(),
                            multi=True,
                            placeholder="Select Periods",
                        ),
                    ]), style=card_style
                ),
            ], width=6),
        ], className="mb-4", justify="center"),  # Center the row content

        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H5("State Tax Collection Analysis", className="card-title", style=title_style),
                        dcc.Graph(id='state-tax-collection-graph'),
                    ]), style=card_style
                ),
            ], width=12),
        ], className="mb-4", justify="center"),

        # Direct content analysis
        html.H5("Analysis", className="card-title", style=title_style),
        html.P("Here are some insights into the State Tax Collection:", style=common_style),
        html.P("1. Tax collection varies significantly among states, influenced by the state's economic policies, tax rates, and the economic activities of its residents.", style=common_style),
        html.P("2. Trends in tax collection can provide insights into the economic health of a state, changes in policy, and shifts in population dynamics.", style=common_style),
        
    ])

        return content

#callback for state-minimum-wage   
    elif tab_value == 'state-minimum-wage':
        content = html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Select States", className="card-title", style=title_style),
                        dcc.Dropdown(
                            id='state-dropdown-hpi',  # Updated ID for state minimum wage
                            options=[{'label': state, 'value': state} for state in realestateneconomic['State'].unique()],
                            value=realestateneconomic['State'].unique().tolist(),
                            multi=True,
                            placeholder="Select States",
                        ),
                    ]), style=card_style
                ),
            ], width=6),

            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Select Periods", className="card-title", style=title_style),
                        dcc.Dropdown(
                            id='period-dropdown-hpi',  # Updated ID for state minimum wage
                            options=[{'label': period, 'value': period} for period in realestateneconomic['Period'].unique()],
                            value=realestateneconomic['Period'].unique().tolist(),
                            multi=True,
                            placeholder="Select Periods",
                        ),
                    ]), style=card_style
                ),
            ], width=6),
        ], className="mb-4", justify="center"),  # Center the row content

        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H5("State Minimum Wage Analysis", className="card-title", style=title_style),
                        dcc.Graph(id='state-minimum-wage-graph'),
                    ]), style=card_style
                ),
            ], width=12),
        ], className="mb-4", justify="center"),

        # Direct content analysis
        html.H5("Analysis", className="card-title", style=title_style),
        html.P("Here are some insights into the State Minimum Wage:", style=common_style),
        html.P("1. The minimum wage varies across states, reflecting differing local living costs and economic policies.", style=common_style),
        html.P("2. Changes in the minimum wage can influence local economies, affecting employment rates, consumer spending, and poverty levels.", style=common_style),
        # Add more paragraphs as needed
    ])

        return content

#callback for bachelor-degree-or-higher-graph
    elif tab_value == 'bachelor-degree-or-higher':
        content = html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Select States", className="card-title", style=title_style),
                        dcc.Dropdown(
                            id='state-dropdown-hpi',  # Updated ID for bachelor degree or higher
                            options=[{'label': state, 'value': state} for state in realestateneconomic['State'].unique()],
                            value=realestateneconomic['State'].unique().tolist(),
                            multi=True,
                            placeholder="Select States",
                        ),
                    ]), style=card_style
                ),
            ], width=6),

            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Select Periods", className="card-title", style=title_style),
                        dcc.Dropdown(
                            id='period-dropdown-hpi',  # Updated ID for bachelor degree or higher
                            options=[{'label': period, 'value': period} for period in realestateneconomic['Period'].unique()],
                            value=realestateneconomic['Period'].unique().tolist(),
                            multi=True,
                            placeholder="Select Periods",
                        ),
                    ]), style=card_style
                ),
            ], width=6),
        ], className="mb-4", justify="center"),  # Center the row content

        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Bachelor Degree or Higher Analysis", className="card-title", style=title_style),
                        dcc.Graph(id='bachelor-degree-or-higher-graph'),
                    ]), style=card_style
                ),
            ], width=12),
        ], className="mb-4", justify="center"),

        # Direct content analysis
        html.H5("Analysis", className="card-title", style=title_style),
        html.P("Here are some insights into the percentage of adults with a bachelor's degree or higher:", style=common_style),
        html.P("1. Educational attainment levels vary significantly across states, often influenced by access to higher education institutions and state education policies.", style=common_style),
        html.P("2. Regions with higher percentages of degree-holders often correlate with higher income levels, lower unemployment rates, and improved social outcomes.", style=common_style),
        # Add more paragraphs as needed
    ])

        return content
 
#Call back for rednering content for employed-persons  
    elif tab_value == 'employed-persons':
        return html.Div([
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(
                        id='state-dropdown-hpi',
                        options=[{'label': state, 'value': state} for state in realestateneconomic['State'].unique()],
                        value=realestateneconomic['State'].unique().tolist(),
                        multi=True,
                        placeholder="Select States",
                    ),
                    md=6
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='period-dropdown-hpi',
                        options=[{'label': period, 'value': period} for period in realestateneconomic['Period'].unique()],
                        value=realestateneconomic['Period'].unique().tolist(),
                        multi=True,
                        placeholder="Select Periods",
                    ),
                    md=6
                ),
            ]),
            dbc.Row(
                dbc.Col(dcc.Graph(id='employed-persons-graph'), width=12)
            )
        ])      
# Part of the callback for rendering tab content        
    elif tab_value == 'labor-force-participation-rate':
        return dbc.Card(
        [
            dbc.CardHeader(html.H4("Labor Force Participation Rate", className="card-title")),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(
                        dcc.Dropdown(
                            id='state-dropdown-lfpr',
                            options=[{'label': state, 'value': state} for state in realestateneconomic['State'].unique()],
                            value=realestateneconomic['State'].unique().tolist(),
                            multi=True,
                            placeholder="Select States",
                        ),
                        md=6
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id='period-dropdown-lfpr',
                            options=[{'label': period, 'value': period} for period in realestateneconomic['Period'].unique()],
                            value=realestateneconomic['Period'].unique().tolist(),
                            multi=True,
                            placeholder="Select Periods",
                        ),
                        md=6
                    ),
                    
                ]),
                dbc.Row(
                    dbc.Col(dcc.Graph(id='labor-force-participation-rate-graph'), width=12)
                ),
                # Placeholder for summary statistics
                html.Div(id='summary-statistics')
            ])
        ]
    )
     
# Page content for "Unemployment Rate" with shared dropdowns
    elif tab_value == 'unemployment-rate-in-percent':
        # Common dropdowns for State and Period, which will be shared by all three graphs
        dropdowns = html.Div([
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(
                        id='unemployment-state-dropdown',
                        options=[{'label': state, 'value': state} for state in realestateneconomic['State'].unique()],
                        value=realestateneconomic['State'].unique().tolist(),
                        multi=True,
                        placeholder="Select States",
                    ),
                    md=6
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='unemployment-period-dropdown',
                        options=[{'label': period, 'value': period} for period in realestateneconomic['Period'].unique()],
                        value=realestateneconomic['Period'].unique().tolist(),
                        multi=True,
                        placeholder="Select Periods",
                    ),
                    md=6
                ),
            ], className="mb-3"),  # Add margin-bottom for spacing
        ])

        # Cards for each of the three graphs
        cards = html.Div([
            dbc.Row([
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.H4("Unemployment Rate in Percent", className="card-title"),
                            dcc.Graph(id='unemployment-rate-in-percent-graph')
                        ])
                    ), 
                    width=12
                )
            ], className="mb-3"),  # Add margin-bottom for spacing between cards

            dbc.Row([
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.H4("Unemployed Persons", className="card-title"),
                            dcc.Graph(id='unemployed-persons-graph')
                        ])
                    ),
                    width=12
                )
            ], className="mb-3"),  # Add margin-bottom for spacing between cards

            dbc.Row([
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.H4("Unemployment Duration", className="card-title"),
                            dcc.Graph(id='unemployment-duration-graph')
                        ])
                    ),
                    width=12
                )
            ]),
        ])

        # Combine dropdowns and cards to render them together
        return html.Div([dropdowns, cards])
    # Call back for insights
    elif tab_value == 'Economic Insights':  # Ensure this matches your actual tab's value
        return html.Div([
        html.H3("Economic Insights", style={'textAlign': 'center', 'fontSize': 30}),
        dbc.Row([
            dbc.Col(html.Div([
                html.Ul([
                    html.Li("The visualization illustrates the link between homeownership and unemployment rates across various states, indicating that regions with higher levels of unemployment often have lower homeownership rates.", style={'fontSize': 22, 'textAlign': 'justify'}),
                    html.Li("The illustration also shows that though state minimum salaries had usually risen over time, jobs fell sharply during the Great Recession and COVID-19, with a noticeable recovery period following COVID.", style={'fontSize': 22, 'textAlign': 'justify'}),
                    html.Li("It implies that all through the Great Recession and COVID-19, state revenue from taxes and labor force participation rates varied significantly, indicating the economic stress and recovery trends in the chosen states.", style={'fontSize': 22, 'textAlign': 'justify'}),
                    html.Li("The visual representation also demonstrates how the COVID-19 pandemic and the Great Recession both had a discernible effect on median household and per capita personal income, with both usually falling during the recessions and beginning to recover in the post-recession and post-COVID periods.", style={'fontSize': 22, 'textAlign': 'justify'}),
                ])
            ]), width=12),
        ])
    ])


# Main Callback for updating summary statistics

@app.callback(
    Output('summary-statistics', 'children'),
    [Input('state-dropdown-lfpr', 'value'),
     Input('period-dropdown-lfpr', 'value')]
)
def update_summary_statistics(selected_states, selected_periods):
    
    if not selected_states or not selected_periods:
        return "Please select both states and periods."

    filtered_df = realestateneconomic[
        (realestateneconomic['State'].isin(selected_states)) & 
        (realestateneconomic['Period'].isin(selected_periods))
    ]
    
    # Group by state and calculate mean and median
    grouped = filtered_df.groupby('State')['Labor Force Participation Rate in Percent, Annual']
    mean_rates = grouped.mean().reset_index(name='mean')
    median_rates = grouped.median().reset_index(name='median')

    # Combine mean and median into a single DataFrame
    statistics = pd.merge(mean_rates, median_rates, on='State')

    # Construct the children components with the calculated statistics for each state
    card_content = dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(html.H5(state, className="card-title")),
                        dbc.CardBody([
                            html.P(f"Mean Labor Force Participation Rate: {mean_rate:.2f}%", className="card-text"),
                            html.P(f"Median Labor Force Participation Rate: {median_rate:.2f}%", className="card-text")
                        ])
                    ],
                    className="mb-3"
                ),
                md=4  # Adjust the size of the column here depending on how many cards per row you want
            )
            for state, mean_rate, median_rate in zip(statistics['State'], statistics['mean'], statistics['median'])
        ],
        className="mb-4"
    )

    return card_content



# Callback for leadnig and lagging indicators- Extra Credit                       
@app.callback(
    Output('tabs-content-leading-lagging', 'children'),
    [Input('tabs-leading-lagging', 'value')]
)
def render_leading_lagging_content(tab):
    if tab == 'tab-leading':
        # Layout for leading indicators
        return html.Div([
            html.H3('Leading Indicators'),
            dcc.Checklist(
                id='leading-checklist',
                options=[
                    {'label': 'Zillow Home Value Index', 'value': 'Zillow Home Value Index in Dollars'},
                    {'label': 'State minimum wage', 'value': 'State minimum wage  Dollars per Hour'}
                ],
                value=['Zillow Home Value Index in Dollars', 'State minimum wage  Dollars per Hour'],
                inline=True
            ),
            dcc.Graph(id='leading-indicators-graph'),
            html.Div([  # Corrected from 'html.div' to 'html.Div'
                html.H4('Analysis', className='mt-4'),  # Corrected from 'classname' to 'className'
                html.P("The first derivation on this graph unveils a steady uptrend for both the Zillow Home Value Index and the state minimum wage, also suggesting that there could be economic development and pressure on the inflation channels. The ZHVI's growth is evidence of a flourishing real estate market, in which the factors propelling the rise outweigh supply or those that improve market conditions. At the same time, the state theory of minimum wage climbing at a snail's pace is explained by aforementioned legislative and financial procedures that are aimed to tackle cost of living issues. This V-shaped pattern formed by these two lines around 2008 and 2021 denotes that the period from these two dates when living cost and wage were growing in the same pace. But after this period, we have observed a lopsided increase in the value of homes, which now seems to be more superior to the wage increase. This gap may carry serious consequences for housing affordability and, consequently, for the uniform profitability of economic processes.", className='analysis-text')  # Corrected from 'html.p' to 'html.P' and added 'className'
            ], className='analysis-section')  # Corrected from 'classname' to 'className'
        ])
    elif tab == 'tab-lagging':
        # Layout for lagging indicators
        return html.Div([
            html.H3('Lagging Indicators'),
            dcc.Checklist(
                id='lagging-checklist',
                options=[
                    {'label': 'Unemployment Rate', 'value': 'UR'},
                    {'label': 'State Tax Collection', 'value': 'STC'}
                ],
                value=['UR', 'STC'],
                inline=True
            ),
            dcc.Graph(id='lagging-indicators-graph'),
            html.Div([  # Corrected from 'html.div' to 'html.Div'
                html.H4('Analysis', className='mt-4'),  # Corrected from 'classname' to 'className'
                html.P("The contrasting trend between the long term indicator such as the unemployment average with the state tax collection, as presented in this visual, clearly indicates an inconsistency between the trend. To begin with, the indicators play opposite; hence, with a reduction in the unemployment rate, a state tax collection tends to increase and this may be understood as a sign of economic recovery or growth. Conversely, by about the year 2010 the curve steepens sharply. The higher rate of unemployment causes a sudden jump, possibly foreshadowing an economic crisis; this might be countered by a reduction in tax collection as income and consumption reduces. On the other hand, the State tax collection is always steadily increasing regardless of the rise in the unemployment level. This means that either the State tax base has expanded, & the rates of the State tax increased or the aggregate of the economic activities taxed by the State have grown much more than the decline in employment. The sharp decrease of unemployment from 2015 onwards in when compared with the rapid growth tax revenue could indicate a good economic recovery, where both labor productivity increase as well as state revenue. The spike is obvious at the end of the graph, probably owing to the COVID-19 pandemic, which will bring about short time-lag of tax collections in the state, maybe due to some fiscal measures and delayed tax filing. The two scholars, however, did not depict the same picture from the same cloth. This dichotomy in the two indicators represents the complicated hem of economic health and the multifarious effects of policies, taxation, and job incomes.", className='analysis-text')  # Corrected from 'html.p' to 'html.P' and added 'className'
            ], className='analysis-section')  # Corrected from 'classname' to 'className'
        ])
    else:
        return html.P("404: Page not found. Please select an option from the menu.")

# Callback for differential impact--extra credit
# Callback for differential impact content
@app.callback(
    Output('tabs-content-differential-impact', 'children'),  # Make sure this matches the id of the content container for differential impact
    [Input('tabs-differential-impact', 'value')]  # Ensure there is a component with this id that can trigger the callback
)
def render_differential_impact_content(tab_value):
    # Assuming you have some logic based on the tab_value, here's a simplified example
    if tab_value == 'recession-impact':
        # Your logic to create a graph or content for recession impact
        pass
    elif tab_value == 'covid-impact':
        # Your logic to create a graph or content for covid impact
        pass
    # Return the content for the selected tab
    return html.Div("Content based on the tab selected")


#Part F: Graph Update Callbacks
# Callback for updating the leading indicators graph
@app.callback(
    Output('leading-indicators-graph', 'figure'),
    [Input('leading-checklist', 'value')]
)
def update_leading_graph(selected_averages):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Assume leading_avg_data['Year'] is of datetime type and extracting year as integer
    leading_avg_data['Year'] = leading_avg_data['Year'].dt.year

    # Get all unique years
    all_years = sorted(leading_avg_data['Year'].unique())

    if 'Zillow Home Value Index in Dollars' in selected_averages:
        fig.add_trace(
            go.Scatter(
                x=leading_avg_data['Year'],
                y=leading_avg_data['Zillow Home Value Index in Dollars'],
                name='Avg. Zillow Home Value Index ($)',
                mode='lines+markers',
                marker=dict(size=10)
            ),
            secondary_y=False,
        )
    
    if 'State minimum wage  Dollars per Hour' in selected_averages:
        fig.add_trace(
            go.Scatter(
                x=leading_avg_data['Year'],
                y=leading_avg_data['State minimum wage  Dollars per Hour'],
                name='Avg. State minimum wage  ($/hr)',
                marker_color='green',
                mode='lines+markers',
                marker=dict(size=10)
            ),
            secondary_y=True,
        )
    
    # Set x-axis to display every year
    fig.update_xaxes(
        tickvals=all_years,  # Specify which ticks to display
        ticktext=[str(year) for year in all_years],  # Text to display at each tick
        title='Year'
    )
    fig.update_yaxes(title_text="Avg. Zillow Home Value Index ($)", secondary_y=False)
    fig.update_yaxes(title_text="Avg. State minimum wage  ($/hr)", secondary_y=True)
    fig.update_layout(
        title_text="Leading Indicators: Avg. Zillow Home Value Index vs. State minimum wage",
        plot_bgcolor="white",
        font=dict(size=12),
    )
    return fig
#callback for house price index
@app.callback(
    Output('house-price-index-graph', 'figure'),
    [Input('state-dropdown-hpi', 'value'),
     Input('period-dropdown-hpi', 'value')]
)
def update_house_price_index_graph(selected_states, selected_periods):
    filtered_df = realestateneconomic[
        (realestateneconomic['State'].isin(selected_states)) & 
        (realestateneconomic['Period'].isin(selected_periods))
    ]
    filtered_df['Year'] = pd.DatetimeIndex(filtered_df['Year']).year
    highest_peak = filtered_df.loc[filtered_df['All Transactions House Price Index'].idxmax()]
    lowest_peak = filtered_df.loc[filtered_df['All Transactions House Price Index'].idxmin()]

    fig = px.line(
        filtered_df,
        x='Year', 
        y='All Transactions House Price Index', 
        color='State', 
        line_group='Period',
        markers=True
    )
    fig.update_xaxes(tickvals=filtered_df['Year'].unique(), tickformat="%Y", title='Year')
    fig.update_layout(yaxis_title='House Price Index')

    # Add annotation for the highest peak
    fig.add_annotation(
        x=highest_peak['Year'],
        y=highest_peak['All Transactions House Price Index'],
        text=f"Highest Peak of HPI in California in the year 2022: {highest_peak['All Transactions House Price Index']}",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-40
    )
    # Add annotation for the lowest peak
    fig.add_annotation(
        x=lowest_peak['Year'],
        y=lowest_peak['All Transactions House Price Index'],
        text=f"Lowest Peak-Texas-2005: {lowest_peak['All Transactions House Price Index']}",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-20
    )
    return fig
#Callback for Resident Population
@app.callback(
    Output('resident-population-thousands-of-persons-graph', 'figure'),
    [Input('state-dropdown-hpi', 'value'),  # Assuming you have a dropdown for state selection
     Input('period-dropdown-hpi', 'value')]  # Assuming you have a dropdown for period selection
)
def update_resident_population_graph(selected_states, selected_periods):
    # Filter the dataframe based on selected states and periods
    filtered_df = realestateneconomic[
        (realestateneconomic['State'].isin(selected_states)) &
        (realestateneconomic['Period'].isin(selected_periods))
    ]

    filtered_df['Year'] = pd.DatetimeIndex(filtered_df['Year']).year
    fig = px.line(
        filtered_df,
        x='Year',
        y='Resident Population, Thousands of Persons',
        color='State',
        line_group='Period',
        markers=True
    )
    fig.update_xaxes(tickvals=filtered_df['Year'].unique(), tickformat="%Y", title='Year')
    fig.update_layout(yaxis_title='Resident Population, Thousands of Persons')
    return fig
# Callback for updating the lagging indicators graph
@app.callback(
    Output('lagging-indicators-graph', 'figure'),
    [Input('lagging-checklist', 'value')]
)
def update_lagging_graph(selected_averages):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Assuming lagging_avg_data['Year'] is already in the correct format, e.g., integer year values
    all_years = sorted(lagging_avg_data['Year'].unique())

    # Add Unemployment Rate trace if selected
    if 'UR' in selected_averages:
        fig.add_trace(
            go.Scatter(
                x=lagging_avg_data['Year'],
                y=lagging_avg_data['Unemployment Rate in Percent'],
                name='Avg. Unemployment Rate (%)',
                mode='lines+markers',
                marker=dict(size=10)
            ),
            secondary_y=False,
        )
    
    # Add State Tax Collection trace if selected
    if 'STC' in selected_averages:
        fig.add_trace(
            go.Scatter(
                x=lagging_avg_data['Year'],
                y=lagging_avg_data['State tax collection Millions of U.S. Dollars'],
                name='Avg. State Tax Collection (Millions $)',
                marker_color='red',
                mode='lines+markers',
                marker=dict(size=10)
            ),
            secondary_y=True,
        )
    
    # Set x-axis to display every year
    fig.update_xaxes(
        tickvals=all_years,
        tickformat="%Y",  # Format the tick labels as just the year
        title='Year'
    )
    
    # Configure the layout of the figure
    fig.update_layout(
        title_text="Lagging Indicators: Avg. Unemployment Rate vs. State Tax Collection",
        plot_bgcolor="white",
        font=dict(size=12),
    )
    fig.update_yaxes(title_text="Avg. Unemployment Rate (%)", secondary_y=False)
    fig.update_yaxes(title_text="Avg. State Tax Collection (Millions $)", secondary_y=True)
    
    return fig

#callback for Zillow Home Value Index Graph
@app.callback(
    Output('zillow-home-value-index-graph', 'figure'),
    [Input('state-dropdown-zhvi', 'value'),
     Input('period-dropdown-zhvi', 'value')]
)
def update_zillow_home_value_index_graph(selected_states, selected_periods):
    filtered_df = realestateneconomic[(realestateneconomic['State'].isin(selected_states)) & 
                                      (realestateneconomic['Period'].isin(selected_periods))]
    # Ensure 'Year' is interpreted as just the year
    filtered_df['Year'] = pd.DatetimeIndex(filtered_df['Year']).year


    fig = px.line(filtered_df, x='Year', y='Zillow Home Value Index in Dollars', color='State', line_group='Period',
                  markers=True, title='Zillow Home Value Index in Dollars Comparison')
    fig.update_layout(
    xaxis = {
        'title': 'Year',
        'tickmode': 'array',
        'tickvals': filtered_df['Year'].unique(),  # Ensure this array contains all unique years you want to display
        'ticktext': [str(year) for year in filtered_df['Year'].unique()]  # Optional: Format how the tick labels are presented
    },
    yaxis = {
        'title': 'Zillow Home Value Index ($))'
    }
)
    # Identify the highest and lowest Zillow Home Value Index within the filtered DataFrame
    highest_index = filtered_df.loc[filtered_df['Zillow Home Value Index in Dollars'].idxmax()]
    lowest_index = filtered_df.loc[filtered_df['Zillow Home Value Index in Dollars'].idxmin()]
    # Add annotation for the highest index
    fig.add_annotation(
        x=highest_index['Year'],
        y=highest_index['Zillow Home Value Index in Dollars'],
        text=f"Highest Index: {highest_index['State']} {highest_index['Year']}: ${highest_index['Zillow Home Value Index in Dollars']}",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-40
    )

    # Add annotation for the lowest index
    fig.add_annotation(
        x=lowest_index['Year'],
        y=lowest_index['Zillow Home Value Index in Dollars'],
        text=f"Lowest Index: {lowest_index['State']} {lowest_index['Year']}: ${lowest_index['Zillow Home Value Index in Dollars']}",
        showarrow=True,
        arrowhead=3,
        ax=0,
        ay=40  # Adjusted to avoid overlap, might need fine-tuning based on your graph's scale
    )

    return fig
#callback for Median HOusehold Income Graph
@app.callback(
    Output('median-household-income-graph', 'figure'),
    [Input('state-dropdown-mhi', 'value'),
     Input('period-dropdown-mhi', 'value')]
)
def update_median_household_income_graph(selected_states, selected_periods):
    filtered_df = realestateneconomic[
        (realestateneconomic['State'].isin(selected_states)) & 
        (realestateneconomic['Period'].isin(selected_periods))
    ]
     
    filtered_df['Year'] = pd.DatetimeIndex(filtered_df['Year']).year
    fig =  px.line(
    filtered_df,
    x="Year",
    y="Median Household Income (In Dollars)",
    color="State",
    labels={"Year": "Year", "Median Household Income (In Dollars)": "Median Household Income ($)"},
    markers=True,
    symbol="State",
    line_shape="spline"
)


    fig.update_layout(
    xaxis = {
        'title': 'Year',
        'tickmode': 'array',
        'tickvals': filtered_df['Year'].unique(),  # Ensure this array contains all unique years you want to display
        'ticktext': [str(year) for year in filtered_df['Year'].unique()]  # Optional: Format how the tick labels are presented
    },
    yaxis = {
        'title': 'Median Household Income ($)'
    }
    )
    # Identify the highest and lowest Zillow Home Value Index within the filtered DataFrame
    highest_index = filtered_df.loc[filtered_df['Median Household Income (In Dollars)'].idxmax()]
    lowest_index = filtered_df.loc[filtered_df['Median Household Income (In Dollars)'].idxmin()]
    # Add annotation for the highest index
    fig.add_annotation(
        x=highest_index['Year'],
        y=highest_index['Median Household Income (In Dollars)'],
        text=f"Highest Index: {highest_index['State']} {highest_index['Year']}: ${highest_index['Median Household Income (In Dollars)']}",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-40
    )

    # Add annotation for the lowest index
    fig.add_annotation(
        x=lowest_index['Year'],
        y=lowest_index['Median Household Income (In Dollars)'],
        text=f"Lowest Index: {lowest_index['State']} {lowest_index['Year']}: ${lowest_index['Median Household Income (In Dollars)']}",
        showarrow=True,
        arrowhead=3,
        ax=0,
        ay=40  # Adjusted to avoid overlap, might need fine-tuning based on your graph's scale
    )
    return fig
#callback for HomeOwnership Rate
@app.callback(
    Output('homeownership-rate-graph', 'figure'),
    [Input('state-dropdown-hpi', 'value'),
     Input('period-dropdown-hpi', 'value')]
)
def update_homeownership_rate_graph(selected_states, selected_periods):
    filtered_df = realestateneconomic[
        (realestateneconomic['State'].isin(selected_states)) & 
        (realestateneconomic['Period'].isin(selected_periods))
    ].copy()

    filtered_df['Year'] = pd.DatetimeIndex(filtered_df['Year']).year

    fig = px.line(
        filtered_df, 
        x='Year', 
        y='HomeOwnership Rate in %', 
        color='State', 
        line_group='Period',
        markers=True
    )
    
    fig.update_layout(
        xaxis={
            'title': 'Year',
            'tickmode': 'array',
            'tickvals': filtered_df['Year'].unique(),
            'ticktext': [str(year) for year in filtered_df['Year'].unique()]
        },
        yaxis={
            'title': 'HomeOwnership Rate in %'
        }
    )

    highest_index = filtered_df.loc[filtered_df['HomeOwnership Rate in %'].idxmax()]
    lowest_index = filtered_df.loc[filtered_df['HomeOwnership Rate in %'].idxmin()]

    # Corrected the text to remove $ symbol for percentage values
    fig.add_annotation(
        x=highest_index['Year'],
        y=highest_index['HomeOwnership Rate in %'],
        text=f"Highest Rate: {highest_index['State']} {highest_index['Year']}: {highest_index['HomeOwnership Rate in %']}%",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-40
    )

    fig.add_annotation(
        x=lowest_index['Year'],
        y=lowest_index['HomeOwnership Rate in %'],
        # Corrected the typo in the field key
        text=f"Lowest Rate: {lowest_index['State']} {lowest_index['Year']}: {lowest_index['HomeOwnership Rate in %']}%",
        showarrow=True,
        arrowhead=3,
        ax=0,
        ay=40
    )

    return fig
#callback for Per Capita Personal Income in Dollars
@app.callback(
    Output('per-capita-personal-income-graph', 'figure'),
    [Input('state-dropdown-hpi', 'value'),
     Input('period-dropdown-hpi', 'value')]
)
def update_per_capita_personal_income_graph(selected_states, selected_periods):
    filtered_df = realestateneconomic[(realestateneconomic['State'].isin(selected_states)) & 
                                      (realestateneconomic['Period'].isin(selected_periods))]
    fig = px.line(filtered_df, x='Year', y='Per Capita Personal Income in Dollars', color='State', line_group='Period',
                  markers=True, title='Per Capita Personal Income in Dollars Comparison')
    fig.update_layout(xaxis_title='Year', yaxis_title='Per Capita Personal Income ($)')
    return fig   
#callback for regional-price-parities-services-housing
@app.callback(
    Output('regional-price-parities-services-housing-graph', 'figure'),
    [Input('state-dropdown-hpi', 'value'),
     Input('period-dropdown-hpi', 'value')]
)
def update_regional_price_parities_services_housing_graph(selected_states, selected_periods):
    filtered_df = realestateneconomic[(realestateneconomic['State'].isin(selected_states)) & 
                                      (realestateneconomic['Period'].isin(selected_periods))]
    fig = px.line(filtered_df, x='Year', y='Regional Price Parities: Services: Housing (Annual)', color='State', line_group='Period',
                  markers=True, title='Regional Price Parities: Services: Housing Analysis')
    fig.update_layout(xaxis_title='Year', yaxis_title='Regional Price Parities')
    return fig 

#callback for state-tax-collection Graph
@app.callback(
    Output('state-tax-collection-graph', 'figure'),
    [Input('state-dropdown-hpi', 'value'),
     Input('period-dropdown-hpi', 'value')]
)
def update_state_tax_collection_graph(selected_states, selected_periods):
    # Filter the dataframe based on the selected states and periods
    filtered_df = realestateneconomic[
        (realestateneconomic['State'].isin(selected_states)) &
        (realestateneconomic['Period'].isin(selected_periods))
    ]
    filtered_df['Year'] = pd.DatetimeIndex(filtered_df['Year']).year
    # Pivot the dataframe to have years as the index and states as the columns
    pivoted_df = filtered_df.pivot_table(
        index='Year', 
        columns='State', 
        values='State tax collection Millions of U.S. Dollars',
        aggfunc='sum'
    ).fillna(0) 
    fig = go.Figure()
    for state in pivoted_df.columns:
        fig.add_trace(
            go.Scatter(
                x=pivoted_df.index,
                y=pivoted_df[state],
                mode='lines+markers',
                name=state,
                stackgroup='one',  # define stack group
                line=dict(width=0.5),
                marker=dict(size=4),
                fill='tonexty'  # fill area between trace0 and trace1
            )
        )
    fig.update_layout(
        xaxis={
            'title': 'Year',
            'tickmode': 'array',
            'tickvals': filtered_df['Year'].unique(),
            'ticktext': [str(year) for year in filtered_df['Year'].unique()]
        },
        yaxis={
            'title': 'State Tax Collection (Millions $)'
        },) 
    return fig

#callback for state-minimum-wage
@app.callback(
    Output('state-minimum-wage-graph', 'figure'),
    [Input('state-dropdown-hpi', 'value'),
     Input('period-dropdown-hpi', 'value')]
)
def update_state_minimum_wage_graph(selected_states, selected_periods):
    filtered_df = realestateneconomic[(realestateneconomic['State'].isin(selected_states)) & 
                                      (realestateneconomic['Period'].isin(selected_periods))]
    filtered_df['Year'] = pd.DatetimeIndex(filtered_df['Year']).year
    fig = px.line(filtered_df, x='Year', y='State minimum wage  Dollars per Hour', color='State', line_group='Period',
                  markers=True, title='State minimum wage Analysis')
    fig.update_layout(
        xaxis={
            'title': 'Year',
            'tickmode': 'array',
            'tickvals': filtered_df['Year'].unique(),
            'ticktext': [str(year) for year in filtered_df['Year'].unique()]
        },
        yaxis={
            'title': 'State minimum wage  ($/hr))'
        },)
    return fig 
#callback for bachelor_degree_or_higher
@app.callback(
    Output('bachelor-degree-or-higher-graph', 'figure'),
    [Input('state-dropdown-hpi', 'value'),
     Input('period-dropdown-hpi', 'value')]
)
def update_bachelor_degree_or_higher(selected_states, selected_periods):
    filtered_df = realestateneconomic[
        (realestateneconomic['State'].isin(selected_states)) &
        (realestateneconomic['Period'].isin(selected_periods))
    ]
    filtered_df['Year'] = pd.DatetimeIndex(filtered_df['Year']).year
    
    # Using px.bar() for a bar chart
    fig = px.bar(
        filtered_df,
        x='Year',
        y='Bachelor Degree or Higher in %',
        color='State',
        barmode='group',  # Group bars for each year side by side for each state
        title='Bachelor Degree or Higher Studies Education Analysis'
    )
    
    # Customizing the layout
    fig.update_layout(
        xaxis={
            'title': 'Year',
            'tickmode': 'array',
            'tickvals': filtered_df['Year'].unique(),
            'ticktext': [str(year) for year in filtered_df['Year'].unique()]
        },
        yaxis={
            'title': 'Bachelor Degree or Higher (%)'
        },
        legend_title="State"
    )
    return fig
#callback for employed-persons-graph
@app.callback(
    Output('employed-persons-graph', 'figure'),
    [Input('state-dropdown-hpi', 'value'),
     Input('period-dropdown-hpi', 'value')]
)
def update_employed_persons_graph(selected_states, selected_periods):
    # Filter the DataFrame based on the selected states and periods
    filtered_df = realestateneconomic[
        (realestateneconomic['State'].isin(selected_states)) &
        (realestateneconomic['Period'].isin(selected_periods))
    ]
    filtered_df['Year'] = pd.DatetimeIndex(filtered_df['Year']).year
    # Create a bar chart
    fig = px.bar(
        filtered_df,
        x='Year',
        y='Employed Persons in number of persons',
        color='State',  # Different color for each state
        barmode='group',  # Group bars for the same year next to each other
        title='Employed Persons by State Over Time'
    )
    fig.update_layout(
        xaxis={
            'title': 'Year',
            'tickmode': 'array',
            'tickvals': filtered_df['Year'].unique(),
            'ticktext': [str(year) for year in filtered_df['Year'].unique()]
        },
        yaxis={
            'title': 'Number of Employed Persons'
        })
    return fig
# Callback for updating the Labor Force Participation Rate graph
@app.callback(
    Output('labor-force-participation-rate-graph', 'figure'),
    [Input('state-dropdown-lfpr', 'value'),
     Input('period-dropdown-lfpr', 'value')]
)
def update_labor_force_participation_rate_graph(selected_states, selected_periods):
    # First, we need to handle the case when no states or periods are selected
    if not selected_states or not selected_periods:
        return go.Figure()  # Return an empty figure

    # Filter the dataframe based on the selected states and periods
    filtered_df = realestateneconomic[
        (realestateneconomic['State'].isin(selected_states)) &
        (realestateneconomic['Period'].isin(selected_periods))
    ]
    filtered_df['Year'] = pd.DatetimeIndex(filtered_df['Year']).year
    # Create the Plotly Express line chart for Labor Force Participation Rate
    fig = px.line(
        filtered_df,
        x='Year',  # assuming 'Year' is the name of your date column
        y='Labor Force Participation Rate in Percent, Annual',  # adjust the column name if different
        color='State',  # to have different lines for each state
        markers=True
    )
    # Customize the layout of the graph
    fig.update_layout(
    xaxis = {
        'title': 'Year',
        'tickmode': 'array',
        'tickvals': filtered_df['Year'].unique(),  # Ensure this array contains all unique years you want to display
        'ticktext': [str(year) for year in filtered_df['Year'].unique()]  # Optional: Format how the tick labels are presented
    },
    yaxis = {
        'title': 'Labor Force Participation Rate (%)'
    }
)
    # Customize the markers and lines
    fig.update_traces(
        mode='lines+markers',
        marker=dict(size=5, opacity=0.5, line=dict(width=0.5, color='DarkSlateGrey')),
        line=dict(width=2)
    )
    # Identify highest and lowest participation rates
    highest_rate = filtered_df.loc[filtered_df['Labor Force Participation Rate in Percent, Annual'].idxmax()]
    lowest_rate = filtered_df.loc[filtered_df['Labor Force Participation Rate in Percent, Annual'].idxmin()]
    # Add annotations for highest and lowest rates
    fig.add_annotation(
        x=highest_rate['Year'],
        y=highest_rate['Labor Force Participation Rate in Percent, Annual'],
        text=f"Highest Rate: {highest_rate['State']} {highest_rate['Year']}: {highest_rate['Labor Force Participation Rate in Percent, Annual']}%",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-40
    )
    fig.add_annotation(
        x=lowest_rate['Year'],
        y=lowest_rate['Labor Force Participation Rate in Percent, Annual'],
        text=f"Lowest Rate: {lowest_rate['State']} {lowest_rate['Year']}: {lowest_rate['Labor Force Participation Rate in Percent, Annual']}%",
        showarrow=True,
        arrowhead=3,
        ax=0,
        ay=40  # May need adjustment based on graph scale
    )
    return fig
# Callback for updating both "Unemployment Rate in Percent" and "Unemployed Persons" graphs
@app.callback(
    Output('unemployment-rate-in-percent-graph', 'figure'),
    [Input('unemployment-state-dropdown', 'value'),
     Input('unemployment-period-dropdown', 'value')]
)
def update_unemployment_rate_in_percent_graph(selected_states, selected_periods):
    # Filter the DataFrame based on the selected states and periods
    filtered_df = realestateneconomic[
        realestateneconomic['State'].isin(selected_states) &
        realestateneconomic['Period'].isin(selected_periods)
    ]
    filtered_df['Year'] = pd.DatetimeIndex(filtered_df['Year']).year
    # Create the graph
    fig = px.line(
        filtered_df,
        x='Year',
        y='Unemployment Rate in Percent',
        color='State'
    )
    fig.update_layout(
        xaxis={
            'title': 'Year',
            'tickmode': 'array',
            'tickvals': filtered_df['Year'].unique(),
            'ticktext': [str(year) for year in filtered_df['Year'].unique()]
        },
        yaxis={
            'title': 'Unemployment Rate (%)'
        }
    )
    return fig
# Callback to update the "Unemployed Persons" graph
@app.callback(
    Output('unemployed-persons-graph', 'figure'),
    [Input('unemployment-state-dropdown', 'value'),
     Input('unemployment-period-dropdown', 'value')]
)
def update_unemployed_persons_graph(selected_states, selected_periods):
    # Filter the DataFrame based on the selected states and periods
    filtered_df = realestateneconomic[
        realestateneconomic['State'].isin(selected_states) &
        realestateneconomic['Period'].isin(selected_periods)
    ]
    filtered_df['Year'] = pd.DatetimeIndex(filtered_df['Year']).year
    fig = px.line(
        filtered_df,
        x='Year',
        y='Unemployed persons',
        color='State'
    )
    fig.update_layout(
        xaxis={
            'title': 'Year',
            'tickmode': 'array',
            'tickvals': filtered_df['Year'].unique(),
            'ticktext': [str(year) for year in filtered_df['Year'].unique()]
        },
        yaxis={
            'title': 'Unemployed Persons'
        }
    )
    return fig
# Callback to update the "Unemployment Duration" graph
@app.callback(
    Output('unemployment-duration-graph', 'figure'),
    [Input('unemployment-state-dropdown', 'value'),
     Input('unemployment-period-dropdown', 'value')]
)
def update_unemployment_duration_graph(selected_states, selected_periods):
    # Filter the DataFrame based on the selected states and periods
    filtered_df = realestateneconomic[
        realestateneconomic['State'].isin(selected_states) &
        realestateneconomic['Period'].isin(selected_periods)
    ]
    filtered_df['Year'] = pd.DatetimeIndex(filtered_df['Year']).year
    fig = px.line(
        filtered_df,
        x='Year',
        y='Persons Unemployed 15 Weeks or Longer, as a Percent of the Civilian Labor Force for Arizona, Percent',
        color='State',
        line_group='Period',
        markers=True,
    )
    
    fig.update_layout(
        xaxis={
            'title': 'Year',
            'tickmode': 'array',
            'tickvals': filtered_df['Year'].unique(),
            'ticktext': [str(year) for year in filtered_df['Year'].unique()]
        },
        yaxis={
            'title': 'Persons Unemployed 15 Weeks or Longer'
        }
    )
    return fig

# Callback for updating the New Houses Sold By Price graph
@app.callback(
    Output('new-houses-sold-usa-graph', 'figure'),
    [Input('period-dropdown-nhs', 'value')]
)
def update_new_houses_sold_graph(selected_periods):
    # Filter the dataframe based on selected periods
    if not selected_periods:
        filtered_df = differential_data
    else:
        filtered_df = differential_data[differential_data['Period'].isin(selected_periods)]

    # Generate the updated graph using the filtered dataframe
    fig = px.bar(
        filtered_df,
        x='Range of House Prices',
        y='New Houses Sold by Sales Price in the United States (Thousands of Units)',
        color='Period',
        barmode='group',
        title='New Houses Sold by Sales Price in the USA',
        category_orders={'Range of House Prices': custom_sort_order}
    )

    # Set y-axis to start from zero and adjust to the range of the data
    fig.update_yaxes(rangemode='tozero')

    # Set specific intervals for y-axis ticks
    fig.update_yaxes(tick0=0, dtick=50)

    # Update layout to improve readability
    fig.update_layout(
        xaxis_title='Range of House Prices',
        yaxis_title='New Houses Sold (Thousands of Units)',
        plot_bgcolor='white',
        xaxis={'categoryorder': 'array', 'categoryarray': custom_sort_order},
        legend_title_text='Period'
    )

    # Optionally, adjust the graph size if needed
    fig.update_layout(
        height=600,  # You can change this as needed
        margin=dict(l=50, r=50, t=50, b=50)  # Adjust the margins to fit the scale if needed
    )
    return fig
#Call back for differential impact graphs



#Part G: Running the Server
if __name__ == "__main__":
    app.run_server(debug=True, port=8058)