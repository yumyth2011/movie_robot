# Docker官方镜像
https://registry.hub.docker.com/r/yipengfei/movie-robot/

手把手教你安装：https://feather-purple-bdd.notion.site/b6c925bf2a9e44548bd4bdeea7d06946

官方telgram大群：[加入智能影音机器人交流群](https://t.me/+shOuvzcee9I4ZDll)

微信群二维码，更新不一定及时
<img src="https://yee-1254270141.cos.ap-beijing.myqcloud.com/movie_robot/wechatgroup.JPG
" width="280" height="354" alt="微信群" style="float: left;"/>

进群有机会获得免费的体验码
# 功能
定时自动从豆瓣电影的想看、在看、看过中获取影音信息，然后去PT站（支持多家站点）自动检索种子，找到最佳资源后按豆瓣电影分类提交到BT下载工具下载。在下载前，会自动检查你的Emby中是否已经存在。
基于此功能机制，还顺带具备了下列功能：
- 将一部刚上映，或者还没上映的电影加入想看，当PT站更新时会第一时间帮你下好，被Emby扫描到后直接观看。
- 对剧集类型的影视资源，如果你正在看一部没更新完的剧，只要pt站更新，也会帮你对比本地影音库缺少的剧集开始自动下载。
现已支持mteam、hdsky同时搜索，对搜索结果汇总打分，选择你的最爱片源，支持自定义一切选种规则！
# 更新日志
2022.01.30
1. 重新设计实现了剧集（综艺、电视剧）的选种逻辑，如果你在豆瓣点了一部想看的电视剧，如果这部剧还没更新完，初次下载，会帮你把已更新剧集的种子，都下上。如果你已经有了最新的剧集，只要出新的，就自动帮你下最新一集；如果一部剧已经完整的更新完，则会选择全集资源包优先下载；
2. 加速PT站点第一次访问速度；

2022.01.28
1. 修复tjupt初次下载或很久没在页面点下载需要手动确认导致失败的BUG；
2. 修复Qbit下载工具web api登陆过期无法正常使用的BUG；
3. 修复cookie对多余分号处理错误的BUG；

2022.01.27
1. 增加pt站点北洋园支持
2. 豆瓣支持cookie登陆，解决极其罕见的电影信息需要登陆获取的问题
3. 修复hdsky下载数取成正在下载数的BUG；
4. 修复单个pt站点挂了，导致其他pt站搜索不可用的BUG；


# 特别说明
发现了一些人，拿走代码随便改一下，就二次宣传，所以决定不再开源。
任何人都可以搜索movie-robot直接安装镜像，但是为了控制用户量，保证作者的更新热情，打赏一杯咖啡，即可获得永久授权码，加入vip讨论群。
# 赞赏一下
<img src="https://raw.githubusercontent.com/pofey/movie_robot/main/pay.png" width="310" height="310" alt="赞赏码" style="float: left;"/>

# 作者微信
凭打赏获得激活码

<img src="https://raw.githubusercontent.com/pofey/movie_robot/main/wechat.png" width="338" height="432" alt="微信" style="float: left;"/>
