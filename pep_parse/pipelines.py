# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
import datetime as dt

from collections import defaultdict

from pep_parse.settings import RESULTS_DIR


class PepParsePipeline:

    def __init__(self):
        self.results_dir = RESULTS_DIR
        self.results_dir.mkdir(exist_ok=True)

    def open_spider(self, spider):
        self.statuses = defaultdict(int)

    def process_item(self, item, spider):
        self.statuses[item.get('status')] += 1
        return item

    def close_spider(self, spider):
        now = dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f'status_summary_{now}.csv'
        file_path = self.results_dir / file_name
        with open(file_path, mode='w', encoding='utf-8') as f:
            csv.writer(
                f,
                dialect=csv.unix_dialect,
                quoting=csv.QUOTE_NONE,
            ).writerows([
                ('Status', 'Quantity'),
                *self.statuses.items(),
                ('Total', sum(self.statuses.values())),
            ])
