import csv, re, json, time, sqlite3, requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
# sort subreddit feed by new, each item is of tag shreddit-post (data-ks-item (child))
# collect the attributes: content-href, comment-count, created-timestamp, id, post-title, score, author, feedindex
 
 
def search_element(driver):
    #column for
    path = 'lastelement.csv'
    
    with open(path, 'r' ) as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
        #print(rows)
        last_row = rows[-1]
        #print("last row: ", last_row)
        time_of_last_post = last_row[3]
        id_of_las_post = last_row[0]
        # Convert string to datetime object
    goal_timestamp = datetime.strptime(time_of_last_post, '%Y-%m-%dT%H:%M:%S.%f%z')
    after_than_timestamp = True
    while after_than_timestamp:
        post = driver.find_elements(By.TAG_NAME, "shreddit-post")
        post = post[-1] 
        current_post_timestamp = post.get_attribute('created-timestamp')
        current_post_timestamp = datetime.strptime(current_post_timestamp, '%Y-%m-%dT%H:%M:%S.%f%z')
        if current_post_timestamp < goal_timestamp:
            driver.execute_script("arguments[0].scrollIntoView();", post)
            after_than_timestamp = False
            # get feedindex
            feed_index = post.get_attribute('feedindex')
            print("found!")
            time.sleep(5)
            return int(feed_index) +1
        else:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
"""Add method to search continue where we left of"""
def main():
    counter_of_posts = 0
    subreddit_link_top_week = 'https://www.reddit.com/r/AmItheAsshole/top/?t=week'
    subreddit_link = 'https://www.reddit.com/r/AmItheAsshole/new/'
    # subreddit_link = subreddit_link_top_week
    posts_db_name = 'SubredditData.db'
    posts_table_name = 'AmItheAsshole'
    
    unique_ids = [0,]
    post_height = 0
    number_of_posts_I_want = 12000
    driver = start_selenium_session(subreddit_link)
    wait = WebDriverWait(driver, timeout=5)
    time.sleep(15)
    #feed_index = search_element(driver)
    feed_index =3
    new_post =[]
    try:
        while len(unique_ids) < number_of_posts_I_want:
        
            comments_data = []
            comments_tables_names = []
        # for loop inside a while loop, the for loop is for batches
        
            ten_posts = []
            # returns the content to be added to sqlite, comment tables have already been created for each post
            for _ in range(10):
                temp_unique_ids = unique_ids[:-10] if len(unique_ids) > 10 else unique_ids
                new_post, feed_index, new_unique_id, post_height, comments, comment_table_name = get_1_post(driver, temp_unique_ids, feed_index, post_height, wait)
                unique_ids.append(new_unique_id)
                
                # print("newpost: ",new_post)
                if new_post:
                    counter_of_posts += 1
                    ten_posts.append(new_post)
                    comments_data.append(comments)
                    comments_tables_names.append(comment_table_name)
                    
            #print("len 10 posts: ",len(ten_posts))
            # add 10 posts to sql table
            #print("CONTENT passed to add to sqlite: ", (ten_posts, posts_db_name, posts_table_name))
            #print("comments table name: ",comments_tables_names )
            add_posts_to_sqlite(ten_posts, posts_db_name, posts_table_name)
            try:
                headers = ['post_id','comment_id','ups', 'author', 'content']
                #print("len comments data: ",len(comments_data))
                for comments_per_post,table_name in zip(comments_data, comments_tables_names):
                    #print("len comments per post: ",len(comments_per_post))
                    top_comments_to_sql(comments_per_post, table_name, posts_table_name, posts_db_name)
                    path = 'data_comments.csv'
                #print("content: ", comments_data)
                """
                    with open(path, 'a', newline='', encoding='utf-8') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(headers)
                        writer.writerows(comments_per_post)"""
            except Exception as e:
                print("exception at comment retrieval")

    except Exception as e:
        print("Error in main: ", e)

    finally:
        time.sleep(7)
        print("Number of posts by counter: ", counter_of_posts)
        print("Number of posts given by feedindex: ", feed_index)
        """with open('data.csv', 'w') as csvfile:
                writer = csv.writer(csvfile)
                
                writer.writerows(ten_posts)"""
        with open('lastelement.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            #writer.writerow("/n")
            writer.writerow(new_post)
        with open('n_posts.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
             
            writer.writerow(["Number of posts by counter: ", counter_of_posts])
            writer.writerow(["Number of posts given by feedindex: ", feed_index])

            

 
def add_posts_to_sqlite(ten_posts, posts_db_name, posts_table_name):
    cursor, connection = make_sql_connection(posts_db_name)
    try:
        cursor.executemany(f'INSERT INTO {posts_table_name} (post_id, ups, comment_count, created_timestamp, author, post_title, url, text_content) VALUES (?,?,?,?,?,?,?,?)', ten_posts)
    except sqlite3.IntegrityError:
        for post in ten_posts:
            try:
                cursor.execute(f'INSERT INTO {posts_table_name} (post_id, ups, comment_count, created_timestamp, author, post_title, url, text_content) VALUES (?,?,?,?,?,?,?,?)', post)
            except sqlite3.IntegrityError:
                 
                cursor.execute(f"UPDATE {posts_table_name} SET ups = ?, comment_count= ? WHERE post_id=?",(post[1], post[2], post[0]))
    finally:
        connection.commit()
        connection.close()

def start_selenium_session(subreddit_link , browser=0):
    if browser < 1:
        options = webdriver.SafariOptions()
        driver = webdriver.Safari(options=options)
    else:
        driver = webdriver.Chrome()
    #options.page_load_strategy = 'normal'
    # pecifies the time to wait for the implicit element location strategy when locating elements. 
    #options.timeouts = { 'implicit': 1000 }
    
    driver.get(subreddit_link)
    return driver

def make_sql_connection(table_name):
    try:
        connection = sqlite3.connect(table_name)
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON')
        return cursor, connection
    except Exception as e:
        print("Error in making sql connection: ",e)

def get_1_post(driver, unique_ids, feed_index, post_height, wait):
    # change to get a single post encapsulate in try except block, to scroll if not found 
    # and if not found again go to next post
    post = None
    post_height = post_height if post_height > 0 else 300
    new_post = []    
    try:
        print("feedindex: ", feed_index)
        post = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f"shreddit-post[feedindex='{feed_index}']")))     
        print("found? ", post)
        if not post:
            post = driver.find_element(By.CSS_SELECTOR, f"shreddit-post[feedindex='{feed_index}']")
            print("npt post 1")
    except (NoSuchElementException, TimeoutException):
        """dont immediatly add feed_index, first try to scroll
        and if not found feed index, if not found again then change feed number to the closest avalaible"""
        print("(NoSuchElementException, TimeoutException) at get 1 post")
        try:
            # try scrolling 
            counter = 0
            while counter < 5:
                if not post:
                    driver.execute_script(f"window.scrollBy(0, {post_height});")
                    counter += 1
                    post = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f"shreddit-post[feedindex='{feed_index}']")))     
                else:
                          
                    break
        except Exception as e:
            print("Exception Inside 'get_1_Post'  No such element : ", e)
        
        # change feed index to closest found
        if not post:
            element_wait = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f"shreddit-post")))
            print("Still not post")
            posts = driver.find_elements(By.CSS_SELECTOR, "shreddit-post")
            # correct to get accurate feedindex, not first, not last
            for post_i in posts:
                if int(post_i.get_attribute("feedindex")) > feed_index:
                     
                    driver.execute_script("arguments[0].scrollIntoView(true);", post_i)
                    post = post_i
                    break
            
            feed_index = int(post.get_attribute("feedindex"))     
         
        feed_index += 1

        post = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f"shreddit-post[feedindex='{feed_index}']")))
         
    finally:
        if post:
            try:
                try:
                    post_height = post.size['height']
                except Exception as e:
                    print("Exception at post height")
                post_title = post.get_attribute("post-title")
                post_id = post.get_attribute("id")
                    # use function to get inner text

                text_content = get_post_text_content(post_element=post, post_id=post_id)
                url = post.get_attribute("content-href")
                comment_count = post.get_attribute("comment-count")
                created_timestamp = post.get_attribute("created-timestamp")
                ups = post.get_attribute("score")
                author = post.get_attribute("author")
                #print("post title: ", post_title)
                post_data = [ post_id, ups, comment_count, created_timestamp, author, post_title, url, text_content]
                if post_id not in unique_ids:
                    unique_ids.append(post_id)
                    new_post = post_data
                    comments = extract_top_comments(url)
                    comment_table_name = f'{post_id}__comments'
                # creates table, nd adds comments to sqlite
                    
                        #print("comments: ", comments)

                    driver.execute_script(f"window.scrollBy(0, {post_height});")
                    feed_index += 1
                    post_id = ''
                    return new_post, feed_index, post_id, post_height, comments, comment_table_name
            except Exception as e:
                print("exception in get one post, getting atributes+comments ")
                print("Error : ", e)
                new_post = []
                comments=[]
                comment_table_name = ''
                post_id = ''
                feed_index +=1
                return new_post, feed_index, post_id, post_height, comments, comment_table_name

def get_post_text_content(post_element, post_id):
    post_id_name = post_id + '-post-rtjson-content'
    text_element = post_element.find_element(By.ID, post_id_name) 
    text_content = text_element.text
    text_content = re.sub(r'\s+', ' ', text_content)
    text_content = text_content.replace('\n', '').encode('utf-8')
    return text_content

def extract_top_comments(url):
    try:
        driver_comments = start_selenium_session(url, browser=1)
    except Exception as e:
        print("Failed to start second selenium driver: ", e)
    element = WebDriverWait(driver_comments, 10).until(
    EC.presence_of_all_elements_located((By.TAG_NAME, 'shreddit-comment'))
    )
    soup = BeautifulSoup(driver_comments.page_source, 'html.parser')
    driver_comments.quit()
    comments = soup.find_all('shreddit-comment')
    comments_data = []
    for comment in comments:
        post_content = []
        author =comment['author']
        comment_id = comment['thingid']
        try:
            score = comment['score']
        except Exception as e:
            print("error in score")
            score = 0
        post_id = comment['postid']
        content = comment.find('div', {'id': '-post-rtjson-content'}).text
        content = re.sub(r'\s+', ' ', content)
        content = content.replace('\n', '').encode('utf-8')
        post_content = [
            post_id,
            comment_id,
            score,
            author,
            content
        ]
        comments_data.append(post_content)
    # print("soup: ", soup)


    
    
    
    
    return comments_data
     
    
def create_comment_table(comment_table_name, post_table_name, posts_db_name):
    cursor_comments, connection_comments = make_sql_connection(posts_db_name)
    cursor_comments.execute(
        f'''
        CREATE TABLE IF NOT EXISTS {comment_table_name}  (
            post_id TEXT,
            comment_id INT,
            content TEXT,
            ups INTEGER,
            author TEXT,
            FOREIGN KEY (post_id) REFERENCES {post_table_name}(post_id)

        )
        '''
    )
    connection_comments.commit()
    return cursor_comments, connection_comments

def top_comments_to_sql(comments_data, comment_table_name, post_table_name, posts_db_name):
        try:
            cursor_comments, connection_comments = create_comment_table(comment_table_name, post_table_name, posts_db_name)
        except Exception as e:
            print("exception at sqlite for comments")
        try:
            cursor_comments.executemany(f'INSERT INTO {comment_table_name} (post_id, comment_id, ups, author, content) VALUES (?,?,?,?,?)', comments_data)
        except Exception as e:
            print("Exception at executemany comments", e)
        connection_comments.commit()
        connection_comments.close( )
if __name__ == "__main__":
    
    main()


  