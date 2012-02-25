# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'KV.value'
        db.alter_column('conductor_kv', 'value', self.gf('django.db.models.fields.TextField')(null=True))


    def backwards(self, orm):
        
        # Changing field 'KV.value'
        db.alter_column('conductor_kv', 'value', self.gf('django.db.models.fields.TextField')(default=''))


    models = {
        'conductor.kv': {
            'Meta': {'object_name': 'KV'},
            'expiration': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.TextField', [], {}),
            'value': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'conductor.task': {
            'Meta': {'object_name': 'Task'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map_code': ('django.db.models.fields.TextField', [], {}),
            'reduce_code': ('django.db.models.fields.TextField', [], {}),
            'results': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['conductor']
