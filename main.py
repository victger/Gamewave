from chromedriver.ChromeDriver import launch_driver
from twitch.Twitch import scrape_twitch
from youtube.Youtube import scrape_youtube
from app.elastic import es
from app.elastic_utils import insert_data, process_data
from app.flask_app import app

# driver = launch_driver()

# data_twitch = scrape_twitch(driver)
# data_youtube = scrape_youtube(driver, data_twitch)

# driver.quit()

# process_data(data_youtube)

# final_data = data_youtube.to_dict('records')
# insert_data(es, final_data)
    
app.run(debug=True)