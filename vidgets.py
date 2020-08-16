import pygame
pygame.init()
pygame.scrap.init()

class Text:

    def __init__(self, master, text, rect, color=(255, 255, 255)):
        self.master=master
        self.txt=text
        x, y = self.master.get_size()
        rect = [rect[0] * x, rect[1] * y, rect[2] * x, rect[3] * y]
        font = pygame.font.SysFont('courier', round(min(rect[3],rect[2]/max(1,len(text))/0.6)))
        self.surface = font.render(text, True, color)
        w, h = self.surface.get_size()
        pos = [rect[0]+rect[2]//2,rect[1]+rect[3]//2]
        self.pos=(pos[0]-w//2,pos[1]-h//2)
    def place(self):
        self.master.blit(self.surface,self.pos)

class Button:
    def __init__(self, master, rect, text,txt_color=(0,0,0)):
        self.master=master
        x, y = self.master.get_size()
        self.rect = [rect[0] * x, rect[1] * y, rect[2] * x, rect[3] * y]
        self.surface=pygame.Surface(self.rect[2:])
        size=self.rect[2]/self.rect[3]/len(text)/0.6
        self.txt=Text(self.surface,text,(0,0,1,1),txt_color)
    def is_pressed(self,events):
        self.master.blit(self.surface,self.rect[:2])
        pos=pygame.mouse.get_pos()
        rect=self.rect
        if rect[0]<pos[0]<rect[0]+rect[2] and rect[1]<pos[1]<rect[1]+rect[3]:
            self.surface.fill((255,255,255))
            for ev in events:
                if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
                    events.clear()
                    return True
        else:
            self.surface.fill((200,200,200))
        pygame.draw.rect(self.surface,(0,0,0),[0,0]+rect[2:],1)
        self.txt.place()
        return False

class ListBox:
    def __init__(self, master, rect, texts, choosen=0):
        self._rect=tuple(rect)
        self.active=False
        self.buttons=[Button(master,(rect[0],rect[1]+(i+1)*rect[3],rect[2],rect[3]),texts[i]) for i in range(len(texts))]
        self.choosen=Button(master,rect,texts[choosen])
    def place(self,events):
        if self.active:
            for ev in events:
                if ev.type==pygame.MOUSEBUTTONDOWN:
                    self.active=False
            for i in self.buttons:
                if i.is_pressed(events):
                    self.choosen=Button(i.master,self._rect,i.txt.txt)
        elif self.choosen.is_pressed(events):self.active=True

class ChooseBox:
    def __init__(self,master,rect,texts,choosen=0):
        self.choosen=choosen
        rect=list(rect)
        rect[2]/=len(texts)
        self.dirs=[Button(master,(rect[0]+rect[2]*i,rect[1],rect[2],rect[3]),texts[i]) for i in range(len(texts))]
    def place(self,events):
        for i in range(len(self.dirs)):
            if self.dirs[i].is_pressed(events):
                self.choosen=i

class ScrollBar:
    def __init__(self,master,rect,choosen=0):
        self.choosen=choosen
        self.active=False
        self.master=master
        x, y = self.master.get_size()
        self.rect = [rect[0] * x, rect[1] * y, rect[2] * x, rect[3] * y]
        self.__M__=self.rect[3]/10
    def place(self,events):
        m=self.__M__
        pos=pygame.mouse.get_pos()
        for ev in events:
            if ev.type==pygame.MOUSEBUTTONDOWN:
                self.active=self.rect[0]<pos[0]<self.rect[0]+self.rect[2] and self.rect[1]<pos[1]<self.rect[1]+self.rect[3]
            if ev.type==pygame.MOUSEBUTTONUP:self.active=False
        if self.active:
            self.choosen=max(0,min(1,(pos[0]-self.rect[0]-m)/(self.rect[2]-m*2)))
        pygame.draw.rect(self.master,(255,255,255),self.rect,1)
        pygame.draw.rect(self.master,(255,255,255),(self.rect[0]+m,self.rect[1]+m,(self.rect[2]-m*2)*self.choosen,self.rect[3]-m*2))

class Input:
    def __init__(self,master,rect,bg_text,limit=15):
        self.master=master
        self.choosen=0
        self.limit=limit
        self.active=False
        x, y = self.master.get_size()
        self.rect = [rect[0] * x, rect[1] * y, rect[2] * x, rect[3] * y]
        self.surface=pygame.Surface(self.rect[2:])
        self.txt = ''
        self.text=Text(self.surface,self.txt,(0,0,1,1))
        self.bg_text=Text(self.surface,bg_text,(0,0,1,1),(150,150,150))
    def place(self,events):
        self.surface.fill((255,255,255))
        pygame.draw.rect(self.surface,(0,0,0),(0,0,*self.rect[2:]),1)
        pos = pygame.mouse.get_pos()
        rect = self.rect
        for ev in events:
            if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
                if rect[0] < pos[0] < rect[0] + rect[2] and rect[1] < pos[1] < rect[1] + rect[3]:
                    self.choosen=round((pos[0]-self.text.pos[0]-self.rect[0])*len(self.txt)/self.text.surface.get_width())
                    self.active=True
                else:
                    self.active=False
        if self.active:
            add=''
            keys = pygame.key.get_pressed()
            for ev in events:
                if ev.type==pygame.KEYDOWN:
                    if ev.key==pygame.K_LEFT:self.choosen-=1
                    elif ev.key==pygame.K_RIGHT:self.choosen+=1
                    elif ev.key==8:
                        self.txt=self.txt[:self.choosen-1]+self.txt[self.choosen:]
                        self.choosen-=1
                    elif ev.key==pygame.K_v and keys[pygame.K_LCTRL]:
                        try:add = pygame.scrap.get(pygame.SCRAP_TEXT).decode("UTF-8")[:-1]
                        except:pass
                    else:add+=ev.unicode
            add=add[:self.limit-len(self.txt)]
            self.txt=self.txt[:self.choosen] + add + self.txt[self.choosen:]
            self.text=Text(self.surface,self.txt,(0,0,1,1),(0,0,0))
            self.choosen+=len(add)
            self.choosen=max(0,min(self.choosen,len(self.txt)))
            x=self.text.pos[0]+self.text.surface.get_width() * self.choosen / max(1, len(self.txt))
            y=self.text.surface.get_height()/10
            pygame.draw.line(self.surface, (0, 0, 0), (x, y), (x, 8 * y))
        elif not len(self.txt):self.bg_text.place()
        self.text.place()
        self.master.blit(self.surface,self.rect[:2])
