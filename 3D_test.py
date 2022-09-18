import GT3lib as gt

root = gt.Window()

#load all textur
root.mesh.add_cube_texture(dir_path="Graphics_Engine/textures/env", name="test")
root.mesh.add_cube_texture(color=["blue","red","black","white","green","grey"], name="c_gray")


#load mesh
root.mesh.add_obj(root.ctx, path="Graphics_Engine/objects/cat/20430_Cat_v1_NEW.obj", name="chat")
gravit = (0,-0.01,0)

class Test(gt.Cube):
    def custom_update(self):
        self.vel = (self.vel[0]+gravit[0],self.vel[1]+gravit[1],self.vel[2]+gravit[2]) #(self.pos[0], self.pos[1]-gravit*, self.pos[2])
        self.pos = (self.vel[0]*0.9+self.pos[0], self.vel[1]*0.9+self.pos[1], self.vel[2]*0.9+self.pos[2])
        rot = self.get_rot()
        self.set_rot((self.rot_vel[0]+rot[0], self.rot_vel[1]+rot[1], self.rot_vel[2]+rot[2]))
        
        if self.pos[1] < 0:
            self.pos = (self.pos[0], 10, self.pos[2])
            #self.vel = (0,0,0)

        keys = gt.pg.key.get_pressed()
        
        if keys[gt.pg.K_p]:
            self.pos = (0, 10, 0)
            self.vel = (0,0,0)
            self.rot_vel = (2,2,2)
        

    

class Main_scene(gt.Scene):
    def load(self):
        self.add_object(gt.Obj(self.app, scale=(0.1,0.1,0.1), rot = (-90,0,0), mesh_name="chat"))
        self.add_object(gt.EnvBox(self.app, tex_id="c_gray"))
        test = Test(self.app, scale=(1,0.1,1), pos=(0,0,0))
        self.add_object(test)



root.scene=Main_scene(root)
root.run()
