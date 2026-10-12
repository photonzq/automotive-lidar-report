import json, sys
sys.stdout.reconfigure(encoding='utf-8')
from fetchq import fetch
queries = {
 'lidar': "contenttype='project' AND 'lidar'",
 'ladar': "contenttype='project' AND ('ladar' OR 'laser radar')",
 'fmcw': "contenttype='project' AND 'FMCW'",
 'freqmodcw': "contenttype='project' AND 'frequency modulated continuous wave'",
 'opa': "contenttype='project' AND 'optical phased array'",
 'opas': "contenttype='project' AND 'optical phased arrays'",
 'spad': "contenttype='project' AND 'SPAD'",
 'spads': "contenttype='project' AND 'SPADs'",
 'spadlong': "contenttype='project' AND 'single photon avalanche'",
 'laserranging': "contenttype='project' AND 'laser ranging'",
 'microcomb': "contenttype='project' AND 'microcomb'",
 'microcombs': "contenttype='project' AND 'microcombs'",
 'combranging': "contenttype='project' AND 'frequency comb' AND 'ranging'",
 'combdistance': "contenttype='project' AND 'comb' AND 'distance measurement'",
 'tof': "contenttype='project' AND 'time of flight' AND ('depth' OR 'ranging' OR '3D imaging' OR 'distance' OR 'camera')",
 'tof2': "contenttype='project' AND 'ToF' AND ('depth' OR 'ranging' OR '3D' OR 'camera' OR 'sensor')",
 'beamsteer': "contenttype='project' AND 'beam steering' AND ('optical' OR 'laser' OR 'photonic')",
 'depthsensing': "contenttype='project' AND 'depth sensing'",
 '3dsensing': "contenttype='project' AND '3D sensing'",
 '3dimaging': "contenttype='project' AND '3D imaging' AND 'laser'",
 'optranging': "contenttype='project' AND 'optical ranging'",
 'ranging': "contenttype='project' AND 'ranging' AND ('photonic' OR 'laser' OR 'optical')",
 'distlaser': "contenttype='project' AND 'distance measurement' AND 'laser'",
 'depthcam': "contenttype='project' AND ('depth camera' OR '3D camera')",
 'autolaser': "contenttype='project' AND 'autonomous' AND 'laser' AND ('vehicle' OR 'vehicles' OR 'driving') AND ('sensor' OR 'sensing')",
}
allp = {}
src = {}
for tag, q in queries.items():
    try:
        hits, tot = fetch(q, tag)
    except Exception as e:
        print('ERR', tag, e); continue
    print(tag, tot, len(hits))
    for x in hits:
        p = x.get('project', x)
        allp[p['id']] = p
        src.setdefault(p['id'], []).append(tag)
json.dump(allp, open('union.json','w',encoding='utf-8'))
json.dump(src, open('union_src.json','w',encoding='utf-8'))
print('UNION', len(allp))
