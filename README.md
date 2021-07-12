# AnalyticsPing
:bar_chart: Sends ping to website and collects this information in local db

Modules:
* sqlite3 - to create db and operate with data
* subprocess - pings url
* time - to run script again every 3 secs
* re - takes important info from ping response 

![ping_st](https://github.com/teora13/AnalyticsPing/blob/main/ping_st.jpg)

Script create db (if it's no exists) with tables and collects important information there. It keeps details about lost data, such as: date, time, sent, lost, received packages. Also it keeps info in case of lost internet connection.  

![tables](https://github.com/teora13/AnalyticsPing/blob/main/tables.jpg)

