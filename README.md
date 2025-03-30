# CobblemonSelector

## 介绍

使用Nonebot+Onebot v11构建的用于群聊内查询游戏内Minecraft - Cobblemon模组中的精灵数据、群系数据、精灵生成数据的机器人

所有数据来源于Cobblemon Mod，图片来源于原画

该项目仅仅是本人的一个练手项目，代码质量欠佳，如果有任何漏洞或不足请提出！

使用fastapi反向代理react，所以不需要额外使用nginx等进行反向代理，十分方便

## 技术栈

### 前端

* Vite
* TypeScript
* React
* React-Router
* Tailwindcss
* Axios

### 后端

* Python
* Fastapi
* nonebot

### 亮点

* 直接在根目录中运行npm run build && python bot.py 即可快速启动机器人

  

其实本来想作为Bukkit插件包装SpringBoot的形式来开发后端，这样更好获取Cobblemon的数据

但是由于把SpringBoot打包到Bukkit插件过于臃肿，并且服务器宕机时，查询系统也会跟着掉线

所以自己写了一个对方可梦模组数据的解析器，方便玩家在游戏外查询，当然现在已经没有回头路

## 使用方式

1. 安装Node.js并加入到环境变量

2. 在项目根目录中打开终端运行npm install && npm run build以构建前端文件

3. 安装 Python 并加入到环境变量

4. 安装onebot v11 adapter 并配置web sockets反向代理

5. 更改.env文件的端口设置

6.  有两种方式

   方式一 (推荐) 

   1. 创建Python虚拟环境并激活
   2. 安装Poetry: pip3 install poetry
   3. 构建Poetry: poetry install

   方式二(没测试，AI生成的)

   1. 直接运行 start.bat (Windows) 或 start.sh (MacOS/Linux)

7. 启动！在根目录中: python -m bot.py

## Developer: Liangbai2333