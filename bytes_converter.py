class BytesConverter:
    def __init__(self, imgbytes=None, imgstr=None):
        self.imgbytes = imgbytes
        self.imgstr = imgstr

    def convert_to_bytes(self):
        return self.imgstr.encode('utf-8')

    def convert_to_str(self):
        return
