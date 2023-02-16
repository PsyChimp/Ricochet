import math3d
import pygame
import collide
import time
import random
class Player(object):
    def __init__(self,start_x,start_y,size,color):
        self.pos=math3d.VectorN(start_x,start_y,0)
        self.color=color
        self.size=size
        self.collide=False
        self.bullet_time=time.time()
        self.weapon="Pistol"
    def update(self,deltaTime,key_list,block_list,mouse_x,mouse_y,mouse_l,mouse_mid,mouse_r,bullet_manager):
        mouse_pos=math3d.VectorN(mouse_x,mouse_y,0)
        self.direction=math3d.VectorN(0,0,0)
        #movement controls
        if key_list[pygame.K_w]:
            self.pos[1]-=0.5 * deltaTime
            for block in block_list:
                if isinstance(block,Block):
                    if collide.collideCircleRectangle(self.pos[0],self.pos[1],self.size,block.x,block.y,block.x+block.length,block.y+block.width):
                        self.pos[1]+=1
                if isinstance(block,Circle):
                    dis=(block.pos-self.pos).magnitude()
                    if dis<=self.size+block.size:
                        self.pos[1]+=1
        if key_list[pygame.K_s]:
            self.pos[1]+=0.5 * deltaTime
            for block in block_list:
                if isinstance(block,Block):
                    if collide.collideCircleRectangle(self.pos[0],self.pos[1],self.size,block.x,block.y,block.x+block.length,block.y+block.width):
                        self.pos[1]-=1
                if isinstance(block,Circle):
                    dis=(block.pos-self.pos).magnitude()
                    if dis<=self.size+block.size:
                        self.pos[1]-=1
        if key_list[pygame.K_a]:
            self.pos[0]-=0.5 * deltaTime
            for block in block_list:
                if isinstance(block,Block):
                    if collide.collideCircleRectangle(self.pos[0],self.pos[1],self.size,block.x,block.y,block.x+block.length,block.y+block.width):
                        self.pos[0]+=1
                if isinstance(block,Circle):
                    dis=(block.pos-self.pos).magnitude()
                    if dis<=self.size+block.size:
                        self.pos[0]+=1
        if key_list[pygame.K_d]:
            self.pos[0]+=0.5 * deltaTime
            for block in block_list:
                if isinstance(block,Block):
                    if collide.collideCircleRectangle(self.pos[0],self.pos[1],self.size,block.x,block.y,block.x+block.length,block.y+block.width):
                        self.pos[0]-=1
                if isinstance(block,Circle):
                    dis=(block.pos-self.pos).magnitude()
                    if dis<=self.size+block.size:
                        self.pos[0]-=1
        old_dir=self.direction

        if mouse_pos==self.pos:
            self.direction=old_dir
        else:
            self.direction=(mouse_pos-self.pos).normalized()
        
        v=math3d.VectorN(self.direction[1]*-1,self.direction[0],0)
        self.gun_point=self.pos+self.direction*15
        self.hand_point=self.pos-v*5
        #weapon switching
        if key_list[pygame.K_1]:
            self.weapon = "Pistol"
        if key_list[pygame.K_2]:
            self.weapon = "Shotgun"
        if key_list[pygame.K_3]:
            self.weapon = "Automatic"
        if key_list[pygame.K_4]:
            self.weapon = "Railgun"
        if key_list[pygame.K_5]:
            self.weapon = "Flamer"
        #weapon controls
        if mouse_l and time.time()>=self.bullet_time:
            
            if self.weapon=="Pistol":
                bullet_manager.bullet_list.append(Bullet(self.gun_point[0],self.gun_point[1],self.direction,3,True,3,(255,140,0),self.weapon))
                self.bullet_time=time.time()+1
            if self.weapon=="Shotgun":
                x=self.direction
                for i in range(0,5):
                    offset=math3d.VectorN(random.uniform(-0.5,0.5),random.uniform(-0.5,0.5),0)
                    des=(x+offset).normalized()
                    bullet_manager.bullet_list.append(Bullet(self.gun_point[0],self.gun_point[1],des,3,True,3,(255,140,0),self.weapon))
                self.bullet_time=time.time()+1
            if self.weapon=="Automatic":
                offset=math3d.VectorN(random.uniform(-0.1,0.1),random.uniform(-0.1,0.1),0)
                des=self.direction+offset
                bullet_manager.bullet_list.append(Bullet(self.gun_point[0],self.gun_point[1],des,3,True,3,(255,140,0),self))
                self.bullet_time=time.time()+0.1
            if self.weapon=="Railgun":
                bullet_manager.bullet_list.append(Bullet(self.gun_point[0],self.gun_point[1],self.direction,5,False,3,(255,140,0),self.weapon))
                self.bullet_time=time.time()+5
            if self.weapon=="Flamer":
                if random.randint(0,1)==1:
                    color=(255,200,0)
                else:
                    color=(200,0,0)
                offset=math3d.VectorN(random.uniform(-0.3,0.3),random.uniform(-0.3,0.3),0)
                des=self.direction+offset
                bullet_manager.bullet_list.append(Bullet(self.gun_point[0],self.gun_point[1],des,0.5,True,7,color,self.weapon))
                self.bullet_time=time.time()+0.1
    def render(self,surface,mouse_x,mouse_y):
        pygame.draw.circle(surface,self.color,(int(self.pos[0]),int(self.pos[1])),self.size,0)
        pygame.draw.line(surface,(100,100,100),(int(self.hand_point[0]),int(self.hand_point[1])),(int(self.gun_point[0]),int(self.gun_point[1])),3)

class BlockManager(object):
    def __init__(self):
        self.block_list=[]
    def render(self,surface):
        for block in self.block_list:
            block.render(surface)

class Block(object):
    def __init__(self,x,y,length,width,color):
        self.x=x
        self.y=y
        self.length=length
        self.width=width
        self.color=color
        self.center=math3d.VectorN(x+length/2,y+width/2,0)
        
        
    def render(self,surface):
        pygame.draw.rect(surface,self.color,(self.x,self.y,self.length,self.width),0)
class Circle(object):
    def __init__(self,x,y,size,color):
        self.x=x
        self.y=y
        self.pos=math3d.VectorN(x,y,0)
        self.size=size
        self.color=color
    def render(self,surface):
        pygame.draw.circle(surface,self.color,(self.x,self.y),self.size,0)
class BulletManager(object):
    def __init__(self):
        self.bullet_list=[]
    def update(self,deltaTime,block_list):
        for bullet in self.bullet_list:
            bullet.update(deltaTime)
            for block in block_list:
                if bullet.collide==True:
                    if isinstance(block,Block):
                        if collide.collideCircleRectangle(bullet.pos[0],bullet.pos[1],3,block.x,block.y,block.x+block.length,block.y+block.width):
                            
                            if bullet.source_wep=="Flamer":
                                self.bullet_list.remove(bullet)
                                break
                            if bullet.ric_count>3:
                                self.bullet_list.remove(bullet)
                                break
                            
                            dis=block.center-bullet.pos
                            
                            if block.width<block.length:
                                scale=block.length/block.width
                                dis[1]*=scale
                            if block.width>block.length:
                                scale=block.width/block.length
                                dis[0]*=scale
                            if abs(dis[0])<abs(dis[1]):
                                
                                new_y=bullet.direction[1]*-1
                                new_dir=math3d.VectorN(bullet.direction[0],new_y,0)
                                bullet.ric_count+=1
                            if abs(dis[0])>abs(dis[1]):
                                
                                new_x=bullet.direction[0]*-1
                                new_dir=math3d.VectorN(new_x,bullet.direction[1],0)
                                bullet.ric_count+=1
                            if abs(dis[0])==abs(dis[1]):
                                
                                self.bullet_list.remove(bullet)
                                break
                            
                            
                            if new_dir.dot(bullet.direction)>-0.9:
                            
                                bullet.direction=new_dir
                            else:
                                self.bullet_list.remove(bullet)
                                break
                    if isinstance(block,Circle):
                        dis=(block.pos-bullet.pos).magnitude()
                        if dis<=block.size+bullet.size:
                            
                            offset=(bullet.pos-block.pos).normalized()
                            new_dir=(bullet.direction+offset).normalized()
                            bullet.ric_count+=1
                            
                            if new_dir.dot(bullet.direction)>-0.9:
                                bullet.direction=new_dir
                            else:
                                self.bullet_list.remove(bullet)
                                break

            if bullet.pos[0]>=800 or bullet.pos[0]<=0:
                self.bullet_list.remove(bullet)
                break
            if bullet.pos[1]>=600 or bullet.pos[1]<=0:
                self.bullet_list.remove(bullet)
                break
    def render(self,surface):
        for bullet in self.bullet_list:
            bullet.render(surface)

class Bullet(object):
    def __init__(self,start_x,start_y,direction,speed,collide,size,color,source_wep):
        self.pos=math3d.VectorN(start_x,start_y,0)
        self.direction=math3d.VectorN(direction[0],direction[1],0)
        self.speed=speed
        self.collide=collide
        self.size=size
        self.color=color
        self.source_wep=source_wep
        self.ric_count=0
    def update(self, deltaTime):
        self.pos+=self.direction*self.speed*deltaTime
    def render(self,surface):
        pygame.draw.circle(surface,self.color,(int(self.pos[0]),int(self.pos[1])),self.size,0)
if __name__=="__main__":
    pygame.init()

    clock = pygame.time.Clock()
    
    player1=Player(400,300,10,(250,0,0))
    
    bm=BlockManager()
    bul_m=BulletManager()
    bm.block_list.append(Block(100,100,100,100,(100,100,100)))
    bm.block_list.append(Block(200,200,70,35,(100,100,100)))
    bm.block_list.append(Block(50,200,35,70,(100,100,100)))
    bm.block_list.append(Circle(500,500,50,(100,100,100)))
    bm.block_list.append(Block(500,200,100,100,(100,100,100)))
    screen=pygame.display.set_mode((800,600),pygame.SWSURFACE,24)
    font = pygame.font.SysFont("Arial",20)
    
    while True:
        deltaTime = clock.tick() / 3
        mx,my=pygame.mouse.get_pos()
        ml,mm,mr=pygame.mouse.get_pressed()
        pygame.event.pump()

        keys=pygame.key.get_pressed()

        screen.fill((0,0,0))

        if keys[pygame.K_ESCAPE]:
            break

        player1.update(deltaTime,keys,bm.block_list,mx,my,ml,mm,mr,bul_m)
        player1.render(screen,mx,my)
        bm.render(screen)
        bul_m.update(deltaTime,bm.block_list)
        bul_m.render(screen)
        
        weapon_status = font.render(player1.weapon,0,(250,250,250))
        screen.blit(weapon_status,(0,0))
        pygame.display.flip()
    pygame.display.quit()
