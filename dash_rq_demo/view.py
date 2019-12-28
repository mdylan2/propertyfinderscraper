import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash_table import DataTable
import dash_html_components as html

navbar = dbc.NavbarSimple(
        brand="Property Finder Scraper",
        brand_href="#",
        sticky='top',    
        dark = True,
        color = 'primary',
        fluid = True
    )

body = dbc.Container(
    [

        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id = "transaction_type",
                            options = [
                                {'label':'Buy', 'value': 1},
                                {'label': 'Rent', 'value': 2},
                                {'label': 'Commercial Rent', 'value': 4},
                                {'label':'Commercial Buy', 'value': 3}
                            ],
                            value = 1,
                            multi = False,
                            placeholder = "Transaction Type"
                        ),
                    ], 
                ),
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id = "housing_type",
                            options = [
                                {'label': "Apartment",'value': 1}, 
                                {'label': "Villa",'value': 35}
                            ],
                            value = 1,
                            placeholder = "Housing Type"
                        ),
                    ], 
                ),
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id = "rental_period",
                            options = [
                                {"label":"Daily", "value":'d'},
                                {"label":"Weekly", "value":'w'},
                                {"label":"Monthly", "value":'m'},
                                {"label":"Yearly", "value":"y"}
                            ],
                            value = "y",
                            placeholder = "Rental Period"
                        ),
                    ],
                ),                
                dbc.Col(
                    [
                        dbc.Button("Scrape the Data!", id = "letsgo", color = "primary")
                    ], 
                )
            ], className = "mt-3"
        ),

        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3("Please Select Stuff From Above", style = {'margin': '0px'})
                    ], id = "title", width = 8
                ),

            ], className = "mt-3", justify = "between",
        ),
        
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Collapse(
                            dbc.Progress(id="progress", className="mb-3", style={"height": "25px"}), id="collapse"
                        ),
                    ]
                )
            ], className = "mt-3"
        ),

        dbc.Row(
            [
                dbc.Col(
                    [
                        DataTable(
                            id='table',
                            columns = [
                                {'name': 'title_list', 'id': 'title_list', 'deletable': True, 'renamable': True},
                                {'name': 'location_list', 'id': 'location_list', 'deletable': True, 'renamable': True},
                                {'name': 'type_list', 'id': 'type_list', 'deletable': True, 'renamable': True},
                                {'name': 'bedroom_list', 'id': 'bedroom_list', 'deletable': True, 'renamable': True},
                                {'name': 'bathroom_list', 'id': 'bathroom_list', 'deletable': True, 'renamable': True},
                                {'name': 'area_list', 'id': 'area_list', 'deletable': True, 'renamable': True},
                            ],
                            data=[],
                            page_size=10,
                            export_format='xlsx',
                            export_headers='display',
                        ),
                    ]
                )
            ], className = "mt-2"
        )
        
    ], fluid = True
)