# PhonePe Pulse Project

PhonePe Pulse is a data visualization project that showcases digital payment trends in India using an interactive map and insightful charts. The project gathers data from PhonePe's extensive transaction history and presents it in an easily digestible format.

## Project Overview

The PhonePe Pulse website displays over 2000+ Crore transactions by consumers on an interactive map of India. With a market share of over 45%, PhonePe's data provides valuable insights into the country's digital payment habits. The project's insights are derived from PhonePe's transaction data, combined with merchant and customer interviews.

## Features

- Interactive map of India displaying transaction data
- Insights derived from PhonePe's extensive transaction history
- Charts and graphs for visual representation of trends
- User-friendly interface using Streamlit for data exploration

## Libraries/Modules Used

- `pandas`: Used to create DataFrames with the scraped data.
- `mysql.connector`: Used for storing and retrieving data from a MySQL database.
- `streamlit`: Used to create a user-friendly graphical interface.
- `plotly`: Used for data visualization and creating interactive charts and maps.
- `json`: Used to load JSON files.
- `git.repo.base`: Used for cloning the PhonePe Pulse GitHub repository.

## Workflow

1. **Data Extraction**: Cloning the PhonePe Pulse GitHub repository to fetch data and store it in JSON format.
2. **Data Transformation**: Converting the JSON files into readable DataFrames, transforming and cleaning the data.
3. **Database Insertion**: Storing the transformed data into a MySQL database.
4. **Dashboard Creation**: Using Plotly and Streamlit to create interactive charts, maps, and a user-friendly dashboard.
5. **Data Retrieval**: Optionally, fetching data from the MySQL database into Pandas DataFrames.

## How to Use

1. Clone this repository.
2. Install the required libraries using `pip install -r requirements.txt`.
3. Set up your MySQL database credentials in the appropriate place in your script.
4. Run the script to extract, transform, store, and visualize the data.
5. Open the Streamlit app in your web browser to explore the interactive dashboard.

## Screenshots

Insert relevant screenshots of your dashboard and visualizations here.

## Acknowledgements

- [PhonePe Pulse GitHub Repository](https://github.com/phonepe/pulse)
- [Python `pandas` documentation](https://pandas.pydata.org/docs/)
- [Python `mysql-connector` documentation](https://dev.mysql.com/doc/connector-python/en/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Documentation](https://plotly.com/python/)
- [GitHub API for Python](https://github.com/PyGithub/PyGithub)

Feel free to contribute, report issues, or fork this repository.
