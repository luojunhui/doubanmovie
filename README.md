# scrapy爬取[豆瓣选电影页面](https://movie.douban.com/explore "点我打开")的信息

# 安装
1. ```git clone https://github.com/luojunhui/doubanmovie.git```
2. ```cd doubanmovie```
3. ```virtualenv -p python3 .venv```,```source .venv/bin/activate```
4. ```pip install -r requirements.txt```

# 运行
```text
scrapy crawl douban -o movie.json
```

# 查看数据
```
cat movie.json
```