import pandas as pd
from fetch_dogs import get_dogs


def main():
    dog_dict = get_dogs()
    dog_df = create_dog_table(dog_dict)
    compare_data(dog_df)


def create_dog_table(dog_dict):
    dog_df = pd.DataFrame(dog_dict)
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

