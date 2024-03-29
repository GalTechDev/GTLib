from .vao import VAO
from . import vbo
from .texture import Texture


class Mesh:
    def __init__(self, app):
        self.app = app
        self.vao = VAO(app.ctx)
        self.texture = Texture(app.ctx)

    def add_obj(self, app, name, path):
        if not name in self.vao.vbo.vbos.keys():
            objvbo = vbo.ObjVBO(app, path)
            print(objvbo.vbo)
            if objvbo.vbo:
                self.vao.vbo.vbos[name] = objvbo
                self.vao.vaos[name] = self.vao.get_vao(program=self.vao.program.programs['default'], vbo=self.vao.vbo.vbos[name])

    def add_cube_texture(self, name, dir_path=None, color=None, ext=".png"):
        if not name in self.texture.textures.keys():
            if (dir_path!=None and color!=None) or (dir_path==None and color==None):
                raise Exception("You must give path OR color")
            else:
                if dir_path!=None:
                    texture=self.texture.get_texture_cube(dir_path=dir_path, ext=ext)
                else:
                    texture=self.texture.get_color_cube(color=color)

            self.texture.textures.update({name:texture})



        if not name in self.texture.textures.keys():
            texture=self.texture.get_texture_cube(dir_path=dir_path, ext=ext)
            self.texture.textures.update({name:texture})

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