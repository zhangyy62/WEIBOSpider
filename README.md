# WEIBOSpider
This is project that capture sina weibo datas

# 第一种方式
参考博文 https://www.jianshu.com/p/f65829b22b91  
利用http://weibo.cn/{user_id}/profile?page={page_index}来分页获取某用户的微博内容

原理就是抓页面html元素来获取数据

# 第二种方式
移动端微博的API:https://m.weibo.cn/api/container/getIndex?containerid={containerid}_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&page={page}   
可通过get方法请求上面的API，再将数据结构JSON反序列化一下，直接从API结果获取数据。
