key_switch_camera = 'c' # the camera is bound to the hero or not
key_switch_mode = 'z' # can get past obstacles or not


key_forward = 'w' # step forward (the direction the camera is pointing in)
key_back = 's' # step back
key_left = 'a' # step left (sideways from the camera)
key_right = 'd' # step right
key_up = 'e' # step up
key_down = 'q' # step down


key_turn_left = 'n' # turn the camera to the right (and the world to the left)
key_turn_right = 'm' # turn the camera to the left (and the world to the right)
key_build = 'b'
key_destroy = 'v'

key_savemap = 'k'
key_loadmap = 'p'

class Hero():
    def __init__(self, pos, land):
        self.land = land
        self.mode = True # pass through everything mode
        self.hero = loader.loadModel('smiley')
        self.hero.setColor(1, 0.5, 0)
        self.hero.setScale(0.3)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)
        self.cameraBind()
        self.accept_events()


    def cameraBind(self):
        base.disableMouse()
        base.camera.setH(180)
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0, 0, 1.5)
        self.cameraOn = True


    def cameraUp(self):
        pos = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2]-3)
        base.camera.reparentTo(render)
        base.enableMouse()
        self.cameraOn = False




    def changeView(self):
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()


    def turn_left(self):
        self.hero.setH((self.hero.getH() + 5) % 360)


    def turn_right(self):
        self.hero.setH((self.hero.getH() - 5) % 360)


    def look_at(self, angle):
        '''returns the coordinates which the hero at the point (x, y) moves to
        if they step towards angle '''


        x_from = round(self.hero.getX())
        y_from = round(self.hero.getY())
        z_from = round(self.hero.getZ())


        dx, dy = self.check_dir(angle)
        x_to = x_from + dx
        y_to = y_from + dy
        return x_to, y_to, z_from


    def just_move(self, angle):
        '''moves to the desired coordinates in any case'''
        pos = self.look_at(angle)
        self.hero.setPos(pos)


    def move_to(self, angle):
        if self.mode:
            self.just_move(angle)
    
    def check_dir(self,angle):
        '''returns the rounded changes in the X and Y coordinates
        corresponding to the movement towards the angle.
        The Y coordinate decreases if the hero is looking at a 0-degree angle,
        and increases when they look at a 180-degree angle.   
        The X coordinate increases if the hero is looking at a 90-degree angle,
        and decreases when they look at a 270-degree angle.   
            0-degree angle (from 0 to 20)      ->        Y - 1
            45-degree angle (from 25 to 65)    -> X + 1, Y - 1
            90-degree angle (from 70 to 110) -> X + 1
            from 115 to 155 -> X + 1, Y + 1
            from 160 to 200 -> Y + 1
            205 to 245 -> X - 1, Y + 1
            from 250 to 290 -> X - 1
            from 290 to 335 -> X - 1, Y - 1
            from 340 -> Y - 1 '''
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


    def forward(self):
        angle =(self.hero.getH()) % 360
        self.move_to(angle)


    def back(self):
        angle = (self.hero.getH()+180) % 360
        self.move_to(angle)
    
    def left(self):
        angle = (self.hero.getH() + 90) % 360
        self.move_to(angle)


    def right(self):
        angle = (self.hero.getH() + 270) % 360
        self.move_to(angle)


    def accept_events(self):
        base.accept(key_turn_left, self.turn_left)
        base.accept(key_turn_left + '-repeat', self.turn_left)
        base.accept(key_turn_right, self.turn_right)
        base.accept(key_turn_right + '-repeat', self.turn_right)


        base.accept(key_forward, self.forward)
        base.accept(key_forward + '-repeat', self.forward)
        base.accept(key_back, self.back)
        base.accept(key_back + '-repeat', self.back)
        base.accept(key_left, self.left)
        base.accept(key_left + '-repeat', self.left)
        base.accept(key_right, self.right)
        base.accept(key_right + '-repeat', self.right)
        base.accept(key_up, self.up)
        base.accept(key_up + '-repeat', self.up)
        base.accept(key_down, self.down)
        base.accept(key_down + '-repeat', self.down)
        base.accept(key_build, self.build)
        base.accept(key_destroy, self.destroy)
        base.accept(key_savemap, self.land.saveMap)
        base.accept(key_loadmap, self.land.loadMap)


        base.accept(key_switch_camera, self.changeView)
    def changeMode(self):
        if self.mode:
            self.mode = False
        else:
            self.mode = True
    def try_move(self, angle):
        pos = self.look_at(angle)
        if self.land.isEmpty(pos):
            pos = self.land.findHighestEmpty(pos)
            self.hero.setPos(pos)
        else:
            pos = pos[0], pos[1], pos[2] + 1
            if self.land.isEmpty(pos):
                self.hero.setPos(pos)
    def up(self):
        if self.mode:
            self.hero.setZ(self.hero.getZ()+1)
    def down(self):
        if self.mode and self.hero.getZ() > 1:
            self.hero.setZ(self.hero.getZ() -1)
    def build(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.addBlock(pos)
        else:
            self.land.buildBlock(pos)
    def destroy(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.delBlock(pos)
        else:
            self.land.delBlockFrom(pos)