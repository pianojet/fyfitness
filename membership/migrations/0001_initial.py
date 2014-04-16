# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Member'
        db.create_table(u'membership_member', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('member_since', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('occupation', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('strengths', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('want_support', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('about_me', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('who_can_view', self.gf('django.db.models.fields.CharField')(default='Everyone', max_length=50)),
            ('i_accept_terms_and_conditions', self.gf('django.db.models.fields.BooleanField')()),
            ('i_am_a_health_professional', self.gf('django.db.models.fields.BooleanField')()),
            ('hp_confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('icon', self.gf('django.db.models.fields.URLField')(max_length=70, null=True, blank=True)),
        ))
        db.send_create_signal(u'membership', ['Member'])

        # Adding M2M table for field authorized_followers on 'Member'
        m2m_table_name = db.shorten_name(u'membership_member_authorized_followers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_member', models.ForeignKey(orm[u'membership.member'], null=False)),
            ('to_member', models.ForeignKey(orm[u'membership.member'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_member_id', 'to_member_id'])

        # Adding model 'Follow'
        db.create_table(u'membership_follow', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('m', self.gf('django.db.models.fields.related.ForeignKey')(related_name='me', to=orm['membership.Member'])),
            ('y', self.gf('django.db.models.fields.related.ForeignKey')(related_name='follow_list', to=orm['membership.Member'])),
            ('blog_last_checked_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('progress_last_checked_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'membership', ['Follow'])

        # Adding model 'HealthProfessional'
        db.create_table(u'membership_healthprofessional', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['membership.Member'])),
            ('job_field', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('job_title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('credentials', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'membership', ['HealthProfessional'])

        # Adding model 'Goal'
        db.create_table(u'membership_goal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['membership.Member'])),
            ('who_can_view', self.gf('django.db.models.fields.CharField')(default='Everyone', max_length=50)),
            ('goal_start_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('goal_end_date', self.gf('django.db.models.fields.DateField')()),
            ('goal_type', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('goal_other_type', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('goal_metric', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('goal_unit_number', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('starting_unit_number', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('goal_unit_type', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('goal_other_unit_type', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('primary_goal', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'membership', ['Goal'])

        # Adding model 'Progress'
        db.create_table(u'membership_progress', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('day', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('goal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['membership.Goal'])),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['membership.Member'])),
            ('current_stat', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
        ))
        db.send_create_signal(u'membership', ['Progress'])


    def backwards(self, orm):
        # Deleting model 'Member'
        db.delete_table(u'membership_member')

        # Removing M2M table for field authorized_followers on 'Member'
        db.delete_table(db.shorten_name(u'membership_member_authorized_followers'))

        # Deleting model 'Follow'
        db.delete_table(u'membership_follow')

        # Deleting model 'HealthProfessional'
        db.delete_table(u'membership_healthprofessional')

        # Deleting model 'Goal'
        db.delete_table(u'membership_goal')

        # Deleting model 'Progress'
        db.delete_table(u'membership_progress')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'membership.follow': {
            'Meta': {'object_name': 'Follow'},
            'blog_last_checked_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'm': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'me'", 'to': u"orm['membership.Member']"}),
            'progress_last_checked_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'y': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'follow_list'", 'to': u"orm['membership.Member']"})
        },
        u'membership.goal': {
            'Meta': {'object_name': 'Goal'},
            'goal_end_date': ('django.db.models.fields.DateField', [], {}),
            'goal_metric': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'goal_other_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'goal_other_unit_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'goal_start_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'goal_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'goal_unit_number': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'goal_unit_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['membership.Member']"}),
            'primary_goal': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'starting_unit_number': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'who_can_view': ('django.db.models.fields.CharField', [], {'default': "'Everyone'", 'max_length': '50'})
        },
        u'membership.healthprofessional': {
            'Meta': {'object_name': 'HealthProfessional'},
            'credentials': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_field': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'job_title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['membership.Member']"})
        },
        u'membership.member': {
            'Meta': {'object_name': 'Member'},
            'about_me': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'authorized_followers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'auth'", 'symmetrical': 'False', 'to': u"orm['membership.Member']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'follow': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['membership.Member']", 'through': u"orm['membership.Follow']", 'symmetrical': 'False'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'hp_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'i_accept_terms_and_conditions': ('django.db.models.fields.BooleanField', [], {}),
            'i_am_a_health_professional': ('django.db.models.fields.BooleanField', [], {}),
            'icon': ('django.db.models.fields.URLField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'member_since': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'occupation': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'strengths': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'want_support': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'who_can_view': ('django.db.models.fields.CharField', [], {'default': "'Everyone'", 'max_length': '50'})
        },
        u'membership.progress': {
            'Meta': {'object_name': 'Progress'},
            'current_stat': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'day': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'goal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['membership.Goal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['membership.Member']"})
        }
    }

    complete_apps = ['membership']