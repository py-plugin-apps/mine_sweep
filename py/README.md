# minesweeper
zhenxun_bot 扫雷游戏
移植自[MeetWq](https://github.com/noneplugin/nonebot-plugin-minesweeper)，默认完成游戏时奖励10金币
## 安装
```
pip install nonebot_plugin_minesweeper
```
## 使用
- 扫雷 开始游戏；
- 扫雷初级 / 扫雷中级 / 扫雷高级 可开始不同难度的游戏；
- 可使用 -r/--row ROW 、-c/--col COL 、-n/--num NUM 自定义行列数和雷数；
- 可使用 -s/--skin SKIN 指定皮肤，默认为 winxp；
- 使用 挖开/open + 位置 来挖开方块，可同时指定多个位置；
- 使用 标记/mark + 位置 来标记方块，可同时指定多个位置；
- 位置为 字母+数字 的组合，如“A1”；
- 发送 查看游戏 查看当前游戏状态；
- 发送 结束扫雷 结束游戏；
- 使用 添加人员 + qq/@ 可以添加人员到游戏内，只能当前局内能进行游戏的人来进行添加；
### 更新
**2022/8/2**[v1.0]

1. 同步主仓库更新：添加扫雷人员限制；坐标改为在格子上显示

**2022/6/20**[v0.2]

1. 增加自定义地雷限制

**2022/6/18**[v0.1]

1. 初版
