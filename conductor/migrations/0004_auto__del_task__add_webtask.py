# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Task'
        db.delete_table('conductor_task')

        # Adding model 'WebTask'
        db.create_table('conductor_webtask', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('map_code', self.gf('django.db.models.fields.TextField')()),
            ('reduce_code', self.gf('django.db.models.fields.TextField')()),
            ('results', self.gf('django.db.models.fields.TextField')()),
            ('complete', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('urls', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('conductor', ['WebTask'])


    def backwards(self, orm):
        
        # Adding model 'Task'
        db.create_table('conductor_task', (
            ('results', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('map_code', self.gf('django.db.models.fields.TextField')()),
            ('reduce_code', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('conductor', ['Task'])

        # Deleting model 'WebTask'
        db.delete_table('conductor_webtask')


    models = {
        'conductor.kv': {
            'Meta': {'object_name': 'KV'},
            'expiration': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.TextField', [], {}),
            'value': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'conductor.webtask': {
            'Meta': {'object_name': 'WebTask'},
            'complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map_code': ('django.db.models.fields.TextField', [], {}),
            'reduce_code': ('django.db.models.fields.TextField', [], {}),
            'results': ('django.db.models.fields.TextField', [], {}),
            'urls': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['conductor']
