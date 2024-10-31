import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

def scrape_youtube(driver, data_twitch):

    visible = EC.visibility_of_element_located
    data_youtube=pd.DataFrame()

    # Cette boucle permet de parcourir tous les jeux contenus dans notre dataframe Twitch sur Youtube. Il faut changer le paramètre len(data_twitch) pour echercher moins de jeux

    for k in range(0,len(data_twitch)):

        # A chaque itération, on initialise nos tableaux pour concaténer nos informations dans la dataframe sans doublons

        game= []
        tags= []
        video_title= []
        link= []
        channel= []
        views= []
        date= []

        # Navigation vers le ième jeu de notre datafrme Twitch

        driver.get('https://www.youtube.com/results?search_query={}'.format(str(data_twitch["Game"][k])))
        
        time.sleep(1)

        # Acceptation des cookies Youtube à la première itération

        if k==0:
            button = driver.find_element(By.XPATH,"//*[@id='content']/div[2]/div[6]/div[1]/ytd-button-renderer[1]/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]")
            button.click()

        # On clique sur la carte de jeu Youtube si elle est disponible, sinon on passe à la prochaine itération.

        try:
            driver.find_element(By.XPATH, "//*[@id='watch-card-subtitle']").click()
        except:
            continue

        # On clique sur l'onglet "Récentes" dans la carte du jeu

        recent_tab_position= 4
        recent_tab = WebDriverWait(driver, 5).until(visible((By.XPATH, f"(//tp-yt-paper-tab[@role='tab'])[{recent_tab_position}]")))
        recent_tab.click()

        time.sleep(2)

        # On scrolle suffisamment dans la page pour scrapper 100 vidéos de la carte de jeu dans l'onglet "Récentes"

        height = driver.execute_script('''var body = document.body,
                                            html = document.documentElement;
                                            var height = Math.max( body.scrollHeight, body.offsetHeight, 
                                            html.clientHeight, html.scrollHeight, html.offsetHeight );
                                            return height;''')

        driver.execute_script("window.scrollTo(0, "+str(height)+");")

        time.sleep(2)

        # On récupère le titre, la chaîne, le nombre de vues, la date, le jeu ainsi que le lien de la vidéo concernée

        
        total_grid= driver.find_element(By.XPATH, "//div[contains(@id,'items') and contains(@class, 'style-scope ytd-grid-renderer')]")

        grids= total_grid.find_elements(By.XPATH, ".//ytd-grid-video-renderer")

        for grid in grids:

            video_title.append(grid.find_element(By.XPATH, ".//a[contains(@id, 'video-title')]").text)
            link.append(grid.find_element(By.XPATH, ".//a[contains(@id, 'video-title')]").get_attribute("href"))
            channel.append(grid.find_element(By.XPATH, ".//ytd-channel-name").text)
            metadata= grid.find_elements(By.XPATH, ".//div[contains(@id, 'metadata-line')]")

            views.append(metadata[0].text.split('\n')[0])
            date.append(metadata[0].text.split('\n')[1])

            # On crée une dataframe temporaire contenant les informations de la vidéo en cours de scraping et on concatène toutes les dataframes temporaires pour obtenir la dataframe finale.

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