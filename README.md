# Text search web application


Text searching web app created with django framework and fuzzysearch library. There are 5 urls in that app:
 - Main page: contain window for searched text, and other urls described below. 
 - help: contain necessary information about web app urls.
 - refresh_database: url for refreshing database, documents for database are taking from data folder.
 - search: url for displaying searching process results.
 - validate: url for displaying different metrics of text searching system, test data located into test folder. 

## Usage
To run the app execute following commands:
```bash
pip install -r requirements.txt
python manage.py runserver
```

