import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_youtube(driver, data_twitch):

    visible = EC.visibility_of_element_located
    data_youtube=pd.DataFrame()

    for k in range(0,len(data_twitch)):

        games= []
        tags= []
        video_titles= []
        links= []
        channels= []
        views= []
        dates= []

        driver.get('https://www.youtube.com/results?search_query={}'.format(str(data_twitch["Game"][k])))
        
        time.sleep(1)

        # Cookies handling

        if k==0:
            button = driver.find_element(By.XPATH,"//*[@id='content']/div[2]/div[6]/div[1]/ytd-button-renderer[1]/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]")
            button.click()

        # Click on Youtube card

        try:
            driver.find_element(By.XPATH, "//*[@id='watch-card-subtitle']").click()
        except:
            continue

        # Click on "Recent"

        recent_tab_position= 4
        recent_tab = WebDriverWait(driver, 5).until(visible((By.XPATH, f"(//tp-yt-paper-tab[@role='tab'])[{recent_tab_position}]")))
        recent_tab.click()

        time.sleep(2)

        # Scrolling to get 100 videos

        height = driver.execute_script('''var body = document.body,
                                            html = document.documentElement;
                                            var height = Math.max( body.scrollHeight, body.offsetHeight, 
                                            html.clientHeight, html.scrollHeight, html.offsetHeight );
                                            return height;''')

        driver.execute_script("window.scrollTo(0, "+str(height)+");")

        time.sleep(2)

        # Get Youtube videos data
        
        total_grid= driver.find_element(By.XPATH, "//div[contains(@id,'items') and contains(@class, 'style-scope ytd-grid-renderer')]")
        grids= total_grid.find_elements(By.XPATH, ".//ytd-grid-video-renderer")

        for grid in grids:

            video_title= grid.find_element(By.XPATH, ".//a[contains(@id, 'video-title')]").text
            link= grid.find_element(By.XPATH, ".//a[contains(@id, 'video-title')]").get_attribute("href")
            channel= grid.find_element(By.XPATH, ".//ytd-channel-name").text
            metadata= grid.find_elements(By.XPATH, ".//div[contains(@id, 'metadata-line')]")
            metadata_split= metadata[0].text.split('\n')

            video_titles.append(video_title)
            links.append(link)
            channels.append(channel)

            if len(metadata[0].text.split('\n'))==2:
                view= metadata_split[0]
                date= metadata_split[1]
                views.append(view)
                dates.append(date)

            else:
                print(link+' video passed as it seems to be a live stream.')
                pass

            games.append(data_twitch["Game"][k])
            tags.append(data_twitch["Tags"][k])

        temp_df = pd.DataFrame({
            'Game': games,
            'Video title': video_titles,
            'Channel': channels,
            'Views': views,
            'Date': dates,
            'Tags': tags,
            'Link': links
        })

        data_youtube= pd.concat([data_youtube,temp_df], axis=0)

        print('Gathered data from '+data_twitch["Game"][k])

    return data_youtube