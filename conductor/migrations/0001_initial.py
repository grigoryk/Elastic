# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Task'
        db.create_table('conductor_task', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('map_code', self.gf('django.db.models.fields.TextField')()),
            ('reduce_code', self.gf('django.db.models.fields.TextField')()),
            ('results', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('conductor', ['Task'])


    def backwards(self, orm):
        
        # Deleting model 'Task'
        db.delete_table('conductor_task')


    models = {
        'conductor.task': {
            'Meta': {'object_name': 'Task'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map_code': ('django.db.models.fields.TextField', [], {}),
            'reduce_code': ('django.db.models.fields.TextField', [], {}),
            'results': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['conductor']
