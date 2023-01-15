# Dog Go


## Summary
Dog Go is a simple web scraping project intended to allow someone to quickly gather newly available dogs in their area, via scraping [PetFinder](https://www.petfinder.com). Users can then view these dogs via a barebones Django webapp.


## Structure
At the top level is all the config, documentation, and git files. All source code is stored in [src/..](/src/). The scraping process is all stored in [src/dog_go](/src/dog_go/), while the webapp is stored in [src/dog_go_webapp](/src/dog_go_webapp/)


## Workflow
When `fetch_dogs.py` is run, it calls `get_dogs(...)`. `get_dogs()` passes the given parameters to `get_dog_cards()`, which queries the website using the selenium library. The resulting list of selenium datatypes is passed to `clean_dog_cards()`, which cleans the data and stores it in a Pandas DataFrame.

An alternative method of running is the run `update_dogs.py`, which will run the same process with additional final steps. After creating the DataFrame of dogs, the DataFrame is queried against (data/old_dogs.csv)[/src/dog_go/data/old_dogs.csv], which contains previously acquired dogs (it is empty otherwise), so that the resulting DataFrame only has new dogs. The new dogs are then written to `old_dogs.csv` for any subsequent runs.

To view the dogs in the webapp, copy `old_dogs.csv` to [dog_go_webapp/src/data/](/src/dog_go_webapp/src/data/), then start the webapp via Django's `manage.py` command (`python manage.py runserver`).

![webapp-example](/assets/images/dog_go_webapp_example.png)


## Future Iterations
This is a very simplistic, rough around the edges project. This may be its final iteration, but if future changes were to be implemented, they would revolve around the webapp primarly. A few of the main things I would like to improve upon are:
- The ability to call `update_dogs.py` from the webapp and dynamically updating the site with new dogs.
- A better data structure for dogs in the webapp, even if it's just a sqlite3 database.
- A filter to more effeciently look through the dogs you scraped.
- The ability to add users, allowing each user to have their own set of searched dogs, based on their parameters.