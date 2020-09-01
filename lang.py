from os import listdir,startfile
def Load_New_Lang(lang):
    from urllib.request import urlopen
    new_lang = urlopen(f'https://github.com/minimer/Mythical-Knight/blob/master/data/langs/{lang}?raw=true').read()
    with open(f'data/langs/{lang}', 'wb')as f: f.write(new_lang)
def langs():
    with open('data/langs/others/langs', 'r')as f:
        langs=sorted(f.readline().split())
    return langs
class Language:
    def __init__(self,lang):
        self.lang=lang
        if lang=='ru':return
        if not lang in listdir('data/langs'):Load_New_Lang(lang)
        with open(f'data/langs/others/words','r')as g:
            with open(f'data/langs/{lang}','r')as f:
                self.dict=dict(i for i in zip(g.readlines(),f.readlines()))
    def __getitem__(self, item):
        if self.lang=='ru':return item
        return self.dict[item]
a=Language('ru')