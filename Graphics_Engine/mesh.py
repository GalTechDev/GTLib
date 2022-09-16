from Graphics_Engine.vao import VAO
from Graphics_Engine import vbo
from Graphics_Engine.texture import Texture


class Mesh:
    def __init__(self, app):
        self.app = app
        self.vao = VAO(app.ctx)
        self.texture = Texture(app.ctx)

    def add_obj(self, app, name, path):
        if not name in self.vao.vbo.vbos.keys():
            self.vao.vbo.vbos[name] = vbo.ObjVBO(app, path)
            self.vao.vaos[name] = self.vao.get_vao(program=self.vao.program.programs['default'], vbo=self.vao.vbo.vbos[name])

    def add_texture(self, name, path=None, color=None):
        if not name in self.texture.textures.keys():
            if (path!=None and color!=None) or (path==None and color==None):
                raise Exception("You must give path OR color")
            else:
                if path!=None:
                    texture=self.texture.get_texture(path=path)
                else:
                    texture=self.texture.get_color(color=color)

            self.texture.textures.update({name:texture})

    def destroy(self):
        self.vao.destroy()
        self.texture.destroy()