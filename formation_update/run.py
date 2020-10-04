import sys, asyncio
if sys.version_info[0]==3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from formation_flying.server import server


server.port = 8600
server.launch()


