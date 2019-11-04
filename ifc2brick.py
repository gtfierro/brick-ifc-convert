from rdflib import Graph, Namespace, URIRef, Literal
from collections import defaultdict
import ifcopenshell
import coloredlogs, logging
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', fmt='%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s')

RDF = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = Namespace('http://www.w3.org/2000/01/rdf-schema#')
OWL = Namespace('http://www.w3.org/2002/07/owl#')
BRICK = Namespace('http://brickschema.org/schema/1.1.0/Brick#')

def parseid(s):
    if isinstance(s, str):
        s = s.replace('#','')
    return int(s)
def fixname(n):
    if n is None:
        return ''
    return n.replace(' ','_')


class Generator(object):
    def __init__(self, G, cfg):
        self.G = G
        self.G.bind('brick', BRICK)
        self.G.bind('rdf', RDF)
        self.G.bind('owl', OWL)
        self.G.bind('rdfs', RDFS)
        ifc =  ifcopenshell.open(cfg['ifc_file'])

        BLDG = Namespace(cfg['building_namespace'])

        # zones
        zones = {}
        logging.info("Read HVAC zones")
        for zone in ifc.by_type('IfcZone'):
            zones[parseid(zone.id())] = zone


        # get groups
        logging.info("Read rooms, map to HVAC zones")
        zone2rooms = defaultdict(list)
        for group in ifc.by_type('IfcRelAssignsToGroup'):
            zoneid = parseid(group.RelatingGroup.id())
            zone = zones.get(zoneid)
            if zone is None:
                logging.warning("No zone found for group")
                continue
            things = group.RelatedObjects
            for thing in things:
                if thing.is_a('IfcSpace'):
                    zone2rooms[zoneid].append(thing.LongName + thing.Name)

        floors = {}
        logging.info("Read floors")
        for group in ifc.by_type('IfcBuildingStorey'):
            floorid = parseid(group.id())
            floors[floorid] = group.LongName

        logging.info("Read rooms")
        rooms = []
        rooms2floors = defaultdict(list)
        for group in ifc.by_type('IfcRelAggregates'):
            rel_obj = group.RelatingObject
            if rel_obj.is_a('IfcBuildingStorey'):
                for o in group.RelatedObjects:
                    room_name = o.LongName + o.Name
                    rooms.append(room_name)
                    rooms2floors[rel_obj.LongName].append(room_name)

        for rm in rooms:
            rm = fixname(rm)
            G.add((BLDG[rm], RDF.type, BRICK.Room))
        for floor in floors.values():
            floor = fixname(floor)
            G.add((BLDG[floor], RDF.type, BRICK.Floor))
        for floor, roomlist in rooms2floors.items():
            floor = fixname(floor)
            for room in roomlist:
                room = fixname(room)
                G.add((BLDG[floor], BRICK.hasPart, BLDG[room]))
        for zone, roomlist in zone2rooms.items():
            zone = fixname(str(zone))
            G.add((BLDG[zone], RDF.type, BRICK.HVAC_ZONE))
            for room in roomlist:
                room = fixname(room)
                G.add((BLDG[room], BRICK.isPartOf, BLDG[zone]))

            
if __name__ == '__main__':
    import sys
    G = Graph()

    cfg = {
        'ifc_file': sys.argv[1],
        'building_namespace': 'http://example.com/mybuilding#',
    }

    gen = Generator(G, cfg)

    with open('output.ttl','wb') as f:
        f.write(G.serialize(format='ttl'))

