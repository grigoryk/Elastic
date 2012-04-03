# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'KV.raw_split'
        db.add_column('conductor_kv', 'raw_split', self.gf('django.db.models.fields.IntegerField')(default=1000), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'KV.raw_split'
        db.delete_column('conductor_kv', 'raw_split')


    models = {
        'conductor.kv': {
            'Meta': {'object_name': 'KV'},
            'expiration': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.TextField', [], {}),
            'raw': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'raw_split': ('django.db.models.fields.IntegerField', [], {'default': '1000'}),
            'value': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'conductor.webtask': {
            'Meta': {'object_name': 'WebTask'},
            'complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map_code': ('django.db.models.fields.TextField', [], {}),
            'reduce_code': ('django.db.models.fields.TextField', [], {}),
            'results': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'urls': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['conductor']
