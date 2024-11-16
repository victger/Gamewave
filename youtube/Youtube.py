import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_youtube(driver, data_twitch):

    visible = EC.visibility_of_element_located
    data_youtube=pd.DataFrame()

    for k in range(0,len(data_twitch)):

        game= []
        tags= []
        video_title= []
        link= []
        channel= []
        views= []
        date= []

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

            video_title.append(grid.find_element(By.XPATH, ".//a[contains(@id, 'video-title')]").text)
            link.append(grid.find_element(By.XPATH, ".//a[contains(@id, 'video-title')]").get_attribute("href"))
            channel.append(grid.find_element(By.XPATH, ".//ytd-channel-name").text)
            metadata= grid.find_elements(By.XPATH, ".//div[contains(@id, 'metadata-line')]")

            views.append(metadata[0].text.split('\n')[0])
            date.append(metadata[0].text.split('\n')[1])

            game.append(data_twitch["Game"][k])
            tags.append(data_twitch["Tags"][k])

        temp_df = pd.DataFrame({
            'Game': game,
            'Video title': video_title,
            'Channel': channel,
            'Views': views,
            'Date': date,
            'Tags': tags,
            'Link': link
        })

        data_youtube= pd.concat([data_youtube,temp_df], axis=0)

    return data_youtube