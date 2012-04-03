# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'WebTask.map_code'
        db.alter_column('conductor_webtask', 'map_code', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'WebTask.reduce_code'
        db.alter_column('conductor_webtask', 'reduce_code', self.gf('django.db.models.fields.TextField')(null=True))


    def backwards(self, orm):
        
        # Changing field 'WebTask.map_code'
        db.alter_column('conductor_webtask', 'map_code', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'WebTask.reduce_code'
        db.alter_column('conductor_webtask', 'reduce_code', self.gf('django.db.models.fields.TextField')(default=''))


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
            'map_code': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'raw': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conductor.KV']", 'null': 'True', 'blank': 'True'}),
            'reduce_code': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'results': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'urls': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['conductor']
