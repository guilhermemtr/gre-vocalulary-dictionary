class Tag:
    def __init__(self, tagId, tagName, tagDesc):
        self.tagId = tagId
        self.tagName = tagName
        self.tagDesc = tagDesc

    def getId(self):
        return self.tagId

    def getName(self):
        return self.tagName

    def getDesc(self):
        return self.tagDesc
