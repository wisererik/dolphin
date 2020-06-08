from unittest import mock

from dolphin import context, exception
from dolphin import test
from dolphin.db import api as db_api
from dolphin.db.sqlalchemy import api, models


class TestSIMDBAPI(test.TestCase):

    @mock.patch('sqlalchemy.create_engine', mock.Mock())
    def test_register_db(self):
        db_api.register_db()

    def test_get_session(self):
        api.get_session()

    def test_get_engine(self):
        api.get_engine()

    @mock.patch('dolphin.db.sqlalchemy.api.get_session')
    def test_storage_get(self, mock_session):
        fake_storage = {}
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_storage
        result = db_api.storage_get(context,
                                    'c5c91c98-91aa-40e6-85ac-37a1d3b32bda')
        assert len(result) == 0

    @mock.patch('dolphin.db.sqlalchemy.api.get_session')
    def test_storage_update(self, mock_session):
        fake_storage = models.Storage()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_storage
        result = db_api.storage_update(context,
                                       'c5c91c98-91aa-40e6-85ac-37a1d3b32bda',
                                       fake_storage)
        assert len(result) == 0

    @mock.patch('dolphin.db.sqlalchemy.api.get_session')
    def test_storage_delete(self, mock_session):
        fake_storage = models.Storage()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_storage
        result = db_api.storage_delete(context,
                                       'c5c91c98-91aa-40e6-85ac-37a1d3b32bda')
        assert result is None

    @mock.patch('dolphin.db.sqlalchemy.api.get_session')
    def test_storage_create(self, mock_session):
        fake_storage = models.Storage()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_storage
        result = db_api.storage_create(context, fake_storage)
        assert len(result) == 0

    @mock.patch('dolphin.db.sqlalchemy.api.get_session')
    def test_storage_get_all(self, mock_session):
        fake_storage = []
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_storage
        result = db_api.storage_get_all(context)
        assert len(result) == 0

        mock_session.return_value.__enter__.return_value.query = fake_storage
        result = db_api.storage_get_all(context, filters={'status': 'Normal'})
        assert len(result) == 0

        result = db_api.storage_get_all(context, limit=1)
        assert len(result) == 0

        result = db_api.storage_get_all(context, offset=3)
        assert len(result) == 0

        result = db_api.storage_get_all(context, sort_dirs=['desc'],
                                        sort_keys=['name'])
        assert len(result) == 0

        self.assertRaises(exception.InvalidInput, api.storage_get_all,
                          context, sort_dirs=['desc', 'asc'],
                          sort_keys=['name'])

        self.assertRaises(exception.InvalidInput, api.storage_get_all,
                          context, sort_dirs=['desc_err'],
                          sort_keys=['name'])

        result = db_api.storage_get_all(context, sort_dirs=['desc'],
                                        sort_keys=['name', 'id'])
        assert len(result) == 0

    @mock.patch('dolphin.db.sqlalchemy.api.get_session')
    def test_pool_get(self, mock_session):
        fake_pool = {}
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_pool
        result = db_api.pool_get(context,
                                 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd')
        assert len(result) == 0

    @mock.patch('dolphin.db.sqlalchemy.api.get_session')
    def test_pool_get_all(self, mock_session):
        fake_pool = []
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_pool
        result = api.pool_get_all(context)
        assert len(result) == 0

        result = db_api.pool_get_all(context, filters={'status': 'Normal'})
        assert len(result) == 0

    @mock.patch('dolphin.db.sqlalchemy.api.get_session')
    def test_pools_update(self, mock_session):
        pools = [{'id': 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd'}]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = pools
        result = db_api.pools_update(context, pools)
        assert len(result) == 1

    @mock.patch('dolphin.db.sqlalchemy.api.get_session')
    def test_pool_update(self, mock_session):
        values = {'id': 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd'}
        mock_session.return_value.__enter__.return_value.query.return_value \
            = values
        result = db_api.pool_update(context,
                                    'c5c91c98-91aa-40e6-85ac-37a1d3b32bd',
                                    values)
        assert len(result) == 0

    @mock.patch('dolphin.db.sqlalchemy.api.get_session')
    def test_pools_delete(self, mock_session):
        fake_pools = [models.Pool().id]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_pools
        result = db_api.pools_delete(context, fake_pools)
        assert result is None

    @mock.patch('dolphin.db.sqlalchemy.api.get_session')
    def test_pools_create(self, mock_session):
        fake_pools = [models.Pool()]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_pools
        result = db_api.pools_create(context, fake_pools)
        assert len(result) == 1

    @mock.patch('dolphin.db.sqlalchemy.api.get_session')
    def test_pool_create(self, mock_session):
        fake_pool = models.Pool()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_pool
        result = db_api.pool_create(context, fake_pool)
        assert len(result) == 0

    @mock.patch('dolphin.db.sqlalchemy.api.get_session')
    def test_volume_get(self, mock_session):
        fake_volume = {}
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_volume
        result = db_api.volume_get(context,
                                   'c5c91c98-91aa-40e6-85ac-37a1d3b32bd')
        assert len(result) == 0

    @mock.patch('dolphin.db.sqlalchemy.api.get_session')
    def test_volumes_update(self, mock_session):
        volumes = [{'id': 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd'}]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = volumes
        result = db_api.volumes_update(context, volumes)
        assert result is None

    @mock.patch('dolphin.db.sqlalchemy.api.get_session')
    def test_volume_update(self, mock_session):
        volumes = [{'id': 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd'}]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = volumes
        result = db_api.volume_update(context,
                                      'c5c91c98-91aa-40e6-85ac-37a1d3b32bd',
                                      volumes)
        assert len(result) == 0

    @mock.patch('dolphin.db.sqlalchemy.api.get_session')
    def test_volumes_delete(self, mock_session):
        fake_volume = ['c5c91c98-91aa-40e6-85ac-37a1d3b32bd']
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_volume
        result = db_api.volumes_delete(context, fake_volume)
        assert result is None

    @mock.patch('dolphin.db.sqlalchemy.api.get_session')
    def test_volumes_create(self, mock_session):
        fake_volume = [models.Volume()]
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_volume
        result = db_api.volumes_create(context, fake_volume)
        assert len(result) == 1

    @mock.patch('dolphin.db.sqlalchemy.api.get_session')
    def test_volume_create(self, mock_session):
        fake_volume = models.Volume()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_volume
        result = db_api.volume_create(context, fake_volume)
        assert len(result) == 0

    @mock.patch('dolphin.db.sqlalchemy.api.get_session')
    def test_volume_get_all(self, mock_session):
        fake_volume = []
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_volume
        result = db_api.volume_get_all(context)
        assert len(result) == 0

        result = db_api.volume_get_all(context, filters={'status': 'Normal'})
        assert len(result) == 0

    @mock.patch('dolphin.db.sqlalchemy.api.get_session')
    def test_access_info_get_all(self, mock_session):
        fake_access_info = []
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_access_info
        result = db_api.access_info_get_all(context)
        assert len(result) == 0

    @mock.patch('dolphin.db.sqlalchemy.api.get_session')
    def test_access_info_get(self, mock_session):
        fake_access_info = models.AccessInfo()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_access_info
        result = db_api.access_info_get(context,
                                        'c5c91c98-91aa-40e6-85ac-37a1d3b32bd')
        assert len(result) == 0

    @mock.patch('dolphin.db.sqlalchemy.api.get_session')
    def test_access_info_create(self, mock_session):
        fake_access_info = models.AccessInfo()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_access_info
        result = db_api.access_info_create(context, fake_access_info)
        assert len(result) == 0

    @mock.patch('dolphin.db.sqlalchemy.api.get_session')
    def test_access_info_update(self, mock_session):
        fake_access_info = models.AccessInfo()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_access_info
        result = db_api.access_info_update(
            context, 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd', fake_access_info)
        assert len(result) == 0

    @mock.patch('dolphin.db.sqlalchemy.api.get_session')
    def test_alert_source_get_all(self, mock_session):
        fake_alert_source = []
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_alert_source
        result = db_api.alert_source_get_all(context)
        assert len(result) == 0

        result = db_api.alert_source_get_all(context,
                                             filters={'status': 'Normal'})
        assert len(result) == 0

    @mock.patch('dolphin.db.sqlalchemy.api.get_session')
    def test_alert_source_update(self, mock_session):
        fake_alert_source = models.AlertSource()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_alert_source
        result = db_api.alert_source_update(
            context, 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd', fake_alert_source)
        assert len(result) == 0

    @mock.patch('dolphin.db.sqlalchemy.api.get_session')
    def test_alert_source_delete(self, mock_session):
        fake_alert_source = models.AlertSource()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_alert_source
        result = db_api.alert_source_delete(
            context, 'c5c91c98-91aa-40e6-85ac-37a1d3b32bd')
        assert result is None

    @mock.patch('dolphin.db.sqlalchemy.api.get_session')
    def test_alert_source_create(self, mock_session):
        fake_alert_source = models.AlertSource()
        mock_session.return_value.__enter__.return_value.query.return_value \
            = fake_alert_source
        result = db_api.alert_source_create(context, fake_alert_source)
        assert len(result) == 0
