
class FileInfo:
    def __init__(self, filename):
        self.filename = filename


class DataSetInfo:
    def __init__(self, name, uptime, count, filepath):
        self.name = name
        self.uptime = uptime
        self.count = count
        self.filepath = filepath


class ScriptInfo:
    def __init__(self, name, filepath, filetype, descript, upload_at, update_at):
        self.name = name
        self.filepath = filepath
        self.filetype = filetype
        self.descript = descript
        self.upload_at = upload_at
        self.update_at = update_at
