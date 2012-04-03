from django.db import models
from django.core.urlresolvers import reverse

from utilities import *

import datetime

try:
    import cPickle as pickle
except ImportError:
    import pickle

class Task(models.Model):
    map_code = models.TextField(blank=True, null=True)
    reduce_code = models.TextField(blank=True, null=True)
    results = models.TextField(blank=True, null=True)
    complete = models.BooleanField(default=False)
    
    def got_results(self):
        if self.results:
            return True
        return False
    
    class Meta:
        abstract = True

class WebTask(Task):
    urls = models.TextField(blank=True, null=True)
    raw = models.ForeignKey('KV', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.raw:
            urls = []
            data_get_url = reverse('data-get', args=[])
            for i in range(0, len(self.raw.value.split(" ")), self.raw.raw_split):
                urls.append("%s?key=%s&from=%s&to=%s" % (data_get_url, self.raw.id, i, i + self.raw.raw_split))
            
            self.urls = pickle.dumps(urls)
        
        self.raw.save()
        
        super(WebTask, self).save(*args, **kwargs)

class KV(models.Model):
    key = models.TextField()
    value = models.TextField(blank=True, null=True)
    
    expiration = models.DateTimeField(blank=True, null=True)
    raw = models.BooleanField(default=True)
    raw_split = models.IntegerField(default=1000)
    
    def __unicode__(self):
        return u"%s-%s" % (self.id, self.key)
        
    def save(self, *args, **kwargs):
        if self.raw:
            cur = 0
            for xs in grouper(self.value.split(" "), self.raw_split):
                xs = [x for x in xs if x]
                set_cache("%s-%s-%s" % (self.id, cur, cur + self.raw_split), " ".join(xs), 60 * 60 * 24)
                cur += self.raw_split
                
        super(KV, self).save(*args, **kwargs)
    
    def expired(self):
        if not self.expiration:
            return False
        
        if datetime.datetime.now() > self.expiration:
            return False
        return True
