# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'KV'
        db.create_table('conductor_kv', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.TextField')()),
            ('value', self.gf('django.db.models.fields.TextField')()),
            ('expiration', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('conductor', ['KV'])


    def backwards(self, orm):
        
        # Deleting model 'KV'
        db.delete_table('conductor_kv')


    models = {
        'conductor.kv': {
            'Meta': {'object_name': 'KV'},
            'expiration': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.TextField', [], {}),
            'value': ('django.db.models.fields.TextField', [], {})
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
