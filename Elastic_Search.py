from elasticsearch import Elasticsearch, helpers
from urllib.parse import urlparse
import os
class ElasticSearch:
    def __init__(self, index):
        es_host     = os.environ['es_hostname']
        es_port     = os.environ['es_port']

        if es_host is None:
            exit('You need to export Elasticsearch hostname')
        if es_port is None:
            exit('You need to export Elasticsearch port number')
        
        self.es     = Elasticsearch([{'host': es_host, 'port': es_port}])
        self.index  = index


    def delete_index(self):
        if self.exists():
            self._result = self.es.indices.delete(self.index)
        return self
    
    def exists(self):
        return self.es.indices.exists(self.index)
    
    def create_index(self):
        self._result= self.es.indices.create(self.index)
        return self

    def add_bulk(self, data):
        actions = []
        
        for record in data:
            phish = self.get_phish_record(record)

            #creatimg elasticsearch record
            elasticsearch_item_data = {
                                "_index" :  self.index,
                                "_source":  phish,
            }
            
            actions.append(elasticsearch_item_data)
        
        return helpers.bulk(self.es, actions, index=self.index)

    def get_phish_record(self, record):
        
        # pop out details, the idea is to create indivual rows
        phish_details   = record.pop('details', None)
            
        # parsing the phish url
        url_info        = urlparse(record['url'])
            
        # adding new fields
        record['schema'] = url_info.scheme
        record['domain'] = url_info.netloc

         #boolean
        if record['online'] == 'yes':
            record['online'] = 'true'
        else:
            record['online'] = 'false'
        
        if record['verified'] == 'yes':
            record['verified'] = 'true'
        else:
            record['verified'] = 'false'

        if url_info.path:
            record['path'] = url_info.path

        if url_info.params:
            record['params'] = url_info.params   

        if url_info.query:
            record['query'] = url_info.query

        if url_info.fragment:
            record['fragment'] = url_info.fragment

       

        if phish_details is not None:
            for item in phish_details:
                record['ip_address']         = item['ip_address']
                record['cidr_block']         = item['cidr_block']
                record['announcing_network'] = item['rir']
                record['country']            = item['country']
                record['detail_time']        = item['detail_time']
        return record    