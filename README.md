# spider-common
轻量级通用爬虫框架，技术栈简单，简单可配置。

适用于无需反抓取，无需登录等情况下网站快速采集，仅用于个人研究使用，请勿滥用。

使用该框架最好具备如下知识：sqlite，python3，css选择器语法

**注意：该框架主要用于数据初级采集，即某个domain下的全量页面采集，不会对页面的特定元素进行解析。如需对网页中特定元素解析提取，可以利用采集后的网页信息进行提取即可。**


## 相关配置

chrome driver 配置
下载对应的驱动：将版本信息换成自己浏览器的：【143.0.7499.147】
https://storage.googleapis.com/chrome-for-testing-public/143.0.7499.147/mac-arm64/chromedriver-mac-arm64.zip


## 使用

添加domain:
sh add_domain.sh  "<your_domain_url>"

启动爬虫：
python3 main.py TaskDownloadPage 100 <domain_id>



## TODO 
- [ ] 存在抓取导航站情况，可以放开domain判断
- [ ] 优化缓存保存时长，domain可配置化
- [ ] 添加cookie设置选项
- [ ] 添加是否屏蔽图片选项
- [ ] 跨域抓取配置化（默认跨域抓取限制抓取层级不超过5）
- [ ] 忽略弹窗
- [ ] 下载图片
- [ ] 换用orm框架操作sqlite
- [ ] 设置定时抓取
- [ ] 部署到24h物理机上
- [ ] web前端
  - [ ] 添加一个domain
  - [ ] domain配置设置（尤其注意selector的设置）
