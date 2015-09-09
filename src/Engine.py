'''
Created on 14 ago 2015
Rev 3.0
@author: Righetz,M
'''
import glob
import json
import os

class Engine():
    '''
    File saving,file loading,file deletion
    '''
    path = 'data/'

    def get_payloads(self):
        '''
        get current file list from default directory and return payload list
        '''
        filenames = glob.glob(self.path + '*.json')
        payload_listing = []
        for file in filenames:
            with open(file, 'r') as cur_file:
                cur_object = json.load(cur_file)
                payload_listing.append(cur_object)
        return payload_listing

    def save_file(self, payload, overwrite):
        '''
        save new payload file from data object
        '''
        if overwrite:
            file = open(self.path + payload['title'].replace(' ', '_') + '.json', 'r')
            json_data = json.load(file)
            file.close()
        else:
            json_data = {}
        json_data['title'] = payload['title']
        json_data['description'] = payload['description']
        json_data['code'] = payload['code']
        json_data['tags'] = payload['tags']
        file = open(self.path + json_data['title'].replace(' ', '_') + '.json', 'w')
        file.write(json.dumps(json_data))
        file.close()

    def delete_file(self, file_name):
        '''
        delete payload file from current selection
        '''
        os.remove(self.path + file_name.replace(' ', '_') + '.json')

    def update_values(self, updated_list):
        '''
        with filtered titles list, get associated payloads values from JSON
        '''
        filenames = glob.glob(self.path + '*.json')
        payload_listing = []
        for file in filenames:
            with open(file, 'r') as cur_file:
                cur_object = json.load(cur_file)
                if cur_object['title'] in updated_list:
                    payload_listing.append(cur_object)
        return payload_listing
