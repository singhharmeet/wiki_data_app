# WIKI Media Data Query Cron And API
This is an example repo to run cron and sql queries on wiki data dump.

# Assumptions and Constraints->
* Only tables required were ``` page, category, pagelinks, categorylinks ```. All developer decisions to refresh and query data was made based on these 4 tables
* category API was developed as sync api, although based on the uncertainity of the response time, it should be an Async api
* Current Dockerfile only deploys the API on localhost. This shoud be changed to uwsgi for webserver.
* Redis and SQLDB are assumed to be already setup. If setup is required, we can use docker compose to either set tem in isolated pods or use AWS ElastiCache and AWS RDS service
* Current setup is done using local cron to save time. this can be easily triggered using AWS event bridge and s3 stored as storage for sql dump files to use less storage space of server.
* the whole setup is currently running on a single server of 2 core and 2 GB RAM(to save costs), performance may vary with instance type.

# Application features->
## V1(Current Code):
* 2 APIs->
  * **/outdated-pages/category/<category\>** to show page details for most outdated page of category
  ```
  Sample Input-> curl http://localhost:5000/outdated-pages/category/Articles_with_short_description
  Sample Output-> {"data":{"diff":75929489,"hpid":240931,"hpt":".hack_(video_game_series)","lpid":33322483,"lpt":".hack//The_Movie"}}
  ```
  * **/execute-sql** to show results of SQL Query suplied by user
  ```
  Sample Input-> curl --request POST --header "Content-Type: application/json" --data '{"query":"select page_id, page_title, page_links_updated, page_touched from page where page_title = '\''AfghanistanPeople'\'' limit 5;"}' http://localhost:5000/execute-sql
  Sample Output-> {"result":[{"page_id":15,"page_links_updated":"20210126121901","page_title":"AfghanistanPeople","page_touched":"20210527204212"}]}
  ```
* 1 Cron job in **cron.py**, containing code to update the datbase and subsequently the cache
 * cron is executed on crontab as-> 0 5 2 * * python3 /home/ubuntu/wiki_data_app/cron.py > log.txt

## V2(Possible Improvements)->
* shifting server cron to airflow based cron setup for easier monitoring and maintainabity
* converting the sql execution API to async and showing job results via callbacks containing s3 based json results.
* creating kubernetes cluster to host the application and components for easier scalablity and maintainence.
* Using managed DBs for higher reliablity
