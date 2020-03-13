
"""
启动入口
"""

from scrapy import cmdline

if __name__ == '__main__':
    cmdline.execute(["scrapy", "crawl", "sub"])
