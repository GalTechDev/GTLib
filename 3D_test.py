import GT3D.GT3lib as gt

root = gt.Window()

#load all textur
root.mesh.add_cube_texture(dir_path="GT3D/Graphics_Engine/textures/env", name="env")
#root.mesh.add_cube_texture(color=["blue","red","black","white","green","grey"], name="c_gray")


#load mesh
root.mesh.add_obj(root.ctx, path="GT3D/Graphics_Engine/objects/ship/untitled.obj", name="ship")

gravit = (0,-0.01,0)
air_resistance = 0.99
absorbtion = 1 - 0.8

class Test(gt.Cube):
    def custom_update(self):
        self.vel = (self.vel[0]+gravit[0],self.vel[1]+gravit[1],self.vel[2]+gravit[2]) #(self.pos[0], self.pos[1]-gravit*, self.pos[2])
        self.pos = (self.vel[0]*0.9+self.pos[0], self.vel[1]*0.9+self.pos[1], self.vel[2]*0.9+self.pos[2])
        self.rot_vel = (self.rot_vel[0]*air_resistance, self.rot_vel[1]*air_resistance, self.rot_vel[2]*air_resistance)
        rot = self.get_rot()
        self.set_rot((self.rot_vel[0]+rot[0], self.rot_vel[1]+rot[1], self.rot_vel[2]+rot[2]))
        
        if self.pos[1] < 0:
            self.pos = (self.pos[0], 0, self.pos[2])
            self.vel = (-self.vel[0]*absorbtion,-self.vel[1]*absorbtion,-self.vel[2]*absorbtion)
            self.rot_vel = ((-self.rot_vel[0])*absorbtion, (-self.rot_vel[1])*absorbtion, (-self.rot_vel[2])*absorbtion)

        keys = gt.pg.key.get_pressed()
        
        if keys[gt.pg.K_p]:
            self.pos = (0, 10, 0)
            self.vel = (0,0,0)
            self.rot_vel = (2,2,2)
    

class Main_scene(gt.Scene):
    def load(self):
        self.add_object(gt.EnvBox(self.app))
        self.add_object(gt.Obj(self.app, scale=(1,1,1), rot = (0,0,0), mesh_name="ship"))



root.scene=Main_scene(root)
root.run()
