# file to define functions to be run as periodic cron
import os
import gzip
import shutil
from datetime import datetime
import urllib.request as req
from multiprocessing import Pool
from db.sql import MySQLDBConn
from config import DB_SETTINGS, CATEGORYWISE_MAX_DIFF_QUERY

SQL_DUMP_BASE_PATH = os.getcwd()+'/sql_dumps/'

WIKIMEDIA_LINKS = {
#    "CATEGORY_LINKS_URL": 'https://dumps.wikimedia.org/enwiki/{0}/enwiki-{0}-categorylinks.sql.gz',
#    "PAGE_URL": 'https://dumps.wikimedia.org/enwiki/{0}/enwiki-{0}-page.sql.gz',
    "CATEGORY_URL": 'https://dumps.wikimedia.org/enwiki/{0}/enwiki-{0}-category.sql.gz',
#    "PAGELINKS_URL": 'https://dumps.wikimedia.org/enwiki/{0}/enwiki-{0}-pagelinks.sql.gz'
}

def unzip_gz_to_sql(path):
    """
    function to unzip data. returns sql file ready to import

    """
    print("unzipping file: "+path)
    with gzip.open(path, 'rb') as f_in:
        with open(path[:-3], 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
            return path[:-3]

def download_file_by_url(url, retries=10):
    """
    Download gzip file to local system. takes 10 retries by default.
    """
    for i in range(retries):
        try:
            print("downloading file: "+url)
            download_path = SQL_DUMP_BASE_PATH+url.split('/')[-1]
            req.urlretrieve(url, download_path)
            return download_path
        except Exception as e:
            print(e)
    return False

def update_cache_with_results():
    """
    updates cache with category wise time difference between head and linked page.
    """
    results = MySQLDBConn.execute_query(CATEGORYWISE_MAX_DIFF_QUERY)
    results = convert_json_serialisable(results)
    dict_results = {}
    for each in results:
        if dict_results.get(each["cat_title"], None) is None:
            dict_results[each["cat_title"]] = {"diff":int(each["link_page_id_change"])-int(each["head_page_id_change"]),"hpt":each["head_page_title"],"hpid":each["head_page_id"],"lpt":each.get("link_page_title"),"lpid":each.get("link_page_id")}
        else:
            diff = int(each["link_page_id_change"])-int(each["head_page_id_change"])
            if diff> dict_results[each["cat_title"]]["diff"]:
                dict_results[each["cat_title"]] = {"diff":int(each["link_page_id_change"])-int(each["head_page_id_change"]),"hpt":each["head_page_title"],"hpid":each["head_page_id"],"lpt":each.get("link_page_title"),"lpid":each.get("link_page_id")}
    return dict_results



thread_pool = Pool(os.cpu_count())

def update_wiki_db():
    """
    Function to update the wikidb every first of month.
    """
    curr_month, curr_year = datetime.now().month, datetime.now().year
    download_date = str(curr_year)+str(format(curr_month, '02d'))+"01"
    download_links = []
    for link in WIKIMEDIA_LINKS.values():
        download_links.append(link.format(download_date))
    if not os.path.isdir(SQL_DUMP_BASE_PATH):
        try:
            os.mkdir(SQL_DUMP_BASE_PATH)
        except Exception as e:
            print("Unable to create folder: "+SQL_DUMP_BASE_PATH+" : "+str(e))
    are_files_downloaded = thread_pool.map(download_file_by_url, download_links)
    sql_file_paths = []
    if are_files_downloaded and False not in are_files_downloaded:
        sql_file_paths = thread_pool.map(unzip_gz_to_sql, are_files_downloaded)
    if sql_file_paths and False not in sql_file_paths:
        sql_file_paths = ["mysql -u {} -p{} {} < {}".format(DB_SETTINGS['user'],DB_SETTINGS['password'],DB_SETTINGS['database'],each) for each in sql_file_paths]
        input(sql_file_paths)
        is_update_complete = thread_pool.map(MySQLDBConn.execute_sql_cmd,sql_file_paths)

    return sql_file_paths



if __name__ == '__main__':
    print("Updating db with newest data revision")
    #print(update_wiki_db())
    print("Updating cache with categorywise diff query")

