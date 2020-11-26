#!/usr/bin/env python3

allowed_times = ['supereon', 'eon', 'era', 'period', 'epoch', 'age']
allowed_types = ['general', 'life', 'geologic', 'glac']

class time:
    def __init__(self, typ, name, start, end):
        if typ not in allowed_times:
            raise Exception('{} not in allowed types'.format(typ))
        self.typ = typ # eon, subeon, era, or period
        self.name = name # name of time
        self.start = start # start year (Ma)
        self.end = end # end year (Ma)

class event:
    def __init__(self, name, t, start=False, end=False, desc=False, typ='general'):
        self.name = name
        self.t = t
        self.start = start
        self.end = end
        self.desc = desc
        self.typ = typ
        
class timeline:
    # holds time classes
    def __init__(self):
        self.t = {}
        self.events = []
        for i in allowed_times:
            self.t[i] = []
        
    def add(self, obj):
        if type(obj) is time:
            self.t[obj.typ].append(obj)
        elif type(obj) is event:
            self.events.append(obj)

    def get_list(self, typ):
        # returns a time sorted list of objects of the allowed time (era, subeon etc) from oldest to newest
        if typ not in allowed_times:
            raise Exception('{} not in allowed types'.format(typ))
        return sorted(self.t[typ], key = lambda i: i.start, reverse=True) 

    def get_events_list(self):
        # returns events in order
       return sorted(self.events, key= lambda i: i.t, reverse=True)


    def print(self):
        for i in allowed_times:
            lst = self.get_list(i)
            print( '---{}---'.format(i.upper()))
            for tim in lst:
                print('{} to {} Ma -- {} {}'.format(cvt_num(tim.start), cvt_num(tim.end), cvt_s(tim.name), cvt_s(i)))
            print()
        self.print_events()

    def print_events(self):
        print('---EVENTS---')
        for e in self.get_events_list():
            if e.start == False and e.end == False:
                print('{} Ma -- {}'.format(cvt_num(e.t), e.name))
            else:
                print('{} to {} Ma -- {}'.format(cvt_num(e.start), cvt_num(e.end), e.name))
            

def cvt_num(num):
    '''converts num to string'''
    return '{:.2f}'.format(float(num)).rstrip('0').rstrip('.')

def cvt_s(s):
    return s.lower().capitalize()

t = timeline()

# add supereon
t.add(time('supereon', 'Precambrian', 4540., 541.))

# add eons
t.add(time('eon', 'Hadean', 4540, 4000))
t.add(time('eon', 'Archean', 4000, 2500))
t.add(time('eon', 'Proterozoic', 2500, 541))
t.add(time('eon', 'Phanerozoic', 541, 0))

# add era
t.add(time('era','Eoarchean', 4000,3600))
t.add(time('era','Paleoarchean', 3600,3200))
t.add(time('era','Mesoarchean', 3200,2800))
t.add(time('era','Neoarchean', 2800,2500))
t.add(time('era','Paleoproterozoic', 2500,1600))
t.add(time('era','Mesoproterozoic', 1600,1000))
t.add(time('era','Neoproterozoic', 1000,541))
t.add(time('era', 'Paleozoic', 541, 251.9))
t.add(time('era', 'Mesozoic', 251.9, 66.))
t.add(time('era', 'Cenozoic', 66.,0.))

# add period
t.add(time('period','Siderian',2500,2300))
t.add(time('period','Rhyacian',2300,2050))
t.add(time('period','Orosirian',2050,1800))
t.add(time('period','Statherian',1800,1600))
t.add(time('period','Calymmian',1600,1400))
t.add(time('period','Ectasian',1400,1200))
t.add(time('period','Stenian',1200,1000))
t.add(time('period','Tonian',1000,720))
t.add(time('period','Cryogenian',720,635))
t.add(time('period','Ediacaran',635,541))

t.add(time('period','Cambrian', 541, 485.4))
t.add(time('period','Ordovician', 485.4,443.8))
t.add(time('period','Silurian', 443.8, 419.2))
t.add(time('period','Devonian', 419.2, 358.9))
t.add(time('period','Carboniferous', 358.9,298.9))
t.add(time('period','Permian', 298.9, 251.9))
t.add(time('period','Triassic', 251.9, 201.3))
t.add(time('period','Jurassic', 201.3,145.0))
t.add(time('period','Cretaceous', 145.0,66.0))

t.add(time('period','Paleogene',66.0,23.03))
t.add(time('period','Neogene',23.03,2.588))
t.add(time('period', 'Quaternary', 2.588,0)) 

# add epoch
t.add(time('epoch','Paleocene', 66,56))
t.add(time('epoch','Eocene', 56,33.9))
t.add(time('epoch','Oligocene', 33.9,23.03))
t.add(time('epoch','Miocene', 23.3, 5.333))
t.add(time('epoch','Pliocene', 5.333,2.58))
t.add(time('epoch','Pleistocene', 2.58, 0.012))
t.add(time('epoch','Holocene', 0.012, 0.0))

# add events
# general
t.add(event('Earth forms from the solar protoplanetary disk', 4540))
t.add(event('the big thwack', 4425, start=4450, end=4400))
t.add(event('Late Heavy Bombardment', 3950, start=4100, end=3800))
t.add(event('\'boring\' billion', 1300, start=1800, end=800))
t.add(event('Paleocene–Eocene Thermal Maximum', 55.5))


# life
t.add(event('Great Oxidation Event', 2200, start=2400, end=2000, typ='life'))
t.add(event('first photosynthetic bacteria appear', 3400, typ='life'))
t.add(event('cyanobacteria begin producing oxygen', 2700, typ='life'))
t.add(event('earliest direct undisputed evidence of life', 3465, typ='life'))
t.add(event('earliest indications of life on land', 3480, typ='life'))

t.add(event('origin of life', 4025, start=3770, end=4280, typ='life'))
t.add(event('eukaryotes form', 1900, start=2100, end=1600, typ='life'))

t.add(event('endosymbiotic origin of mitochondria', 1450, typ='life'))
t.add(event('sexual reproduction appears', 1200, typ='life'))
t.add(event('earliest fungi', 1500, typ='life'))
t.add(event('algae-like plants appear', 1000, typ='life'))
t.add(event('Avalon explosion', 575, typ='life'))
t.add(event('Cambrian explosion', 541, typ='life'))
t.add(event('first vertebrates', 525, typ='life'))
t.add(event('land plants appear', 475, typ='life'))
t.add(event('vascular plants appear', 423, typ='life'))
t.add(event('first woody plants', 400, typ='life'))
t.add(event('first tetrapods evolve and venture onto land', 377.5, start=380, end=375, typ='life'))
t.add(event('first synapsids', 323, typ='life'))
t.add(event('first dinosaurs', 238.6, start=243, end=233.23, typ='life'))
t.add(event('first mammals', 200, typ='life'))
t.add(event('first flowering plants', 180, typ='life'))
t.add(event('Tyrannosaurus rex roams the Earth', 68, start=68, end=66, typ='life'))
t.add(event('Stegosaurus roams the Earth', 152.5, start=155, end=150, typ='life'))

# Humans
t.add(event('earliest primates', 52.5, start=63, end=50, typ='life'))
t.add(event('first great apes', 17.5, start=20, end=15, typ='life'))
t.add(event('first stone tools', 3.4, typ='man'))
t.add(event('anatomically modern humans', 0.5, start=0.8, end=0.3, typ='life'))
t.add(event('earliest fire use', 1.0, typ='man'))
t.add(event('earliest cooking', 2.0, start=2.3, end=1.8, typ='man'))

# extinctions
t.add(event('Ordovician–Silurian extinction events', 445, start=450, end=440, typ="extinction")) 
t.add(event('Late Devonian extinction event', 368, start=370, end=360, typ="extinction")) 
t.add(event('Permian-Triassic extinction event', 252, typ="extinction", desc="Earth's largest extinction event")) 
t.add(event('Triassic-Jurassic extinction event', 201.3, typ='extinction'))
t.add(event('Cretaceous-Paleogene (K-Pg) extinction event', 66, typ='extinction'))

# glaciations
t.add(event('Huronian glaciation (snowball Earth)', 2250, start=2400, end=2100, typ='glac'))
t.add(event('Sturtian glaciation', 698, start=717, end=680, typ='glac')) 
t.add(event('Marinoan glaciation', 642, start=650, end=635, typ='glac')) 
t.add(event('Andean-Saharan glaciation', 435, start=450, end=420, typ='glac')) 
t.add(event('Late Paleozoic icehouse (Karoo ice age)', 310, start=360, end=260, typ='glac')) 
t.add(event('Antarctic glaciation', 34, typ='glac'))
t.add(event('Last Glacial Period', .06335 , start=.115, end=.0117, typ='glac')) 





if __name__ == '__main__':
    t.print()

