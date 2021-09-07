import urllib.request as request
from bs4 import BeautifulSoup
import shapefile as sf
import shutil
from datetime import *
import os
import calendar
import shapely.geometry as sg

# Parameters
DATAAUT = {2:'Chuva'}
DATACON = {1:'Cota' ,2:'Chuva',3:'Vazao'}


# Get fields we need 
def get_fields():
    return [linha.strip() for linha in open('input/fields.txt','r').readlines()] 

    
# Create ANA inventory
def create_inventory():

    # Fields target
    fields = get_fields()
    
    # Request
    url_inventory = "http://telemetriaws1.ana.gov.br/ServiceANA.asmx/HidroInventario?codEstDE=&codEstATE=&tpEst=&nmEst=&nmRio=&codSubBacia=&codBacia=&nmMunicipio=&nmEstado=&sgResp=&sgOper=&telemetrica="
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

    # Creating shapefile 
    w = sf.Writer('data/shp/inventory')
    for n,table in enumerate(ests):
        if n == 0: 
            for campo in sorted(table):w.field(campo,'C','150')
        w.point(float(table['Longitude']),float(table['Latitude']))
        w.record(*(table[campo] for campo in sorted(table)))
    shutil.copy('proj/wgs84.prj','data/shp/inventory.prj')        
    w.close()        
    

# Create path if not exists    
def create_path(path,station,tm):
    '''Input:  path: string
               station: string
               tm: datetime 
       Output: False, if ok
               True, if error
'''               
    error = False
    try:    os.mkdir('%s/%s' % (path,station))
    except: 
        if os.path.exists('%s/%s' % (path,station)) == False: error = True

    if error: print (datetime.now()-tm,'error creating path','%s/%s' % (path,station))
    return error

# Get tables from xml request
def get_tables_xml(error,req,table,tm):
    '''Input:  error: boolean
               req: xml request
               table: string for table you want
               tm: datetime 
       Output: tables: tables from BeautifulSoup

'''              
    if error: return None 
    
    try: 
        Bs_data = BeautifulSoup(req.read(), "xml")
        tables  = Bs_data.find_all(table)
    except: 
        print (datetime.now()-tm,'error reading xml data')
        return None
    return tables
    
# Download and sabe station     
def download_and_save_station(path,station,begin=datetime(1900,1,1),end=datetime(3000,1,1),variable=1,prints=False):
    '''
Input:
  path:     string
  station:  string
  being:    datetime
  end:      datetime
  variable: 1 -> water level
            2 -> rainfall
            3 -> flow
  prints:   boolean          
'''

    # Verify if it is a automatic or a conventional station    
    if 'automatic' in path: 
        url_inventory = "http://telemetriaws1.ana.gov.br/ServiceANA.asmx/DadosHidrometeorologicos?codEstacao=%s&dataInicio=%s&dataFim=%s"                            % (station,'%.2i/%.2i/%.4i' % (begin.day,begin.month,begin.year),'%.2i/%.2i/%.4i' % (end.day,end.month,end.year))  
        tablename = 'DadosHidrometereologicos'
        vrs = [DATAAUT[i] for i in DATAAUT] + ['DataHora']
    else:                   
        url_inventory = "http://telemetriaws1.ana.gov.br/ServiceANA.asmx/HidroSerieHistorica?codEstacao=%s&dataInicio=%s&dataFim=%s&tipoDados=%i&nivelConsistencia=" % (station,'%.2i/%.2i/%.4i' % (begin.day,begin.month,begin.year),'%.2i/%.2i/%.4i' % (end.day,end.month,end.year),variable)
        tablename = 'SerieHistorica' 
        vrs = [DATACON[variable],'DataHora']
    
    error = False
    time1 = datetime.now()
    try:    
        proxy_handler = request.ProxyHandler({})
        opener        = request.build_opener(proxy_handler)
        req           = opener.open(url_inventory)
    except: error = True
    
    time2 = datetime.now()
    if prints:print (time2-time1,'request')
    
    if error == False:    
        
        # Create path if not exists
        error  = create_path(path,station,time2)
        tables = get_tables_xml(error,req,tablename,time2)
        
        if tables != None:
            
            # Organizing data
            if 'automatic' in path:
                files = {}
                for table in tables:
                    for child in table.children:
                        if child.name in vrs:
                            if child.name == 'DataHora': dat = datetime.strptime(child.text.strip(),'%Y-%m-%d %H:%M:%S')
                            else: 
                                if child.name.lower() not in files: files[child.name.lower()] = open('%s/%s/%s.txt' % (path,station,child.name.lower()),'w')                        
                                files[child.name.lower()].write('%.2i/%.2i/%.4i %.2i:%.2i\t%s\n' % (dat.day,dat.month,dat.year,dat.hour,dat.minute,child.text))
                # Closing files
                for f in files: files[f].close()
                time3 = datetime.now()
                if prints:print (time3-time2,'download and save')
            else: 
                out = None
                for table in tables:
                    for child in table.children:                        
                        if child.name == 'DataHora':          dat  = datetime.strptime(child.text.strip(),'%Y-%m-%d %H:%M:%S')
                        if child.name == 'NivelConsistencia': cons = child.text
                        if child.name != None and vrs[0] == child.name[:-2]:
                            day = int(child.name.strip()[-2:])         
                            if day < 1 or day > calendar.monthrange(dat.year,dat.month)[1]: pass# if prints: print ('  datetime error',station,day,dat)
                            else: 
                                if out == None: out = open('%s/%s/%s.txt' % (path,station,vrs[0].lower()),'w')
                                out.write('%s/%.2i/%.4i %.2i:%.2i\t%s\t%s\n' % (day,dat.month,dat.year,dat.hour,dat.minute,child.text,cons))
                # Closing file
                if out != None: out.close()
                time3 = datetime.now()
                if prints:print (time3-time2,'download and save')
                
    else: 
        if prints:print ('error in station:',station)
        
        
        
# Download data for a shapefile input 
def download_data_shapefile(shp_input,period=None,create_inv=False):

    # Create object Polygon for input shapefile 
    pol = sg.Polygon(sf.Reader(shp_input).shapes()[0].points)

    # Download Inventory or not
    if create_inv == True: print('Getting inventory') ; create_inventory() ; print('Inventory created successfully')
        
    # Reading Inventory
    print('Reading inventory')
    inv  = sf.Reader('data/shp/inventory')
    i_cd = [n for n,f in enumerate(inv.fields) if f[0] == 'Codigo'][0]-1
    i_la = [n for n,f in enumerate(inv.fields) if f[0] == 'Latitude'][0]-1
    i_lo = [n for n,f in enumerate(inv.fields) if f[0] == 'Longitude'][0]-1
    i_st = [n for n,f in enumerate(inv.fields) if f[0] == 'nmEstado'][0]-1
    
    
    # Getting all
    print('Getting station codes inside polygon')
    stations = []
    for r in inv.records():
        if pol.contains(sg.Point(float(r[i_lo]),float(r[i_la]))): stations.append(r[i_cd])
      
    print ('Getting records')            
    for n,station in enumerate(sorted(stations)):
        print ('station   %.3f%%: %s' % (100*n/len(stations),station), end='\r')
        if period != None:
            download_and_save_station('data/automatic',   station,begin=period[0],end=period[1])
            download_and_save_station('data/conventional',station,begin=period[0],end=period[1],variable=2)
        else:         
            download_and_save_station('data/automatic',   station)
            download_and_save_station('data/conventional',station,variable=2)     
            
        
        
# For create a new inventory
#create_inventory()

# For download data for Paraná State
#download_data_shapefile('input/shp/parana_wgs84',period=[datetime(1970,1,1),datetime(2021,12,31)])

    
      
