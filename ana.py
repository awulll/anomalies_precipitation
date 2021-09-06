import urllib.request as request
from bs4 import BeautifulSoup



# Get fields we need 
def get_fields():
    return [linha.strip() for linha in open('fields.txt','r').readlines()] 

    
# Create ANA inventory
def create_inventory():

    # Fields target
    fields = get_fields()
    
    # Request
    url_inventory = "http://telemetriaws1.ana.gov.br/ServiceANA.asmx/HidroInventario?codEstDE=&codEstATE=&tpEst=&nmEst=&nmRio=&codSubBacia=&codBacia=&nmMunicipio=&nmEstado=Acre&sgResp=&sgOper=&telemetrica="
    proxy_handler = request.ProxyHandler({})
    opener        = request.build_opener(proxy_handler)
    req           = opener.open(url_inventory)
    data          = req.read()

    # Getting tables
    Bs_data = BeautifulSoup(data, "xml")
    tables  = Bs_data.find_all('Table')
    
    # Organizing data
    ests   = []
    for table in tables:
        ests.append({ child.name:child.text.encode().decode('unicode-escape').encode('latin1').decode('utf-8') for child in table.children if child.name in fields})
    print (ests)


      
create_inventory()


  # # <BaciaCodigo>1</BaciaCodigo>
        # # <SubBaciaCodigo>12</SubBaciaCodigo>
        # # <RioCodigo />
        # # <RioNome />
        # # <EstadoCodigo>2</EstadoCodigo>
        # # <nmEstado>ACRE</nmEstado>
        # # <MunicipioCodigo>2003000</MunicipioCodigo>
        # # <nmMunicipio>CRUZEIRO DO SUL</nmMunicipio>        
       # # <TipoEstacao>2</TipoEstacao>
        # # <Codigo>772000</Codigo>
        # # <Nome>CRUZEIRO DO SUL</Nome>
        # # <CodigoAdicional>82704</CodigoAdicional>
        # # <Latitude>-7.6111</Latitude>
        # # <Longitude>-72.6811</Longitude>
        # # <Altitude>170</Altitude>
        # # <AreaDrenagem />
        
        
                
        

    
    # for linha in str(data)[2:-1].replace('\\r','\r').replace('\\n','\n').split('\n'):# arqs.write(linha)
        # a = linha
        # print(len(a))
        # # if a[0] != '<': print (a)
        # if table != None:
            # if a == '</Table>': table = None
            # else: 
                # a = a.split('<')
                # if len(a) == 3:  campo = a[1].split('>')[0].strip()    ;   valor = a[1].split('>')[1].strip()
                # else:            campo = a[1].split('>')[0].strip()[:-2] ; valor = a[1].split('>')[1].strip()
                # ests[table][campo] = valor      
        # if a.__contains__('<Table diffgr:id='): table = a.split('"')[1] ; ests[table] = {}
    
    # print (ests) 
    # # Creating shapefile 
    # w = sf.Writer('inventario_telemetricas')
    # for n,table in enumerate(sorted(ests)):
        # if n == 0: 
            # for campo in sorted(ests[table]):w.field(campo,'C','150')
        # w.point(float(ests[table]['Longitude']),float(ests[table]['Latitude']))
        # w.record(*(ests[table][campo] for campo in sorted(ests[table])))
    # shutil.copy('projecao/wgs84.prj','inventario_telemetricas.prj')        
    # w.close()        
    
    

















# from datetime import *
# import os
# import xml.etree.ElementTree as ET



# from xml.dom import minidom

# # import xml.etree.ElementTree as ET
# # tree = ET.parse('xml.xml')
# # root = tree.getroot()

# # # one specific item attribute
# # print('Item #2 attribute:')
# # print(root[0].attrib)

# # # all item attributes
# # print('\nAll attributes:')
# # for elem in root:
    # # print (elem)
    # # for subelem in elem:
        # # print(subelem.attrib)

# # # one specific item's data
# # print('\nItem #2 data:')
# # print(root[0].text)

# # # all items data
# # print('\nAll item data:')
# # for elem in root:
    # # for subelem in elem:
        # # print(subelem.text)


# from bs4 import BeautifulSoup
 
 
# # Reading the data inside the xml
# # file to a variable under the name
# # data
# with open('xml.xml', 'r') as f:
    # data = f.read()
 
# # Passing the stored data inside
# # the beautifulsoup parser, storing
# # the returned object
# Bs_data = BeautifulSoup(data, "xml")
 
# # Finding all instances of tag
# # `unique`
# tables = Bs_data.find_all('Table')

# ests  = {}
# campos = [] ; cc = []
# for table in tables:
    # # print (table['id'])
    # # for aa in dir(table): print (aa)
    # # aasd
    # for child in table.children:
        # if child.name != None:
            # print (child.name,'valor:',child.text.encode().decode('unicode-escape').encode('latin1').decode('utf-8'))
            # if campos == []: cc.append(child.name)
    # if campos == []: campos = cc
                
        # # for a in dir(child): print (a)
    # asd
# # # Using find() to extract attributes
# # # of the first instance of the tag
# # b_name = Bs_data.find('child', {'name':'Codigo'})
 
# # print(b_name)
 
# # # Extracting the data stored in a
# # # specific attribute of the
# # # `child` tag
# # # value = b_name.get('test')
 
# # print(value)


# # # parse an xml file by name
# # mydoc = minidom.parse('xml.xml')

# # items = mydoc.getElementsByTagName('Table')

# # for item in items:
    # # # for it in item.iter():
        # # # print (it)
    # # a = 1
    # # print (item.get_tagName())    
    # # for node in item.childNodes:
        # # print (node)
        # # print (node.wholeText)
        # # print (a)
        # # a = a + 1
        # # # for a in dir(node): print (a)
  
# # asd        
    # # # for a in dir(item):
        # # print (a)
    # # asd        
    # # print (item.getElementsByTagName('Codigo'))

# # # one specific item attribute
# # print('Item #2 attribute:')
# # print(items[1])#.#attributes['Codigo'].value)
# # print(items[1].attributes['Codigo'].value)

# # # all item attributes
# # print('\nAll attributes:')
# # for elem in items:
    # # print(elem.attributes['Codigo'].value)

# # # one specific item's data
# # print('\nItem #2 data:')
# # print(items[1].firstChild.data)
# # print(items[1].childNodes[0].data)

# # # all items data
# # print('\nAll item data:')
# # for elem in items:
    # # print(elem.firstChild.data)

# asd

asd
def copy_inventory(diret):

    for arq in os.listdir('telemetricas/consolidado/shapes'):
        if 'consolidado_telemetricas.' in arq: shutil.copy('telemetricas/consolidado/shapes/'+arq,'%s/shapes/inventario_telemetricas.%s' % (diret,arq[-3:]))




def download_station(station,begin,end=datetime(3000,1,1)):

    # Requisição
    url_inventory = "http://telemetriaws1.ana.gov.br/ServiceANA.asmx/DadosHidrometeorologicos?codEstacao=%s&dataInicio=%s&dataFim=%s" % (station,'%.2i/%.2i/%.4i' % (begin.day,begin.month,begin.year),'%.2i/%.2i/%.4i' % (end.day,end.month,end.year))
    proxy_handler = request.ProxyHandler({})
    opener        = request.build_opener(proxy_handler)
    req           = opener.open(url_inventory)
    data          = str(req.read())[2:-1].replace('\\r','').split('\\n')
    
    # Gerando dados para criação de arquivo de saida
    status = False
    vals  = {}
    for linha in data:
        a = linha.strip()
        if status != False:
            if a == '</DadosHidrometereologicos>': status = False
            else: 
                a = a.split('<')
                if len(a) == 3:  field = a[1].split('>')[0].strip()    ;   value = a[1].split('>')[1].strip()
                else:            field = a[1].split('>')[0].strip()[:-2] ; value = a[1].split('>')[1].strip()
                if field == 'DataHora': 
                    dat = datetime.strptime(value,'%Y-%m-%d %H:%M:%S')
                    try:    vals[dat]
                    except: vals[dat] = {v:'' for v in VARIABLES}
                if field in VARIABLES: vals[dat][field] = value
        if a.__contains__('<DadosHidrometereologicos diffgr:id='): status = True  
    return vals
    
def parse_rcrd(filename):
    stack = []

    for event, elem in ET.iterparse(filename, events=('start','end')):
        
        if event == 'start':
            if elem.tag == 'DadosHidrometereologicos':
                record = {
                    'DataHora': '',
                    'Vazao': '',
                    'Nivel': '',
                    'Chuva': ''
                }    
            elif elem.tag in ['DataHora','Vazao','Nivel','Chuva'] and stack[-1] in ['DadosHidrometereologicos']: record[elem.tag] = elem.text
            stack.append(elem.tag)
        elif event == 'end':
            if elem.tag == 'DadosHidrometereologicos':
                yield record

            stack.pop()    


def download_and_save_station2(path,station,begin=datetime(1500,1,1),end=datetime(3000,1,1),fields = ['Vazao','Nivel','Chuva']):

    erro = False
    # Request
    tempo1 = datetime.now()
    url_inventory = "http://telemetriaws1.ana.gov.br/ServiceANA.asmx/DadosHidrometeorologicos?codEstacao=%s&dataInicio=%s&dataFim=%s" % (station,'%.2i/%.2i/%.4i' % (begin.day,begin.month,begin.year),'%.2i/%.2i/%.4i' % (end.day,end.month,end.year))
    try:    proxy_handler = request.ProxyHandler({})
    except: erro          = True 
    try:    opener = request.build_opener(proxy_handler)
    except: erro   = True
    try:    req  = opener.open(url_inventory)
    except: erro = True
    tempo4 = datetime.now()
    print (tempo4-tempo1,'request')
    
    if erro == False:    
        files  = {field:open('%s.txt' % (field.lower()),'w') for field in fields}
        dados = []
        for rcrd in parse_rcrd(req):
            if rcrd['DataHora'] != None:
                for field in fields:
                    if rcrd[field] != None: files[field].write('%s\t%s\n' % (rcrd['DataHora'].strip(),rcrd[field].strip()))
        for f in files: files[f].close()
        tempo5 = datetime.now()
        print (tempo5-tempo4,'download and save')
    else: print ('error in station ',station)        

    
    
def download_and_save_station(path,station,begin=datetime(1500,1,1),end=datetime(3000,1,1)):

    erro = False
    # Request
    tempo1 = datetime.now()
    url_inventory = "http://telemetriaws1.ana.gov.br/ServiceANA.asmx/DadosHidrometeorologicos?codEstacao=%s&dataInicio=%s&dataFim=%s" % (station,'%.2i/%.2i/%.4i' % (begin.day,begin.month,begin.year),'%.2i/%.2i/%.4i' % (end.day,end.month,end.year))
    try:    proxy_handler = request.ProxyHandler({})
    except: erro          = True 
    try:    opener = request.build_opener(proxy_handler)
    except: erro   = True
    try:    req  = opener.open(url_inventory)
    except: erro = True
    tempo4 = datetime.now()
    print (tempo4-tempo1,'request')
    
    if erro == False:    
        data          = str(req.read())[2:-1].replace('\\r','').split('\\n')
        # Reading data and creating output files
        status = False
        try:    os.mkdir('%s/%s' % (path,station))
        except: pass
        files = {field.lower():open('%s/%s/%s.txt' % (path,station,field.lower()),'w') for field in VARIABLES}
        for line in data:
            a = line.strip()
            if status != False:
                if a == '</DadosHidrometereologicos>': status = False
                else: 
                    a = a.split('<')
                    if len(a) == 3:  field = a[1].split('>')[0].strip()    ;   value = a[1].split('>')[1].strip()
                    else:            field = a[1].split('>')[0].strip()[:-2] ; value = a[1].split('>')[1].strip()
                    if value != '':
                        if field == 'DataHora': dat = datetime.strptime(value,'%Y-%m-%d %H:%M:%S')
                        if field in VARIABLES: files[field.lower()].write('%.2i/%.2i/%.4i %.2i:%.2i\t%s\n' % (dat.day,dat.month,dat.year,dat.hour,dat.minute,value))
            if a.__contains__('<DadosHidrometereologicos diffgr:id='): status = True
        
        for f in files:
            files[f].close()
            a = '%s/%s/%s.txt' % (path,station,f)
            if os.path.getsize(a) == 0: os.remove(a)  
        tempo5 = datetime.now()
        print (tempo5-tempo4,'download and save')
    else: print ('error in station ',station)        


def create_dirs(path):

    try:    os.mkdir(path)
    except: pass
    try:    os.mkdir(path+'/shapes')
    except: pass
    try:    os.mkdir(path+'/dados')
    except: pass

def printing(text,ident=0):
    t = ''
    if ident != 0:
        for i in range(ident*4): t = t + ' '
    print(t+text)            
        

# Update mensal
def update_monthly(create_inv=False,copy_inv=False,dataini=datetime(1900,1,1)):
    
    # Download Inventory
    now  = datetime.now()
    path = DIRBASE+'%.4i-%.2i' % (now.year,now.month)
    create_dirs(path)
    if create_inv == True: printing(' - Getting inventory') ; create_inventory(path) ; printing(' - Inventory created successfully')
    if copy_inv   == True: printing(' - Copying inventory') ; copy_inventory(path) ; printing(' - Inventory copied successfully')
    
    # Reading Inventory
    printing(' - Reading inventory')
    s    = sf.Reader(path+'/shapes/inventario_telemetricas')
    i_cd = [n for n,f in enumerate(s.fields) if f[0] == 'Codigo'][0]-1
    i_ca = [n for n,f in enumerate(s.fields) if f[0] == 'CodigoAdic'][0]-1
    printing(' - Inventory read successfully')
    
    # Getting all
    ests = []
    for r in s.records():
        if int(r[i_cd]) < 10: ests.append(r[i_ca])
        else:                 ests.append(r[i_cd])    
    for n,est in enumerate(ests):
        print ('telemétricas    %.3f%% %s' % (100*n/len(ests),est),len(ests))
        download_and_save_station(path+'/dados',est,dataini)        
    
    
# Update mensal
def continue_update_monthly(dataini=datetime(1900,1,1),parte=0):
        
    # Reading Inventory    
    now  = datetime.now()
    path = DIRBASE+'%.4i-%.2i' % (now.year,now.month)
    printing(' - Reading inventory')
    s    = sf.Reader(path+'/shapes/inventario_telemetricas')
    i_cd = [n for n,f in enumerate(s.fields) if f[0] == 'Codigo'][0]-1
    i_ca = [n for n,f in enumerate(s.fields) if f[0] == 'CodigoAdic'][0]-1

    printing(' - Inventory read successfully')

    # Getting all
    ests = []
    for r in s.records():
            if int(r[i_cd]) < 10: ests.append(r[i_ca])
            else:                 ests.append(r[i_cd])
    ests = sorted(ests)
    if parte == 0: pass
    if parte == 1: ests = ests[:1*int(len(ests)/4)]        
    if parte == 2: ests = ests[1*int(len(ests)/4):2*int(len(ests)/4)]        
    if parte == 3: ests = ests[2*int(len(ests)/4):3*int(len(ests)/4)]        
    if parte == 4: ests = ests[3*int(len(ests)/4):]        
            
    for n,est in enumerate(ests):
        print ('telemétricas %i    %.3f%% %s' % (parte,100*n/len(ests),est))
        if os.path.isdir('%s/dados/%s' % (path,est)) == False: download_and_save_station(path+'/dados',est,dataini)            

 
#update_monthly(create_inv,copy_inv,datetime(2019,1,1))
# continue_update_monthly(datetime(2020,1,1),3)
# download_station(station,begin,end=datetime(3000,1,1))

# now  = datetime.now()
# estt = ['86305000','86300000','86298000','86110000','86118000','86162000','86163000','86250000','86296000']
# for est in estt: 

for i in range(1):
    tempo1 = datetime.now()
    download_and_save_station2('.','56994510',begin=datetime(2000,1,1),end=datetime(2021,3,1))
    tempo2 = datetime.now()
    download_and_save_station( '.','56994510',begin=datetime(2000,1,1),end=datetime(2021,3,1))
    tempo3 = datetime.now()
    
    print (tempo2-tempo1,'novo')
    print (tempo3-tempo2,'antigo')


# import urllib.request as request
# import xml.dom.minidom
# import shutil
# import shapefile as sf
# from datetime import *
# import os

# DIRBASE   = 'telemetricas/'
# DATATYPE  = {1:'Cota',2:'Chuva',3:'Vazao'}
# VARIABLES = [DATATYPE[i] for i in DATATYPE]
# create_inv = False
# copy_inv   = True


# def download_and_save_station(path,station,begin=datetime(1500,1,1),end=datetime(3000,1,1)):

    # erro = False
    # # Request
    # tempo1 = datetime.now()
    # url_inventory = "http://telemetriaws1.ana.gov.br/ServiceANA.asmx/DadosHidrometeorologicos?codEstacao=%s&dataInicio=%s&dataFim=%s" % (station,'%.2i/%.2i/%.4i' % (begin.day,begin.month,begin.year),'%.2i/%.2i/%.4i' % (end.day,end.month,end.year))
    # try: proxy_handler = request.ProxyHandler({})
    # except: erro = True
    # if erro == True: print (1) 
    # tempo2 = datetime.now()
    # print (tempo2-tempo1)
    # try: opener        = request.build_opener(proxy_handler)
    # except: erro = True
    # if erro == True: print (2) 
    # tempo3 = datetime.now()
    # print (tempo3-tempo2)
    # try: req           = opener.open(url_inventory)
    # except: erro = True
    # if erro == True: print (3) 
    # tempo4 = datetime.now()
    # print (tempo4-tempo3)
    
    
    # if erro == False:    
        # data          = str(req.read())[2:-1].replace('\\r','').split('\\n')
        # # Reading data and creating output files
        # status = False
        # try:    os.mkdir('%s/%s' % (path,station))
        # except: pass
        # files = {field.lower():open('%s/%s/%s.txt' % (path,station,field.lower()),'w') for field in VARIABLES}
        # for line in data:
            # a = line.strip()
            # if status != False:
                # if a == '</DadosHidrometereologicos>': status = False
                # else: 
                    # a = a.split('<')
                    # if len(a) == 3:  field = a[1].split('>')[0].strip()    ;   value = a[1].split('>')[1].strip()
                    # else:            field = a[1].split('>')[0].strip()[:-2] ; value = a[1].split('>')[1].strip()
                    # if value != '':
                        # if field == 'DataHora': dat = datetime.strptime(value,'%Y-%m-%d %H:%M:%S')
                        # if field in VARIABLES: files[field.lower()].write('%.2i/%.2i/%.4i %.2i:%.2i\t%s\n' % (dat.day,dat.month,dat.year,dat.hour,dat.minute,value))
            # if a.__contains__('<DadosHidrometereologicos diffgr:id='): status = True
        # tempo5 = datetime.now()
        # print (tempo5-tempo4)      
        # for f in files:
            # files[f].close()
            # a = '%s/%s/%s.txt' % (path,station,f)
        # if os.path.getsize(a) == 0: os.remove(a)  
    # else: print ('error in station ',station)        


# path = './'
# station = '56994510' 
# download_and_save_station(path,station,begin=datetime(1500,1,1),end=datetime(3000,1,1))


# DIRBASE   = 'telemetricas/'
# DATATYPE  = {1:'Nivel',2:'Chuva',3:'Vazao'}
# VARIABLES = [DATATYPE[i] for i in DATATYPE]
# create_inv = False
# copy_inv   = True
