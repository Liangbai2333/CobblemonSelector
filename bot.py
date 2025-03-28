import nonebot
from nonebot.adapters.onebot.v11 import Adapter as OntBotAdapter  # 避免重复命名

# 初始化 NoneBot
nonebot.init()

# 注册适配器
driver = nonebot.get_driver()
driver.register_adapter(OntBotAdapter)

# 在这里加载插件
nonebot.load_plugins("bot-plugins")

if __name__ == "__main__":
    nonebot.run()