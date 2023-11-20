import pygame

def relative_mouse_pos(surface_size,surface_pos=(0,0)):
    return relative_pos(pygame.mouse.get_pos(),surface_pos,pygame.display.get_window_size(),surface_size)

def relative_pos(pos_on_parent,pos_child,screen_parent,screen_child):
    absolut_pos = pos_on_parent
    relative_pos = ((int(screen_child[0]/screen_parent[0]*absolut_pos[0]-pos_child[0]),int(screen_child[1]/screen_parent[1]*absolut_pos[1]-pos_child[1])))
    return relative_pos