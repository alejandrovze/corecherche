def on_server_unloaded(server_context):
    import os
    dir_name = "myapp/static/split/"
    test = os.listdir(dir_name)

    for item in test:
        if item.endswith("temp.wav"):
            os.remove(os.path.join(dir_name, item))
