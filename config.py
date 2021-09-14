# common file to define configuration details
import os


DB_SETTINGS = {
        "host": os.getenv("SQL_HOST","localhost"),
        "user": os.getenv("SQL_USER","harmeet"),
        "password": os.getenv("SQL_PASS","welcome@123"),
        "database": os.getenv("SQL_DB_NAME","wiki_db")
    }

CACHE_SETTINGS = {
        "host": os.getenv("REDIS_HOST","localhost"),
        "port": os.getenv("REDIS_PORT",6379),
        "password": os.getenv("REDIS_PASS",""),
        "db": os.getenv("REDIS_DB_NAME",0)
}

CATEGORYWISE_MAX_DIFF_QUERY = '''
select cat_title, head_page_id, page.page_touched as head_page_id_change, page.page_title as head_page_title, link_page_id_change, link_page_title,  link_page_id from (select pl_from as head_page_id , pl_title, page_id as link_page_id, page_title as link_page_title , page_touched as link_page_id_change, cat_title from (select pl_title, pl_from, cat_title from pagelinks inner join (select cl_from, cat_title from categorylinks inner join (select cat_title, cat_pages from category order by cat_pages desc limit 10) t1 on cl_to=cat_title) t2 on cl_from=pl_from) t4 inner join page on pl_title= page_title) t5 inner join page on t5.head_page_id = page.page_id;
'''
