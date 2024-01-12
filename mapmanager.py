import pickle
class Mapmanager():
    def __init__(self):
        self.model = "block.egg"
        self.texture = "block.png"
        self.colors = [(0.2, 0.2, 0.35, 1),
                       (0.3, 0.5, 0.1, 1),
                        (0.4,0.6,0.2,1),
                         (0.5, 0.6, 0.7, 0.8)]

        self.startNew()

    def getColor(self, z):
        if z < 0:
            return self.colors[0]
        elif z < len(self.colors):
            return self.colors[z]
        else:
            return self.colors[-1]


    def startNew(self):
        self.land = render.attachNewNode("Land")

    def addBlock(self, position, texture=None):
        self.block = loader.loadModel(self.model)
        if texture==None:
            self.block.setTexture(loader.loadTexture(self.texture))
        else:
            self.block.setTexture(loader.loadTexture(texture))
        self.block.setPos(position)
        self.color = self.getColor(position[2])
        self.block.setColor(self.color)
        self.block.reparentTo(self.land)
        self.block.setTag("at", str(position))

    def clear(self):
        self.land.removeNode()
        self.startNew()



    def loadland(self, filename):
        self.clear()
        with open(filename) as file:
            y = 0
            for line in file.readlines():
                x = 0
                line = line.split(" ")
                for z in line:
                    for z0 in range(int(z)+1):
                        block = self.addBlock((x, y, z0))
                    x += 1
                y += 1
        return x,y
    def isEmpty(self,pos):
        pos = int(pos[0]) ,int(pos[1]), int(pos[2])
        blocks = self.findBlocks(pos)
        if blocks:
            return False
        else:
            return True
        

    def findBlocks(self,pos):
        return self.land.findAllMatches("=at=" + str(pos))
    
    def findHighestEmpty(self,pos):
        x, y, z = pos
        z = 1
        while not self.isEmpty((x, y, z)):
            z = z+1

        return x, y, z
    
    def delBlock(self, pos):
        blocks = self.findBlocks(pos)
        for block in blocks:
            block.removeNode()

    def delBlockFrom(self, pos):
        x, y, z = self.findHighestEmpty(pos)
        pos = x, y, z - 1
        for block in self.findBlocks(pos):
            block.removeNode()
            
    def buildBlock(self, pos, texture = None):
        x, y, z = pos
        new = self.findHighestEmpty(pos)
        if new[2] <= z + 1:
            if texture == None:
                self.addBlock(new)
            else:
                self.addBlock(new, texture = texture)

    def saveMap(self):
        blocks = self.land.getChildren()
        with open ("my_map.dat","wb") as fout:
            pickle.dump(len(blocks), fout)
            for block in blocks:
                x, y, z = block.getPos()
                pos = int(x), int(y), int(z)
                pickle.dump(pos, fout)


    def loadMap(self):
        self.clear()
        with open ("my_map.dat","rb") as fin:
            length = pickle.load(fin)
            for i in range(length):
                pos = pickle.load(fin)
                self.addBlock(pos)



    




    




    
