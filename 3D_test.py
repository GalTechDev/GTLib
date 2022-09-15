import GT3lib as gt

root = gt.Window()

#load all textur
root.mesh.add_texture(path="Graphics_Engine/objects/cat/20430_cat_diff_v1.jpg", name="chat")

#load mesh
root.mesh.add_obj(root.ctx, path="Graphics_Engine/objects/cat/20430_Cat_v1_NEW.obj", name="chat")


class Main_scene(gt.Scene):
    def load(self):
        self.add_object(gt.Obj(self.app, scale=(0.1,0.1,0.1), rot = (-90,0,0), mesh_name="chat", tex_id="chat"))

root.scene=Main_scene(root)
root.run()
