import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
'''Initiating driver'''
url = 'https://www.footballcritic.com/premier-league/season-2022-2023/player-stats/all/2/65452'
chromeOption = Options()
chromeOption.add_argument("--headless")
chromeOption.add_argument('log-level=3')
browser = webdriver.Chrome(options=chromeOption)
browser.get(url)

'''
Key Variables
-------------
url: will need updating for new seasons with position filter set to all
valid_list: holds valid team list when new season begins to factor in promotions and relegations apply list(set(valid_list)) to get unique teams
line_width: Controls separation margin lengths
page: starting pagination page on webpage
end_page: last page of player list on url
Age Should either be a set {} of required ages or None to indicate no parameter set
Teams: Should be either be a set {} of required teams or None to indicate no parameter set

VALID TEAMS LIST = ['Arsenal', 'Aston Villa', 'Bournemouth', 'Brentford', 'Brighton', 'Chelsea', 'Crystal Palace', 'Everton', 'Fulham', 'Leeds Utd', 'Leicester City', 'Liverpool', 'Man City', 'Man Utd', 'Newcastle', 'Notts Forest', 'Southampton', 'Tottenham', 'West Ham', 'Wolves']
'''
valid_list = []
line_width = 98
page = 1
end_page = 16
Age = None
Teams = {"Arsenal"}

AgeList = "ALL"
if Age is not None:
    AgeList = ', '.join(map(str, Age))  # noqa

'''
total_matches: Tracks number of players that have played that meet criteria set above in Age and Teams
total_players: Tracks the total amount of players in the league that have had game time
'''

total_matches = 0
total_players = 0

'''Accept Privacy Policy'''

time.sleep(2.5)
browser.find_element(By.XPATH, value='//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]').click()

'''Get season from browser URL'''

season = browser.current_url.split("/")
season = season[4].split("-")
season_text = f'{season[0].upper()} {season[1]}-{season[2]}'

'''Print table Heading'''

print(f'{"-":-^{line_width}}')
print(f'{"Players Age " + AgeList + " [" + season_text + "]":^{line_width}}')
print(f'{"-":-^{line_width}}')
print(f'{"Name":<30} {"Position":<20} {"Team":<20} {"Age":<10}')
print(f'{"-":-^{line_width}}')

'''
Main loop. Gets relevant elements from webpage and puts them into separate arrays then cleans them for processing
'''
while page != end_page + 1:
    playerTeam = browser.find_elements(By.CLASS_NAME,
                                       value='General.Discipline.Defending.Errors.Disruption.Passing.Creation.Goals-assists.Scoring.Shooting.Decisive.Goalkeeping.mobOff')
    playerNames = browser.find_elements(By.CLASS_NAME, value="txt")
    playerPos = browser.find_elements(By.CLASS_NAME, value='only_desktop')
    playerAges = browser.find_elements(By.CLASS_NAME, value="cr.small.General.mobOff")
    cleanedAge = [item for item in playerAges if item.text != '']
    cleanedPos = playerPos[1::2]
    cleanedTeam = [playerTeam[x].get_attribute("data-sort") for x in range(4, len(playerTeam), 2)]
    total_players += len(playerNames)

    for name, pos, age, team in zip(playerNames, cleanedPos, cleanedAge, cleanedTeam):
        valid_list.append(team)
        if Age is None and Teams is None:
            print(f'{name.text:<30} {pos.text:<20} {team:<20} {age.text:<10}')
            total_matches = total_players
        elif Age is None and Teams is not None and team in Teams:
            print(f'{name.text:<30} {pos.text:<20} {team:<20} {age.text:<10}')
            total_matches += 1
        elif Age is not None and Teams is None and int(age.text) in Age:
            print(f'{name.text:<30} {pos.text:<20} {team:<20} {age.text:<10}')
            total_matches += 1
        elif Age is not None and Teams is not None and int(age.text) in Age and team in Teams:
            print(f'{name.text:<30} {pos.text:<20} {team:<20} {age.text:<10}')
            total_matches += 1

    browser.execute_script("arguments[0].click();", WebDriverWait(browser, 0.2).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "paginate_button.next"))))

    page += 1

if total_matches == 0:
    print(f'{"No Matches Found.":^{line_width}}')

'''Print table footer'''
print(f'{"-":-^{line_width}}')
print(f'{str(total_matches) + "/" + str(total_players) + " Players" :^{line_width}}')
print(f'{"-":-^{line_width}}')

browser.quit()
