
key_switch_camera = 'c'  # the camera is bound to the hero or not
key_switch_mode = 'z'  # can get past obstacles or not

key_forward = 'w'  # step forward (the direction the camera is pointing in)
key_back = 's'  # step back
key_left = 'a'  # step left (sideways from the camera)
key_right = 'd'  # step right
key_up = 'e'  # step up
key_down = 'q'  # step down

key_turn_left = 'n'  # turn the camera to the right (and the world to the left)
# turn the camera to the left (and the world to the right)
key_turn_right = 'm'
key_build = "b"
key_del = "j"
change_block_brick = "1"
change_block_wood = "2"
change_block_stone = "3"
current_texture = "brick.png"


class Hero():
    def __init__(self, pos, land):
        self.land = land
        self.hero = loader.loadModel("smiley")
        self.hero.setColor((0.2, 0.5, 0.4,1))
        self.hero.setScale(0.4)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)
        self.cameraBind()
        self.accept_events()
        self.mode = True
    def cameraBind(self):
        base.disableMouse()
        base.camera.setHpr(180, 0, 0)
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0,0,1.5)
        self.cameraOn = True
    
    def cameraUp(self):
        pos = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2] - 3)
        base.camera.reparentTo(render)
        base.enableMouse()
        self.cameraOn = False

    def changeTexture(self, button_clicked):
        global current_texture
        if (button_clicked == 1):
            current_texture = "brick.png"
        elif(button_clicked == 2):
            current_texture = "stone.png"
        elif (button_clicked == 3):
            current_texture = "wood.png"

    def accept_events(self):
        base.accept("c", self.changeView)
        base.accept(key_turn_left, self.turn_left)
        base.accept(key_turn_left + "-repeat",self.turn_left)
        base.accept(key_turn_right, self.turn_right)
        base.accept(key_turn_right + "-repeat",self.turn_right)

        base.accept(key_back, self.back)
        base.accept(key_back + "-repeat",self.back)
        base.accept(key_forward, self.forward)
        base.accept(key_forward + "-repeat",self.forward)
        base.accept(key_right, self.right)
        base.accept(key_right + "-repeat",self.right)
        base.accept(key_left, self.left)
        base.accept(key_left + "-repeat",self.left)
        
        base.accept(key_up, self.up)
        base.accept(key_up + "-repeat",self.up)
        base.accept(key_down, self.down)
        base.accept(key_down + "-repeat",self.down)
        base.accept(key_switch_mode, self.change_Mode)



        base.accept(key_build, self.build)
        base.accept(key_del, self.destroy)


        base.accept("k", self.land.saveMap)
        base.accept("l", self.land.loadMap)


        base.accept(change_block_brick, self.changeTexture, [1])
        base.accept(change_block_stone, self.changeTexture, [2])
        base.accept(change_block_wood, self.changeTexture, [3])

    def changeView(self):
        if self.cameraOn == True:
            self.cameraUp()
        else:
            self.cameraBind()
    
    def just_move(self, angle):
        pos = self.look_at(angle)
        self.hero.setPos(pos)
    def try_move(self, angle):
        pos = self.look_at(angle)
        if self.land.isEmpty(pos):
            pos = self.land.findHighestEmpty(pos)
            self.hero.setPos(pos)
        else:
            pos = pos[0], pos[1], pos[2] + 1
            if self.land.isEmpty(pos):
                self.hero.setPos(pos)
        
    def move_to(self, angle):
        if self.mode == True:
            self.just_move(angle)
        else: 
            self.try_move(angle)
    def look_at(self, angle):
        from_x = round(self.hero.getX())
        from_y = round(self.hero.getY())
        from_z = round(self.hero.getZ())
        dx, dy = self.check_dir(angle)
        return from_x + dx, from_y + dy, from_z

    def check_dir(self, angle):
        if angle >= 0 and angle <= 20:
            return (0, -1)
        elif angle <= 65:
            return (1, -1)
        elif angle <= 110:
            return (1, 0)
        elif angle <= 155:
            return (1, 1)
        elif angle <= 200:
            return (0, 1)
        elif angle <= 245:
            return (-1, 1)
        elif angle <= 290:
            return (-1, 0)
        elif angle <= 335:
            return (-1, -1)
        else:
            return (0, -1)
    def back(self):
        angle = (self.hero.getH()+180) % 360
        self.move_to(angle)
    def right(self):
        angle = (self.hero.getH()-90) % 360
        self.move_to(angle)
    def left(self):
        angle = (self.hero.getH()+90) % 360
        self.move_to(angle)

    def forward(self):
        angle = self.hero.getH()
        self.move_to(angle)

    def turn_right(self):
        a = self.hero.getH()
        a = a - 5
        self.hero.setH(a%360)
    
    def turn_left(self):
        a = self.hero.getH()
        a = a + 5
        self.hero.setH(a%360)
    def up(self):
        if self.mode:
            self.hero.setZ(self.hero.getZ()+1)
    def down(self):
        if self.mode and self.hero.getZ()>1:
            self.hero.setZ(self.hero.getZ()-1)

    def change_Mode(self):
        if self.mode:
            x, y, z = self.hero.getPos()
            z -= 1
            while self.land.isEmpty((x, y, z)):
                if z == 1:
                    break
                self.down()
                z -= 1
            self.mode=False
        else:
            self.mode = True


    def build(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.addBlock(pos, texture=current_texture)
        else:
            self.land.buildBlock(pos, texture = current_texture)



    def destroy(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.delBlock(pos)
        else:
            self.land.delBlockFrom(pos)





    
