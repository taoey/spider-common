# spider-common
通用爬虫框架，适用于无需反抓取，无需登录等情况下网站快速采集，仅用于个人研究使用，请勿滥用


driver 配置
https://storage.googleapis.com/chrome-for-testing-public/143.0.7499.147/mac-arm64/chromedriver-mac-arm64.zip


## 使用

启动爬虫：python3 main.py TaskDownloadPage 100



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
