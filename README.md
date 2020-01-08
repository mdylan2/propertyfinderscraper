# Property Finder Scraper
## Description
This repository contains the Python code for a web scraper that takes in user input parameters and returns scraped data from (www.propertyfinder.ae)[www.propertyfinder.ae] as a downloadeable excel file.

The fully functional website can be found at [https://propertyfinderscraper.herokuapp.com/](https://propertyfinderscraper.herokuapp.com/).

## Packages Used
### Packages:
- Plotly Dash
- Pandas
- Redis Queue
- BeautifulSoup
- Requests

### Databases:
- Redis
- PostgreSQL

## Files
Here's a list of important files/folders in the directory:
- `app.py`: Contains the code to launch the application
- `view.py`: Contains the HTML layouts used in the Dash application
- `assets`: Contains the CSS, Javascript and other images used in the website
- `Presentation (CannaRec)`: Contains a presentation I prepared 

## Running Locally or Deploying
The app in this repository is fully deployable on Heroku or can be run locally as well. The app was adapted from (tcbegley's)[https://github.com/tcbegley] repo (dash-rq-demo)[https://github.com/tcbegley/dash-rq-demo]. Please visit his repo for more details on deployment.

All you will need is a postgres and redis server. 

## Interface


## Acknowledgements
I would like to thank [tcbegley](https://github.com/tcbegley) for his amazing work on async updates in Dash!
