from selenium.webdriver.common.by import By
from selenium_manager import create_driver
import time
from typing import Any, Dict, List


def get_dogs(
            distance: int = 50,
            ages: List[str]=['Young', 'Adult'],
            house_trained: bool=True,
            good_with_dogs: bool=True,
            sizes: List[str]=['Medium', 'Large'],
            state: str='IL',
            zip: str='60614',
        ) -> Dict[str, List[Any]]:
    dog_params = {
        'distance': str(distance),
        'ages': ages,
        'house_trained': house_trained,
        'good_with_dogs': good_with_dogs,
        'sizes': sizes,
        'state': str.lower(state),
        'zip': zip,
    }
    cards = get_dog_cards(dog_params)
    dog_dict = clean_dog_cards(cards)
    
    return dog_dict


def get_dog_cards(params: Dict[str, str | List[str] | bool]) -> List[Any]:
    dog_cards = []
    page_num = 1
    next_page = True
    while next_page:
        url = generate_url(
            params['distance'], params['ages'], params['house_trained'],
            params['good_with_dogs'], params['sizes'], params['state'],
            params['zip'], page_num
        )
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


def clean_dog_cards(cards: List[Any]) -> Dict[str, List[Any]]:
    dog_df_dict = {'name':[], 'details':[], 'link':[]}
    for card in cards:
        label = card.get_attribute('aria-label').split(', ')
        name = label[0]
        details = label[2]
        link = card.get_attribute('href')
        
        dog_df_dict['name'].append(name)
        dog_df_dict['details'].append(details)
        dog_df_dict['link'].append(link)

    return dog_df_dict


def generate_url(
        distance: str, 
        ages: List[str],
        house_trained: bool,
        good_with_dogs: bool,
        sizes: List[str],
        state: str,
        zip: str,
        page_num: str,
        ):
    url_prefix = 'https://www.petfinder.com/search/dogs-for-adoption/us/'
    url_location = f'{state}/{zip}/?'
    url_distance = f'distance={distance}'
    url_age = '&'.join([f'age%5B{i}%5D={age}' for i, age in enumerate(ages)])
    url_size = '&'.join([f'size%5B{i}%5D={size}' for i, size in enumerate(sizes)])
    url_house_trained = 'attribute%5B0%5D=House+trained' if house_trained else ''
    url_good_with_dogs = 'household%5B0%5D=good_with_dogs' if good_with_dogs else ''
    url_page_num = f'page={page_num}'    

    url = (
        f'{url_prefix}{url_location}{url_distance}&{url_age}&{url_size}&'
        f'{url_house_trained}&{url_good_with_dogs}&{url_page_num}'
        )    

    return url


if __name__ == '__main__':
    get_dogs()
