# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
from learn_spiders.models import Author, Quote, Tag, create_table, db_connect


class LearnSpidersPipeline:
    def process_item(self, item, spider):
        return item

class SaveQuotesPipeline():
    def __init__(self) -> None:
        """
        Initializes database connection and sessionmaker
        Uses functions from models.py to connect to database (db_connect) and creates tables (create_table) if not existed yet
        """

        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """
        Save quotes in the database 
        This method is called for every item pipeline component
        creates instances for the database session and correspondes author info and quote test to the three tables in models.py (Author, Quote, Tag)
        """

        session = self.Session()
        quote = Quote()
        author = Author()
        tag = Tag()
        author.name = item["author_name"]
        author.birthday = item["author_birthday"]
        author.bornlocation = item["author_bornlocation"]
        author.bio = item["author_bio"]
        quote.quote_content = item["quote_content"]

        # check whether the author exists
        exist_author = session.query(Author).filter_by(name = author.name).first()
        if exist_author is not None: # the current author exists
            quote.author = exist_author
        else:
            quote.author = author 

        # check whether the current quote has tags or not
        if "tags" in item:
            for tag_name in item["tags"]:
                tag = Tag(name = tag_name)
                # check whether the current tag already exists in the database
                exist_tag = session.query(Tag).filter_by(name = tag.name).first()
                if exist_tag is not None: # the current tag exists
                    tag = exist_tag
                quote.tags.append(tag)

        # adds quote to database if exists
        try:
            session.add(quote)
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item

class DuplicatesPipeline(object):

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates tables.
        Checks for duplicated tables and drops the duplicate from the pipeline
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)
        logging.info("****DuplicatesPipeline: database connected****")

    def process_item(self, item, spider):
        session = self.Session()
        exist_quote = session.query(Quote).filter_by(quote_content = item["quote_content"]).first()
        session.close()
        if exist_quote is not None:  # the current quote exists
            raise DropItem("Duplicate item found: %s" % item["quote_content"])
        else:
            return item