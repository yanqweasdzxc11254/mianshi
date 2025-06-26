# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import json


class GetNikePipeline:
    def open_spider(self, spider):
        self.file = open('nike.json', 'w', encoding='utf-8')
        self.file.write('[')  # JSON数组开始

    def process_item(self, item, spider):
        # 将item转换为字典
        item_dict = dict(item)
        
        # 将item转换为JSON格式并写入文件
        line = json.dumps(item_dict, ensure_ascii=False, indent=2) + ',\n'
        self.file.write(line)
        
        return item

    def close_spider(self, spider):
        # 移除最后一个多余的逗号
        if self.file.tell() > 3:
            self.file.seek(self.file.tell() - 3, 0)
            self.file.truncate()
        
        # 结束JSON数组
        self.file.write(']')
        self.file.close()
    