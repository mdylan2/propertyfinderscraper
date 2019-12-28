import datetime
import uuid
from collections import defaultdict
import pandas as pd

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from rq.exceptions import NoSuchJobError
from rq.job import Job

from .core import app, conn, db, queue
from .models import Result
from .tasks import slow_loop
from .view import navbar, body
from .model import scraper

app.layout = html.Div(
    [
        dcc.Store(id="store"),
        dcc.Interval(id="interval", interval=500),
        navbar,
        body
    ]
)


@app.callback(
    Output("store", "data"),
    [Input("letsgo", "n_clicks")],
    [State("transaction_type","value"),
    State("housing_type","value"),
    State("rental_period","value")]
)
def submit(n_clicks, transaction_type, housing_type, rental_period):
    if n_clicks:
        id_ = uuid.uuid4()

        scraper_init = scraper(transaction_type, housing_type, rental_period)

        # queue the task
        queue.enqueue(slow_loop, scraper_init, id_, job_id=str(id_))

        # record queuing in the database
        result = Result(id=id_, queued=datetime.datetime.now())
        db.session.add(result)
        db.session.commit()

        # log process id in dcc.Store
        return {"id": str(id_)}
    return {}


@app.callback(
    [
        Output("table", "data"),
        Output("progress", "value"),
        Output("progress", "children"),
        Output("collapse", "is_open"),
    ],
    [Input("interval", "n_intervals")],
    [State("store", "data")],
)
def retrieve_output(n, data):
    if n and data:
        try:
            job = Job.fetch(data["id"], connection=conn)
            if job.get_status() == "finished":
                return pd.read_json(job.result, orient='index').to_dict('records'), 100, "100%", False
            progress = job.meta.get("progress", 0)
            total = job.meta.get("total",1)
            return [], progress*100/total,"%d%%" %(progress*100/total), True
        except NoSuchJobError:
            # if job no longer exists, retrive result from database
            result = Result.query.filter_by(id=data["id"]).first()
            if result and result.result:
                return [], 100,"100%", False
    return [], None,None, False
