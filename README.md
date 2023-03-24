# novel_comment_spider
## 一、需求简介：

爬取wuxiaworld网站仙侠小说板块的读者书评，并制作成数据集，保存在csv格式的文件中

## 二、运行流程

1. spider_wuxia.py为爬虫代码，保存到wuxia.csv
2. time_process.py为后续对时间格式的处理，首先将wuxia.csv时间列的Edite替换为空，然后将a year/a month/a day ago替换为1 year/1 month/1 day ago,最后运行time_process.py 即可将时间格式转换为期望格式。

## 三、需求具体说明

1、爬取wuxiaworld网站仙侠小说板块的读者书评，并制作成数据集，保存在csv格式的文件中

2、需要爬取的书籍在如下网址可查看到，有12本。

https://www.wuxiaworld.com/novels/?genre=Xianxia

3、以一本书籍为例，书评数据集的数据格式如下：

Title书名：评价的书籍名称。

![title](.\image\title.jpg)  

Author作者：书籍的作者。

![title](.\image\author.jpg) 

Translator译者：书籍的译者。

![title](.\image\translator.jpg)

Reviewer评论者：评论的读者ID或昵称。

![reviewer](.\image\reviewer.jpg)

Time评论时间：评论的时间戳或日期。![reviewer](.\image\time.jpg)

Score评分：读者对该书籍的评分。此处需简单计算一下分数，见注。 ![reviewer](.\image\score.jpg)

Content评论内容：读者对该书籍的评价和评论。     ![reviewer](.\image\content.jpg)

Website评论来源网站：网站名称

书评均来自wuxiaworld网站。

 注：

1、 由于评论是带有回复的，在爬取时把回复当作单独一条评论即可，无需合并。

2、 由于评论时间显示为××前，可能需要根据当前时间转换成具体的年月（日）。

3、 由于单个书评未附有评分，所以每本书籍下的评论评分统一处理为书籍的评分。

4、 评分计算方法：5分制，根据推荐率计算。如推荐率为83%，则评分为83/20≈4.1（保留一位小数即可）。
