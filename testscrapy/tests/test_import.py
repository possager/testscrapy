from importlib import import_module



moudle_name = import_module("testscrapy.my_own_scrapyd.twisted_websocket")

print(moudle_name)
print(moudle_name.websocketFactory)