# Docker官方镜像
https://registry.hub.docker.com/r/yipengfei/movie-robot/

手把手教你安装：https://feather-purple-bdd.notion.site/b6c925bf2a9e44548bd4bdeea7d06946

# 启动命令
```
docker run -itd --restart=always --name=movie-robot -v /volume1/docker_stable/movie-robot:/data --env 'LICENSE_KEY=abc'  yipengfei/movie-robot:latest
```
-v 中源路径改成你自己的
--env的激活码也改成你自己的

[申请一周体验激活码](https://docs.qq.com/form/page/DS3FsQktHcGJ0b2xH)
这个填好了我会每天晚上睡前发邀到邮箱里

官方telgram免费大群：[加入智能影音机器人交流群](https://t.me/+shOuvzcee9I4ZDll)

微信免费群群二维码，更新不一定及时，还有个打赏vip交流群会比较活跃

<img src="https://yee-1254270141.cos.ap-beijing.myqcloud.com/movie_robot/wechatgroup.JPG" width="280" height="354" alt="微信群" style="float: left;"/>


进群有机会获得免费的体验码

# 功能
定时自动从豆瓣电影的想看、在看、看过中获取影音信息，然后去PT站（支持多家站点）自动检索种子，找到最佳资源后按豆瓣电影分类提交到BT下载工具下载。在下载前，会自动检查你的Emby中是否已经存在。
基于此功能机制，还顺带具备了下列功能：
- 将一部刚上映，或者还没上映的电影加入想看，当PT站更新时会第一时间帮你下好，被Emby扫描到后直接观看。
- 对剧集类型的影视资源，如果你正在看一部没更新完的剧，只要pt站更新，也会帮你对比本地影音库缺少的剧集开始自动下载。
现已支持mteam、hdsky同时搜索，对搜索结果汇总打分，选择你的最爱片源，支持自定义一切选种规则！
# 更新日志
2022.02.01
1. 增加支持新站点ssd
2. **支持Plex媒体服务

2022.01.31
4. 新增支持hdchina；
5. 优化归一化实现及部分打分逻辑，增强选种效果；
6. 优化剧集选择逻辑，增加文件尺寸估算算法，来确认资源是否真的包含全集资源（很多站资源标题规则不一致，比如 权力的游戏第八季，无法通过名字准确识别到底包含了整季资源还是部分资源）；


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

# 为什么有激活码
笔者开发这个小东西，是为了解决自己的需求顺便分享给大家，笔者有着稳定的工作，也不指望这个赚钱，做了激活体系，是不想让工具大范围传播。也是对当今的网络环境有些不满，大把的人，愿意去花几十几百甚至上万打赏一个主播，也不愿意花几块或者几十块钱支持好用的软件，支持精彩的文章。这种现象让我非常不舒服，所以决定封闭应用，但我会持续更新，github上可以看到未来全部的更新日志。

# 赞赏一下
<img src="https://raw.githubusercontent.com/pofey/movie_robot/main/pay.png" width="310" height="310" alt="赞赏码" style="float: left;"/>

# 作者微信
凭打赏获得激活码

<img src="https://raw.githubusercontent.com/pofey/movie_robot/main/wechat.png" width="338" height="432" alt="微信" style="float: left;"/>
