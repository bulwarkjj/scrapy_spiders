# Define here the models for your scraped items
#
# items opens the door to item pipeline, which processes the item scraped, we can tell how scrapy should process \n
# the scraped item. for example cleaning it, validation the fields and more.  Also, a inheritable class to make our data more \n
# structured, stronger, and yielding a Python object

import scrapy
from scrapy.item import Item, Field
# from scrapy.loader.processors import MapCompose, TakeFirst
from itemloaders.processors import MapCompose, TakeFirst
from datetime import datetime


class LearnSpidersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

def remove_quotes(text):
    """
    Strips the unicode quotes for cleaner data 
    """
    text = text.strip(u'\u201c'u'\u201d')
    return text 

def convert_date(text):
    """
    Converts author_birthday into Python formatted date for better data parasing
    """
    return datetime.strptime(text, '%B %d, %Y') 

class QuoteItem(Item):
    """
    Item loader - Stores extracted data and returns a list
    MapCompose  - enables me to apply multiple prociessing functions to a field
    TakeFirst - processor that takes the first value of the MapCompose list

    vars --> fields specified in quote_spider()
    """
    quote_content = Field(
        input_processor = MapCompose(remove_quotes),
        output_processor = TakeFirst()
    )
    author_name = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    author_birthday = Field(
        input_processor = MapCompose(convert_date),
        output_processor = TakeFirst()
    )
    author_bornlocation = Field(
        input_processor = MapCompose(),
        output_processor = TakeFirst()
    )
    author_bio = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    tags = Field()