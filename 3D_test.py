import GT3lib as gt

root = gt.Window()

#load all textur
root.mesh.add_texture(path="path.jpg", name="name")

#load mesh
root.mesh.add_obj(root.ctx, path="path.obj", name="name")


class Main_scene(gt.Scene):
    def load(self):
        self.add_object(gt.Obj(self.app, scale=(0.1,0.1,0.1), vao_name="name", tex_id="name"))

root.scene=Main_scene(root)
root.run()
