from scrapy import cmdline

name = 'douban_movie -o douban2.csv'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())
