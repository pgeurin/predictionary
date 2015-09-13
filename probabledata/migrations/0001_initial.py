# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Prediction'
        db.create_table('probabledata_prediction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('probabledata', ['Prediction'])

        # Adding model 'Answer'
        db.create_table('probabledata_answer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('probabledata', ['Answer'])

        # Adding model 'Question'
        db.create_table('probabledata_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('probabledata', ['Question'])

        # Adding M2M table for field answers on 'Question'
        db.create_table('probabledata_question_answers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('question', models.ForeignKey(orm['probabledata.question'], null=False)),
            ('answer', models.ForeignKey(orm['probabledata.answer'], null=False))
        ))
        db.create_unique('probabledata_question_answers', ['question_id', 'answer_id'])

        # Adding M2M table for field predictions on 'Question'
        db.create_table('probabledata_question_predictions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('question', models.ForeignKey(orm['probabledata.question'], null=False)),
            ('prediction', models.ForeignKey(orm['probabledata.prediction'], null=False))
        ))
        db.create_unique('probabledata_question_predictions', ['question_id', 'prediction_id'])

    def backwards(self, orm):
        # Deleting model 'Prediction'
        db.delete_table('probabledata_prediction')

        # Deleting model 'Answer'
        db.delete_table('probabledata_answer')

        # Deleting model 'Question'
        db.delete_table('probabledata_question')

        # Removing M2M table for field answers on 'Question'
        db.delete_table('probabledata_question_answers')

        # Removing M2M table for field predictions on 'Question'
        db.delete_table('probabledata_question_predictions')

    models = {
        'probabledata.answer': {
            'Meta': {'object_name': 'Answer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'probabledata.prediction': {
            'Meta': {'object_name': 'Prediction'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'probabledata.question': {
            'Meta': {'object_name': 'Question'},
            'answers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['probabledata.Answer']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'predictions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['probabledata.Prediction']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['probabledata']