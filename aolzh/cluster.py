import urllib.request
import json
import dml
import prov.model
import datetime
import uuid
import scipy.stats
import random
from sklearn.cluster import KMeans
from sklearn import preprocessing
import numpy as np
from vincenty import vincenty
from gmplot import gmplot

class cluster(dml.Algorithm):
    contributor = 'aolzh'
    reads = ['aolzh.NewYorkHouses','aolzh.NewYorkNormHouses']
    writes = ['aolzh.Cluster']

    @staticmethod
    def execute(trial = False):
        print("cluster")
        '''Retrieve some data sets (not using the API here for the sake of simplicity).'''
        startTime = datetime.datetime.now()

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('aolzh', 'aolzh')

        newyorknormhouses = repo.aolzh.NewYorkNormHouses
        newyorkhouses = repo.aolzh.NewYorkHouses
        
        norm_houses = newyorknormhouses.find()
        houses = newyorkhouses.find()

        test_data = []
        price = []
        name = []
        for n_h in norm_houses:
            for h in houses:
                if n_h['house'] == h['address']:
                    location = [float(h['latitude']),float(h['longitude'])]
                    price.append(h['Price'])
                    name.append(h['address'])
                    break
            houses_score = (n_h['norm_rate']*0.25 + n_h['norm_subway']*0.25 + n_h['norm_school']*0.25 + n_h['norm_stores']*0.25 + n_h['norm_hospitals']*0.25)

            test_data.append([houses_score,location[0],location[1]])

        testdata = np.array(test_data)

        score = testdata[:,0]
        latitude = testdata[:,1]
        longitude = testdata[:,2]

        testdata = preprocessing.scale(testdata)
        testdata[:, 1] = testdata[:,1] * 2.5
        testdata[:, 2] = testdata[:,2] * 2.5


        #To determine the k value
        error = float("inf")
        cluster_num = 10
        """
        for k in range(1,20):
            kmeanstmp = KMeans(init='k-means++', n_clusters=k, n_init=10)
            kmeanstmp.fit_predict(testdata)
            if kmeanstmp.inertia_ < error:
                error = kmeanstmp.inertia_
                cluster_num = k
        print(cluster_num)
        """
        kmeans = KMeans(n_clusters = cluster_num, init = 'k-means++', max_iter = 100, n_init = 10,random_state = 0)
        kmeans.fit_predict(testdata)
        k_centers = kmeans.cluster_centers_
        k_labels = kmeans.labels_
        k_error = kmeans.inertia_

        k_cluster_index = []
        for i in range(cluster_num):
            k_cluster_index.append([])
        for i in range(len(k_labels)):
            k_cluster_index[k_labels[i]].append(i)

        label_name = []
        cluster_house_name = []
        cluster_latitude = []
        cluster_longitude = []

        for i in range(cluster_num):
            total_score = 0
            total_price = 0
            cluster_house_name.append([])
            cluster_latitude.append([])
            cluster_longitude.append([])
            for j in range(len(k_cluster_index[i])):
                total_score += score[k_cluster_index[i][j]]
                total_price += price[k_cluster_index[i][j]]
                cluster_longitude[i].append(longitude[k_cluster_index[i][j]])
                cluster_latitude[i].append(latitude[k_cluster_index[i][j]])
                cluster_house_name[i].append(name[k_cluster_index[i][j]])
            label_name.append([total_score/len(k_cluster_index[i]), int(total_price/len(k_cluster_index[i]))])

        new_label = sorted(label_name,key = lambda k: k[0])
        rank = []
        for i in range(cluster_num):
            rank.append((new_label.index(label_name[i]))/2+0.5)


        urls = []
        for i in range(cluster_num):
            urls.append([])
            for j in range(len(k_cluster_index[i])):
                s = 'https://www.zillow.com/homes/'
                new_ad = (''.join(cluster_house_name[i][j].split(','))).replace(' ','-')
                s += new_ad+'_rb'
                urls[i].append(s)

        color = ['#ff0000','#ffd800','#50ff00','#00ffbb','#00a5ff','#0011ff','#d000ff','#ff008c','#000000','#ffafaf']
        gmap = gmplot.GoogleMapPlotter(40.7128, -74.0060, 12)
        for i in range(cluster_num):
            temp_la = []
            temp_lo = []
            for j in range(len(k_cluster_index[i])):
                temp_la.append(cluster_latitude[i][j])
                temp_lo.append(cluster_longitude[i][j])
            gmap.scatter(temp_la, temp_lo, color[i], size=150, marker=False)
        gmap.draw("my_map.html")
        res = []
        for i in range(cluster_num):
            for j in range(len(k_cluster_index[i])):
                res.append({'url':urls[i][j],'rank':rank[i],'label':label_name[i],'name': cluster_house_name[i][j],'latitude':cluster_latitude[i][j],'longitude':cluster_longitude[i][j],'cluster':i,'price':price[k_cluster_index[i][j]],'score':score[k_cluster_index[i][j]]})
        print(res)
        repo.dropCollection("Cluster")
        repo.createCollection("Cluster")
        repo["aolzh.Cluster"].insert_many(res)
        print("Finished")

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

        cluster_script = doc.agent('alg:aolzh#cluster', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})

        get_cluster = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)

        newyorknormhouses_resource = doc.entity('dat:aolzh#NewYorkNormHouses', {prov.model.PROV_LABEL:'NewYork Norm Houses', prov.model.PROV_TYPE:'ont:DataSet'})
        newyorkhouses_resource = doc.entity('dat:aolzh#NewYorkHouses', {prov.model.PROV_LABEL:'NewYork Houses', prov.model.PROV_TYPE:'ont:DataSet'})

        cluster_ = doc.entity('dat:aolzh#Cluster', {prov.model.PROV_LABEL:'NewYork Houses Cluster', prov.model.PROV_TYPE:'ont:DataSet'})

        doc.wasAssociatedWith(get_cluster, cluster_script)

        doc.usage(get_cluster, newyorknormhouses_resource, startTime, None,
                  {prov.model.PROV_TYPE:'ont:Retrieval'
                  }
                  )
        doc.usage(get_cluster, newyorkhouses_resource, startTime, None,
                  {prov.model.PROV_TYPE:'ont:Retrieval'
                  }
                  )
        
        doc.wasAttributedTo(cluster_, cluster_script)
        doc.wasGeneratedBy(cluster_, get_cluster, endTime)
        doc.wasDerivedFrom(cluster_, newyorknormhouses_resource,get_cluster, get_cluster, get_cluster)
        doc.wasDerivedFrom(cluster_, newyorkhouses_resource,get_cluster, get_cluster, get_cluster)

        repo.logout()
                  
        return doc

cluster.execute()
doc = cluster.provenance()
print(doc.get_provn())
print(json.dumps(json.loads(doc.serialize()), indent=4))

## eof
