import bpy
import numpy as np
from scipy.ndimage import convolve
import datetime
from mathutils import Vector
import random



def initial_status(side_len, probability):
    size = (side_len, side_len)
    status = np.random.binomial(1, probability, size)
    
    return status 
    
def check_alive(status):
    kernel = np.array([[1, 1, 1],
                       [1, 0, 1],
                       [1, 1, 1]])
    convolv = convolve(status, kernel, mode='constant', cval=0.)
    
    return convolv.astype(np.uint8)

def next_gen(status):
    stayin_alive = check_alive(status)
    duo = np.array((stayin_alive == 2), dtype=np.uint8) * status 
    trio = np.array((stayin_alive == 3), dtype=np.uint8)
    new_status = (trio + duo).astype(np.uint8)

    return new_status

start = datetime.datetime.now()

def localize(civilization):
    
    positions = []
    
    for i in range(-civilization, civilization):
        for j in range(-civilization, civilization):
            
            positions.append((i * 8, j * 8))
            
    return positions

civilizations = 4 # it is going to be (num * 2)**2 
localizations = localize(civilizations)

def of_tower(civilizations, localizations):
    obs = []
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0), scale=(1, 1, 1))
    ob = bpy.context.object
    sce = bpy.context.scene
    mat = bpy.data.materials.get("Material")
    limit = 42
    p_low = .4
    p_high = .6 
    low_b = 8
    high_b = 8               
    if ob.name.startswith("Cube"):
        ob.data.materials.append(mat) 
        
    for l in localizations:
        i = 0
        buffer = []
        gen = 6
        probability = np.random.uniform(p_low, p_high, 1)
        status = initial_status(gen, probability)
        
        while np.all((status) == 0) == False:
            status = next_gen(status)
            buffer.append(status)  
            
            if len(buffer) > 5:
                buffer.pop(0)  
                
            for j in range(len(status[0])):
                for k in range(len(status[1])):    
                    if status[j, k] == True:  
                        copy = ob.copy()
                        copy.location = Vector((l[0]+j, l[1]+k, i))
                        copy.data = copy.data.copy() # also duplicate mesh, remove for linked duplicate
                        obs.append(copy)
              
            if i > 5:
                if np.all((buffer[4]) == buffer[3]) == True:
                    break
                if np.all((buffer[4]) == buffer[2]) == True:
                    break
                if np.all((buffer[4]) == buffer[1]) == True:
                    break
                if np.all((buffer[4]) == buffer[0]) == True:
                    break
                if np.all((buffer[1]) == buffer[0]) == True:
                    break
                if i == limit:
                    break 
            i+=1
            
    for ob in obs:
        bpy.context.collection.objects.link(ob)

    dg = bpy.context.evaluated_depsgraph_get() 
    dg.update()


start = datetime.datetime.now()
bpy.ops.mesh.primitive_cube_add(size=.5, location=(0,0,0))
of_tower(civilizations, localizations)


   
end = datetime.datetime.now()    
print(end-start) 