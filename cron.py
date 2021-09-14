# file to define functions to be run as periodic cron
import os
from datetime import datetime
import urllib.request as req
from multiprocessing import Pool
#req.urlretrieve
#urlretrieve("http://www.example.com/songs/mp3.mp3", "mp3.mp3")

SQL_DUMP_BASE_PATH = os.getcwd()+'/sql_dumps/'

WIKIMEDIA_LINKS = {
#    "CATEGORY_LINKS_URL": 'https://dumps.wikimedia.org/enwiki/{0}/enwiki-{0}-categorylinks.sql.gz',
#    "PAGE_URL": 'https://dumps.wikimedia.org/enwiki/{0}/enwiki-{0}-page.sql.gz',
    "CATEGORY_URL": 'https://dumps.wikimedia.org/enwiki/{0}/enwiki-{0}-category.sql.gz',
#    "PAGELINKS_URL": 'https://dumps.wikimedia.org/enwiki/{0}/enwiki-{0}-pagelinks.sql.gz'
}

def download_file_by_url(url, retries=10):
    for i in range(retries):
        try:
            req.urlretrieve(url, SQL_DUMP_BASE_PATH+url.split('/')[-1])
            return True
        except Exception as e:
            print(e)
    return False

thread_pool = Pool(os.cpu_count())

def update_wiki_db():
    """
    Function to update the wikidb every first of month and the views associated with it.
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

    return are_files_downloaded



if __name__ == '__main__':
    print(update_wiki_db())
