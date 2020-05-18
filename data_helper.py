import pprint

pp = pprint.PrettyPrinter(indent=4)


def get_data(soup, driver):

    # Get top page listing data and add exception is item is not found

    address = soup.select(
        "#listing > div > div > section.listing-summary-grid.xs-mt2.xs-mb3.md-mt3 > section.listing-location.xs-flex-order-1.min-width-0 > h1")[0].get_text()
    city = soup.select(
        "#listing > div > div > section.listing-summary-grid.xs-mt2.xs-mb3.md-mt3 > section.listing-location.xs-flex-order-1.min-width-0 > div > a:nth-child(1)")[0].get_text()
    community = soup.select(
        "#listing > div > div > section.listing-summary-grid.xs-mt2.xs-mb3.md-mt3 > section.listing-location.xs-flex-order-1.min-width-0 > div > a:nth-child(2)")[0].get_text()
    price = soup.select(
        "body.listing.listing-active.logged-in:nth-child(2) div.wrapper:nth-child(1) section.section-main.gut.md-pb3 div.container.md-flex div.main-column.xs-col-12.md-col-8.md-pr3 section.listing-summary-grid.xs-mt2.xs-mb3.md-mt3:nth-child(1) section.listing-price.sm-text-right.xs-flex-order-2 div.xs-text-2.sm-text-1.bold.xs-inline.sm-block.xs-mr05.sm-mr0 > span.priv")[0].get_text()
    walk_score = soup.select(
        "body.listing.listing-active.logged-in:nth-child(2) div.wrapper:nth-child(1) section.section-main.gut.md-pb3 div.container.md-flex div.main-column.xs-col-12.md-col-8.md-pr3 section.section-listing.section-listing-pad.xs-mb5.md-mb3.xs-border-bottom-none.expandable:nth-child(4) section.section-listing-content.min-width-0:nth-child(1) div.column-container.sm-column-count-2.column-gap dl.column:nth-child(7) > dd.column-value")[0].get_text()
    age = soup.select(
        "#listing > div > div > section.section-listing.section-listing-pad.xs-mb5.md-mb3.xs-border-bottom-none.expandable > section > div > dl:nth-child(5) > dd > span")[0].get_text()
    days_on_site = soup.select(
        "#listing > div > div > section.listing-summary-grid.xs-mt2.xs-mb3.md-mt3 > section.listing-price.sm-text-right.xs-flex-order-2 > div.xs-text-5.sm-text-4.text-secondary")[0].get_text()
    mls_id = soup.select(
        "#listing > div > div > section.section-listing.section-listing-pad.xs-mb5.md-mb3.xs-border-bottom-none.expandable.expandable-open > section > div > dl.column.key-fact-mls > dd > span")[0].get_text()
    listed_by = soup.select(
        "#listing > div > div > section.section-listing.section-listing-pad.xs-mb5.md-mb3.xs-border-bottom-none.expandable.expandable-open > section > div > dl:nth-child(10) > dd")[0].get_text()
    type = soup.select(
        "#listing > div > div > section.section-listing.section-listing-pad.xs-mb5.md-mb3.xs-border-bottom-none.expandable.expandable-open > section > div > dl:nth-child(1) > dd > span")[0].get_text()
    style = soup.select(
        "#listing > div > div > section.section-listing.section-listing-pad.xs-mb5.md-mb3.xs-border-bottom-none.expandable.expandable-open > section > div > dl:nth-child(2) > dd > span")[0].get_text()

    top_page_data = {'address': address,
                     'city': city,
                     'community': community,
                     'price': price,
                     'walk_score': walk_score,
                     'listed_by': listed_by,
                     'age': age,
                     'days_on_site': days_on_site,
                     'mls_id': mls_id,
                     'type': type,
                     'style': style,
                     }

    # Get the granular listing data.

    keys_list = ['Status', 'Bedrooms', 'Bedrooms Plus', 'Bathrooms',
                 'Bathrooms Plus', 'Kitchens', 'Den/Family Room',
                 'Air Conditioning', 'Fireplace', 'Basement',
                 'Heating', 'Basement_', 'Heating_',
                 'Water Supply', 'Exterior',
                 'Driveway', 'Garage', 'Parking Places',
                 'Covered Parking Places',
                 'Taxes', 'Tax Year', 'Tax Legal Description',
                 'Fronting On', 'Frontage', 'Lot Depth', 'Lot Size Units',
                 'Pool', 'Cross Street', 'Municipality District']

    def get_bottom_data(soup, driver, keys_list):
        """
        Parses column data and formats into dict object.
        """
        new_list = []
        for i in soup.findAll("div", {"class": "column"}):
            text = str(i.get_text())
            items = list(filter(None, (text.split("\n"))))
            new_list.append(items)
        tempA = []
        tempB = []
        # Need to handle column data with identical names and different values.
        for index, item in enumerate(new_list, start=1):
            if item[0] == 'Basement':
                tempA.append(item)
                if len(tempA) == 2:
                    item[0] = 'Basement_'
            if item[0] == 'Heating':
                tempB.append(item)
                if len(tempB) == 2:
                    item[0] = 'Heating_'
            # Some pages returned list items with len = 1, so this condition
            # asigns a None value so it can be applied to the dictionary.
            if len(item) == 1:
                item.append(None)
        dict_ = dict(new_list)
        new_dict = {k: dict_[k] for k in keys_list if k in dict_}
        return new_dict

    bottom_page_data = get_bottom_data(soup, driver, keys_list)

    # merge both dictionaries
    _dict = {**top_page_data, **bottom_page_data}

    pp.pprint(_dict)
    return _dict
