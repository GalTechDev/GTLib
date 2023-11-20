import pygame as pg
import moderngl as mgl


class Texture:
    def __init__(self, ctx):
        self.ctx = ctx
        self.textures = {}
        self.textures[0] = self.get_texture(path='Graphics_Engine/textures/img.png')
        self.textures[1] = self.get_texture(path='Graphics_Engine/textures/img_1.png')
        self.textures[2] = self.get_texture(path='Graphics_Engine/textures/img_2.png')
        self.textures['grey'] = self.get_color("grey")
                

    def get_color(self, color):
        texture = pg.Surface((1,1))
        texture.fill(color)
        texture = self.ctx.texture(size=texture.get_size(), components=3,
                                   data=pg.image.tostring(texture, 'RGB'))
        # mipmaps
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()
        # AF
        texture.anisotropy = 32.0
        print(type(texture))
        return texture

    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=3,
                                   data=pg.image.tostring(texture, 'RGB'))
        # mipmaps
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()
        # AF
        texture.anisotropy = 32.0
        return texture

    def get_texture_cube(self, dir_path, ext = ".png"):
        #faces = ['right', 'left', 'top', 'bottom'] + ['front', 'back'][::-1]
        faces = ['right', 'left', 'top', 'bottom', 'back', 'front']
        textures = []
        for face in faces:
            texture = pg.image.load(f"{dir_path}/{face}{ext}").convert()
            if face in ['right', 'left', 'front', 'back']:
                texture = pg.transform.flip(texture, flip_x=True, flip_y=False)
            else:
                texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
            textures.append(texture)

        size = textures[0].get_size()
        texture_cube = self.ctx.texture_cube(size=size, components=3, data=None)

        for i in range(6):
            texture_data = pg.image.tostring(textures[i], 'RGB')
            texture_cube.write(face=i, data=texture_data)
        
        return texture_cube

    def get_color_cube(self, color: int | str | list | tuple):
        '''list or tuple must be : ['right', 'left', 'top', 'bottom', 'back', 'front']'''
        textures = []
        if type(color) in [str,int]:
            for i in range(6):
                texture = pg.Surface((1,1))
                texture.fill(color)
                textures.append(texture)
        elif type(color) in [tuple,list] and len(color)==6:
            for c in color:
                texture = pg.Surface((1,1))
                texture.fill(c)
                textures.append(texture)
        
        size = textures[0].get_size()
        texture_cube = self.ctx.texture_cube(size=size, components=3, data=None)
        
        for i in range(6):
            texture_data = pg.image.tostring(textures[i], 'RGB')
            texture_cube.write(face=i, data=texture_data)
        
        return texture_cube

    def destroy(self):
        [tex.release() for tex in self.textures.values()]

    