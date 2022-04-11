from selenium.webdriver.common.by import By
from selenium_manager import create_driver
import pandas as pd
import time


def main():
    cards = get_cards()
    dog_df = create_dog_table(cards)
    compare_data(dog_df)

def get_cards():
    dog_cards = []
    page_num = 1
    next_page = True
    while next_page:
        url = f'https://www.petfinder.com/search/dogs-for-adoption/us/il/60515/?age%5B0%5D=Young&attribute%5B0%5D=House+trained&distance=50&household%5B0%5D=good_with_dogs&page={page_num}&size%5B0%5D=Large&size%5B1%5D=Medium'
        driver = create_driver()
        driver.get(url)
        time.sleep(2)
        cards = driver.find_elements(by=By.CLASS_NAME, value='petCard-link')
        if len(cards) == 0:
            next_page = False
        else:
            dog_cards = dog_cards + cards
        page_num += 1
    return dog_cards

def create_dog_table(cards):
    dog_df_dict = {'name':[], 'details':[], 'link':[]}
    for card in cards:
        label = card.get_attribute('aria-label').split(', ')
        name = label[0]
        details = label[2]
        link = card.get_attribute('href')
        
        dog_df_dict['name'].append(name)
        dog_df_dict['details'].append(details)
        dog_df_dict['link'].append(link)

    dog_df = pd.DataFrame(dog_df_dict)
    dog_df = dog_df.loc[~dog_df.details.str.contains('pit', case=False)]
    return dog_df

def compare_data(new_dogs):
    old_dogs = pd.read_csv('data/old_dogs.csv')
    only_new = new_dogs.merge(old_dogs, how='left', on='link', indicator=True)
    only_new = only_new.loc[only_new['_merge'].eq('left_only')].drop(columns='_merge')
    print(f'There are {len(new_dogs)} dogs and {len(only_new)} new dogs!')
    for k,v in only_new.iterrows():
        print(f"{v['name_x']}, {v['details_x']}")

    new_dogs.to_csv('data/old_dogs.csv', index=False)
    print('Dog sheet updated.')

if __name__ == '__main__':
    main()

