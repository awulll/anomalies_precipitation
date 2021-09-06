import urllib.request as request
from bs4 import BeautifulSoup
import shapefile as sf
import shutil


# Get fields we need 
def get_fields():
    return [linha.strip() for linha in open('fields.txt','r').readlines()] 

    
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
    w = sf.Writer('shp/inventory')
    for n,table in enumerate(ests):
        if n == 0: 
            for campo in sorted(table):w.field(campo,'C','150')
        w.point(float(table['Longitude']),float(table['Latitude']))
        w.record(*(table[campo] for campo in sorted(table)))
    shutil.copy('proj/wgs84.prj','shp/inventory.prj')        
    w.close()        
    
      
create_inventory()
