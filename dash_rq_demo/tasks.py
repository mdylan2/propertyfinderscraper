import datetime
import time
from collections import defaultdict
from pandas import DataFrame

from rq import get_current_job

from .core import db
from .models import Result
from .model import scraper

def slow_loop(scraper, id_):
    """
    Converts a string to upper case character by character. Will update the
    database to log start and completion times.

    Parameters
    ----------
    s : str
        String to convert to upper case
    id_ : uuid.UUID
        The job id for the submitted task.
    """
    # Update the database to confirm that task has started processing
    result = Result.query.filter_by(id=id_).first()
    result.started = datetime.datetime.now()
    db.session.add(result)
    db.session.commit()
    
    # Initializing scraper and empty dataframe to store results
    scraper.count_all_pages()
    dataframe = defaultdict(list)

    # Store completion percentage in redis under the process id
    job = get_current_job()
    job.meta["progress"] = 0
    job.save_meta()

    job.meta["total"] = len(scraper.all_pages)
    job.save_meta()

    for page_number in scraper.all_pages:
        title_list, location_list, price_list, type_list, bedroom_list, bathroom_list, area_list = scraper.scrape_page(page_number = page_number)
        dataframe['title_list'].extend(title_list)
        dataframe['location_list'].extend(location_list)
        dataframe['price_list'].extend(price_list)
        dataframe['type_list'].extend(type_list)
        dataframe['bedroom_list'].extend(bedroom_list)
        dataframe['bathroom_list'].extend(bathroom_list)
        dataframe['area_list'].extend(area_list)
        
        # update completion percentage so it's available from front-end
        job.meta["progress"] = page_number
        job.save_meta()

    dataframe = DataFrame(dataframe)
    dataframe['area_list'] = dataframe['area_list'].str.extract("([0-9,]+)", expand = False)

    res = dataframe.to_json(orient='index')

    # update the database to confirm that task has completed processing
    result.completed = datetime.datetime.now()
    result.result = res
    db.session.add(result)
    db.session.commit()

    return res