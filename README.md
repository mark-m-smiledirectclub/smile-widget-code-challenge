# smile-widget-code-challenge

The Smile Widget Company currently sells two types of smile widgets: a Big Widget and a Small Widget.  We'd like to add more flexibility to our product pricing.

# Note

Hey there SmileDirectClub engineer(s),

Opened a PR here for your review. A few comments:

- I created a `ProductPrice` model as requested. It's basically a model that denotes what a product's price is during some given time period. I was going to nuke `Product.price` and create a `ProductPrice` for the given `Product` fixtures, but after thinking about it, I decided that it's best to leave `Product.price` alone and have that denote a standard baseline price. Basically, if there is no `ProductPrice` for a given date `Product.price` becomes our fallback.

- This is fairly rough and I admit that it could use some polishing. For example, my PR leaves everything in cents and should be refactored to present our amounts in dollars/cents.

- Running tests can be done via `docker-compose run --rm web ./smilewidgets/manage.py test products` (I assume ya'll already know this but for documentation's sake)

Hope this covers it. Thanks for reviewing.

## Setup with Docker
1. Install Docker (https://docs.docker.com/install/)
2. Fork this repository.
3. `>>> docker-compose up --build`

## Setup without Docker
1. Install Python (>3.4)
2. Install postgres.  By default the Django app will connect to the database named 'postgres'.  See `settings.DATABASES`.
3. Fork this repository, then clone your repository locally.
4. Install requirements.
  * `>>> pip install -r requirements.txt`
5. Run migrations.
  * `>>> python manage.py migrate`
6. Load data from fixtures:
  * `>>> python manage.py loaddata 0001_fixtures.json`

### Technical Requirements
* We currently have two products with the following prices:
    * Big Widget - $1000
    * Small Widget - $99
* These products, along with existing gift cards are already setup in the database.  Study the existing models and initial data.
* Create a new ProductPrice model and setup the following price schedule:    
  * Black Friday Prices (November 23, 24, & 25)
    * Big Widget - $800
    * Small Widget - FREE!
  * 2019 Prices (starting January 1, 2019)
    * Big Widget - $1200
    * Small Widget - $125
* Build a JSON API endpoint that accepts a product code, date, and (optional) gift card and returns product price.
  * The endpoint should live at `api/get-price` and accept the following parameters:
    * `"productCode"`
    * `"date"`
    * `"giftCardCode"`
* Make all of your changes in a new feature branch and submit a pull request to _your own forked repo_.

### Additional Information
* Please use Django Rest Framework or a Python HTTP framework of your choice to create the endpoint.
* Just as a general guideline, we've designed this exercise to take less than 4 hours.
