from random import randint as rand
from online import *
from lang import *
from auto_update import Check_For_Updates
import pygame


def menu():
    global stage
    n = len(listdir('data/images/bg')) - 1
    alpha = 256
    txt = Text(display, 'Mythical Knight', (0, 0, 1, 0.19))
    play = Button(display, (0.3, 0.4, 0.4, 0.1), lang['Играть'])
    setting = Button(display, (0.3, 0.55, 0.4, 0.1), lang['Настройки'])
    ext = Button(display, (0.3, 0.7, 0.4, 0.1), lang['Выйти'])
    while stage == 'menu':
        events = pygame.event.get()
        if alpha > 255:
            alpha = 0
            img = pygame.transform.smoothscale(pygame.image.load(f'data/images/bg/{rand(0, n)}.jpg').convert(),
                                               settings['display'])
        alpha += 3
        img.set_alpha(alpha)
        display.blit(img, (0, 0))
        txt.place()
        if play.is_pressed(events):
            stage = 'play'
        if setting.is_pressed(events):
            stage = 'setting'
        if ext.is_pressed(events):
            pygame.quit()
            exit()
        pygame.display.flip()


def setting():
    global stage, display, lang, settings
    n = len(listdir('data/images/bg')) - 1
    alpha = 256
    stg = ChooseBox(display, (0, 0.2, 1, 0.06), (lang['Изображение'], lang['Звук'], lang['Управление'], lang['Язык']))
    txt = Text(display, lang['Настройки'], (0, 0, 1, 0.19))
    save = Button(display, (0.51, 0.3, 0.23, 0.05), lang['Применить'])
    back = Button(display, (0.76, 0.3, 0.23, 0.05), lang['Назад'])

    scrn = Text(display, lang['Разрешение'], (0, 0.3, 0.25, 0.05))
    md = Text(display, lang['Режим экрана'], (0, 0.36, 0.25, 0.05))
    sizes = ('1920x1080', '1600x900', '1366x768', '1280x720', '960x540', '848x480', '640x360')
    w, h = settings['display']
    choose = sizes.index(f'{w}x{h}')
    screen = ListBox(display, (0.25, 0.3, 0.25, 0.05), sizes, choose)
    mode = ListBox(display, (0.25, 0.36, 0.25, 0.05), (lang['Оконный'], lang['Полноэкранный']), settings['fullscreen'])

    snd = Text(display, lang['Общая громкость'], (0, 0.3, 0.25, 0.05))
    sound = ScrollBar(display, (0.25, 0.3, 0.25, 0.05), settings['volume'])
    msc = Text(display, lang['Громкость музыки'], (0, 0.36, 0.25, 0.05))
    music = ScrollBar(display, (0.25, 0.36, 0.25, 0.05), settings['music'])

    #

    # lng=settings['lang']
    # LANGS=[Button(display,(0+(i%10)/10,0.4+i//10/20,0.1,0.05),l) for i,l in enumerate(sorted(LANGUAGES.keys()))]

    while stage == 'setting':
        events = pygame.event.get()
        if alpha > 255:
            alpha = 0
            img = pygame.transform.smoothscale(pygame.image.load(f'data/images/bg/{rand(0, n)}.jpg').convert(),
                                               settings['display'])
        alpha += 3
        img.set_alpha(alpha)
        display.blit(img, (0, 0))
        txt.place()
        if stg.choosen == 0:
            scrn.place()
            md.place()
            screen.place(events)
            if not screen.active: mode.place(events)
        if stg.choosen == 1:
            snd.place()
            msc.place()
            sound.place(events)
            music.place(events)
        if stg.choosen == 2:
            pass
        # if stg.choosen==3:
        #    for i in LANGS:
        #        if i.is_pressed(events):
        #            lng=i.txt.txt
        #        if lng==i.txt.txt:pygame.draw.rect(i.surface,(0,0,0),(0,0,*i.rect[2:]),7)
        stg.place(events)
        if save.is_pressed(events):
            # settings['lang']=lng
            settings['volume'] = sound.choosen
            settings['music'] = music.choosen
            settings['display'] = list(map(int, screen.choosen.txt.txt.split('x')))
            settings['fullscreen'] = mode.choosen.txt.txt == 'Полноэкранный'
            with open('data/settings', 'w')as f:
                f.write(dumps(settings))
            # if lng not in listdir('data/langs'):
            #    with open('data/langs/ru','r')as f:lang=loads(f.read())
            #    t=Translator()
            #    new_lang={}
            #    for i in lang:new_lang[i]=t.translate(i, lng, 'ru').text
            #    with open(f'data/langs/{lng}','w')as f:f.write(dumps(new_lang))
            with open(f'data/langs/{settings["lang"]}', 'r')as f:
                lang = loads(f.read())
            display = pygame.display.set_mode(settings['display'], pygame.FULLSCREEN * settings['fullscreen'])
            return
        if back.is_pressed(events):
            stage = 'menu'
        pygame.display.flip()


def play():
    global stage,server
    n = len(listdir('data/images/bg')) - 1
    alpha = 256
    txt = Text(display, lang['Играть'], (0, 0, 1, 0.19))
    port = Input(display, (0.5, 0.3, 0.175, 0.09), lang['Порт'], 5, '4228')
    host = ListBox(display, (0, 0.3, 0.5, 0.09), IPs())
    hostport = Input(display, (0, 0.4, 0.675, 0.09), lang['Хост:Порт'])
    back = Button(display, (0.3, 0.7, 0.4, 0.075), lang['Назад'])
    create = Button(display, (0.7, 0.3, 0.3, 0.09), lang['Создать'])
    connect = Button(display, (0.7, 0.4, 0.3, 0.09), lang['Присоединиться'])
    while stage == 'play':
        events = pygame.event.get()
        if alpha > 255:
            alpha = 0
            img = pygame.transform.smoothscale(pygame.image.load(f'data/images/bg/{rand(0, n)}.jpg').convert(),
                                               settings['display'])
        alpha += 3
        img.set_alpha(alpha)
        display.blit(img, (0, 0))
        txt.place()
        port.place(events)
        host.place(events)
        hostport.place(events)
        if create.is_pressed(events):
            server = f'{host.choosen.txt.txt}:{port.txt}'
            stage = 'create'
        if connect.is_pressed(events):
            server = hostport.txt
            stage='connect'
        if back.is_pressed(events): stage = 'menu'
        host.place(events)
        pygame.display.flip()


def create():
    global stage, mode
    txt = Text(display, lang['Игра'], (0, 0, 1, 0.19))
    n = len(listdir('data/images/bg')) - 1
    alpha = 256
    choose = ChooseBox(display, (0, 0.2, 1, 0.075), [lang[i] for i in listdir('modes')])
    back = Button(display, (0.1, 0.8, 0.3, 0.075), lang['Назад'])
    crt = Button(display, (0.6, 0.8, 0.3, 0.075), lang['Создать'])
    while stage == 'create':
        events = pygame.event.get()
        if alpha > 255:
            alpha = 0
            img = pygame.transform.smoothscale(pygame.image.load(f'data/images/bg/{rand(0, n)}.jpg').convert(),
                                               settings['display'])
        alpha += 3
        img.set_alpha(alpha)
        display.blit(img, (0, 0))
        txt.place()
        choose.place(events)
        if back.is_pressed(events): stage = 'play'
        if crt.is_pressed(events):
            mode=choose.dirs[choose.choosen].txt.txt
            startfile(f'modes/{mode}/server.py')
            stage='connect'
        pygame.display.flip()


def connect():
    global client
    client=Client(server)
    exec(f"from modes.{mode}.client import main\nmain()")

if __name__ == '__main__':
    Check_For_Updates()
    server=''
    mode=''
    with open('data/settings', 'r')as f:
        settings = loads(f.read())
    display = pygame.display.set_mode(settings['display'], pygame.FULLSCREEN * settings['fullscreen'])
    from vidgets import *
    lang = Language(settings['lang'])
    stage = 'menu'
    while True:
        if stage == 'menu': menu()
        if stage == 'setting': setting()
        if stage == 'play': play()
        if stage == 'create': create()
        if stage == 'connect': connect()
