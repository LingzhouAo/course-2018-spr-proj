import urllib.request
import json
import dml
import prov.model
import datetime
import uuid

class getdata(dml.Algorithm):
    contributor = 'aolzh'
    reads = []
    writes = ['aolzh.NewYorkSchool', 'aolzh.NewYorkCrime', 'aolzh.NewYorkSubway', 'aolzh.NewYorkLibrary', 'aolzh.NewYorkHospitals']

    @staticmethod
    def execute(trial = False):
        '''Retrieve some data sets (not using the API here for the sake of simplicity).'''
        startTime = datetime.datetime.now()

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('aolzh', 'aolzh')

        url = 'https://data.cityofnewyork.us/resource/8pnn-kkif.json'
        response = urllib.request.urlopen(url).read().decode("utf-8")
        r = json.loads(response)
        s = json.dumps(r, sort_keys=True, indent=2)
        repo.dropCollection("NewYorkSchool")
        repo.createCollection("NewYorkSchool")
        repo['aolzh.NewYorkSchool'].insert_many(r)
        print("NewYorkSchool Finished")

        url = 'https://data.cityofnewyork.us/resource/qgea-i56i.json'
        response = urllib.request.urlopen(url).read().decode("utf-8")
        r = json.loads(response)
        s = json.dumps(r, sort_keys=True, indent=2)
        repo.dropCollection("NewYorkCrime")
        repo.createCollection("NewYorkCrime")
        repo['aolzh.NewYorkCrime'].insert_many(r)
        print("NewYorkCrime Finished")

        url = 'https://data.cityofnewyork.us/resource/kk4q-3rt2.json'
        response = urllib.request.urlopen(url).read().decode("utf-8")
        r = json.loads(response)
        s = json.dumps(r, sort_keys=True, indent=2)
        repo.dropCollection("NewYorkSubway")
        repo.createCollection("NewYorkSubway")
        repo['aolzh.NewYorkSubway'].insert_many(r)
        print("NewYorkSubway Finished")

        url = 'https://data.cityofnewyork.us/resource/feuq-due4.json'
        response = urllib.request.urlopen(url).read().decode("utf-8")
        r = json.loads(response)
        s = json.dumps(r, sort_keys=True, indent=2)
        repo.dropCollection("NewYorkLibrary")
        repo.createCollection("NewYorkLibrary")
        repo['aolzh.NewYorkLibrary'].insert_many(r)
        print("NewYorkLibrary Finished")

        url = 'https://data.cityofnewyork.us/resource/ymhw-9cz9.json'
        response = urllib.request.urlopen(url).read().decode("utf-8")
        r = json.loads(response)
        s = json.dumps(r, sort_keys=True, indent=2)
        repo.dropCollection("NewYorkHospitals")
        repo.createCollection("NewYorkHospitals")
        repo['aolzh.NewYorkHospitals'].insert_many(r)
        print("NewYorkHospitals Finished")

        repo.logout()

        endTime = datetime.datetime.now()

        return {"start":startTime, "end":endTime}
    
    @staticmethod
    def provenance(doc = prov.model.ProvDocument(), startTime = None, endTime = None):
        '''
            Create the provenance document describing everything happening
            in this script. Each run of the script will generate a new
            document describing that invocation event.
            '''

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('aolzh', 'aolzh')
        doc.add_namespace('alg', 'http://datamechanics.io/algorithm/') # The scripts are in <folder>#<filename> format.
        doc.add_namespace('dat', 'http://datamechanics.io/data/') # The data sets are in <user>#<collection> format.
        doc.add_namespace('ont', 'http://datamechanics.io/ontology#') # 'Extension', 'DataResource', 'DataSet', 'Retrieval', 'Query', or 'Computation'.
        doc.add_namespace('log', 'http://datamechanics.io/log/') # The event log.
        doc.add_namespace('nyc', 'https://data.cityofnewyork.us/resource/')

        getdata_script = doc.agent('alg:aolzh#getdata', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})

        newyorkschool_resource = doc.entity('nyc:8pnn-kkif', {'prov:label':'NewYork Schools', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        newyorkcrime_resource = doc.entity('nyc:qgea-i56i', {'prov:label':'NewYork Crime', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        newyorksubway_resource = doc.entity('nyc:kk4q-3rt2', {'prov:label':'NewYork Subway', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        newyorklibrary_resource = doc.entity('nyc:feuq-due4', {'prov:label':'NewYork Library', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        newyorkhospitals_resource = doc.entity('nyc:ymhw-9cz9', {'prov:label':'NewYork Hospitals', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})

        get_newyorkschool = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        get_newyorkcrime = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        get_newyorksubway = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        get_newyorklibrary = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        get_newyorkhospitals = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)

        doc.wasAssociatedWith(get_newyorkschool, getdata_script)
        doc.wasAssociatedWith(get_newyorkcrime, getdata_script)
        doc.wasAssociatedWith(get_newyorksubway, getdata_script)
        doc.wasAssociatedWith(get_newyorklibrary, getdata_script)
        doc.wasAssociatedWith(get_newyorkhospitals, getdata_script)

        doc.usage(get_newyorkschool, newyorkschool_resource, startTime, None,
                  {prov.model.PROV_TYPE:'ont:Retrieval'
                  }
                  )

        doc.usage(get_newyorkcrime, newyorkcrime_resource, startTime, None,
                  {prov.model.PROV_TYPE:'ont:Retrieval'
                  }
                  )
        doc.usage(get_newyorksubway, newyorksubway_resource, startTime, None,
                  {prov.model.PROV_TYPE:'ont:Retrieval'
                  }
                  )
        doc.usage(get_newyorklibrary, newyorklibrary_resource, startTime, None,
                  {prov.model.PROV_TYPE:'ont:Retrieval'
                  }
                  )
        doc.usage(get_newyorkhospitals, newyorkhospitals_resource, startTime, None,
                  {prov.model.PROV_TYPE:'ont:Retrieval'
                  }
                  )


        newyorkschool = doc.entity('dat:aolzh#NewYorkSchool', {prov.model.PROV_LABEL:'NewYork Schools', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(newyorkschool, getdata_script)
        doc.wasGeneratedBy(newyorkschool, get_newyorkschool, endTime)
        doc.wasDerivedFrom(newyorkschool, newyorkschool_resource, get_newyorkschool, get_newyorkschool, get_newyorkschool)

        newyorkcrime = doc.entity('dat:aolzh#NewYorkCrime', {prov.model.PROV_LABEL:'NewYork Crime', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(newyorkcrime, getdata_script)
        doc.wasGeneratedBy(newyorkcrime, get_newyorkcrime, endTime)
        doc.wasDerivedFrom(newyorkcrime, newyorkcrime_resource, get_newyorkcrime, get_newyorkcrime, get_newyorkcrime)

        newyorksubway = doc.entity('dat:aolzh#NewYorkSubway', {prov.model.PROV_LABEL:'NewYork Subway', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(newyorksubway, getdata_script)
        doc.wasGeneratedBy(newyorksubway, get_newyorksubway, endTime)
        doc.wasDerivedFrom(newyorksubway, newyorksubway_resource, get_newyorksubway, get_newyorksubway, get_newyorksubway)

        newyorklibrary = doc.entity('dat:aolzh#NewYorkLibrary', {prov.model.PROV_LABEL:'Newyork Library', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(newyorklibrary, getdata_script)
        doc.wasGeneratedBy(newyorklibrary, get_newyorklibrary, endTime)
        doc.wasDerivedFrom(newyorklibrary, newyorklibrary_resource, get_newyorklibrary, get_newyorklibrary, get_newyorklibrary)

        newyorkhospitals = doc.entity('dat:aolzh#NewYorkHospitals', {prov.model.PROV_LABEL:'NewYork Hospitals', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(newyorkhospitals, getdata_script)
        doc.wasGeneratedBy(newyorkhospitals, get_newyorkhospitals, endTime)
        doc.wasDerivedFrom(newyorkhospitals, newyorkhospitals_resource, get_newyorkhospitals, get_newyorkhospitals, get_newyorkhospitals)

        repo.logout()
                  
        return doc

getdata.execute()
doc = getdata.provenance()
print(doc.get_provn())
print(json.dumps(json.loads(doc.serialize()), indent=4))

## eof