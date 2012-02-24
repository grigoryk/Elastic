from django.db import models

import datetime
import pickle

class Task(models.Model):
    map_code = models.TextField()
    reduce_code = models.TextField()
    results = models.TextField()
    
    def got_results(self):
        if self.results:
            return True
        return False

class KV(models.Model):
    key = models.TextField()
    value = models.TextField(blank=True, null=True)
    
    expiration = models.DateTimeField(blank=True, null=True)
    
    def unpickled(self):
        try:
            return pickle.loads(str(self.value))
        except:
            return None
    
    def expired(self):
        if not self.expiration:
            return False
        
        if datetime.datetime.now() > self.expiration:
            return False
        return True
