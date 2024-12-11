from datetime import date, datetime
from unittest import TestCase

import pytest

from datetime_utils import JST
from potion import Potion
from properties.date import Date
from properties.property import Property
from properties.title import Title


class TestUpdateProperty(TestCase):
    DATABASE_ID = "1596567a3bbf80d58251f1159e5c40fa"
    PROP_NAME = "日付"

    def setUp(self) -> None:
        self.suite = Potion.get_instance()
        created_page = self.suite.create_page_in_database(
            database_id=self.DATABASE_ID, properties=[Title.from_plain_text(text="テスト")]
        )
        self.page = self.suite.retrieve_page(page_id=created_page["id"])
        return super().setUp()

    def tearDown(self) -> None:
        self.suite.remove_page(self.page.page_id.value)
        return super().setUp()

    @pytest.mark.post_api()
    def test_開始日を変更する(self):
        # Given
        date_ = date(2021, 1, 1)
        date_prop = Date.from_start_date(name=self.PROP_NAME, start_date=date_)

        # When, Then
        actual = self._update_page(property=date_prop)
        self.assertEqual(actual.start_date, date_)
        self.assertEqual(actual.start_time, date_)
        self.assertEqual(actual.start_datetime, datetime(2021, 1, 1, tzinfo=JST))
        self.assertEqual(actual.end_date, None)
        self.assertEqual(actual.end_datetime, None)
        self.assertEqual(actual.end_time, None)

    @pytest.mark.post_api()
    def test_開始時刻を変更する(self):
        # Given
        datetime_ = datetime(2021, 1, 1, 12, 34, 0, tzinfo=JST)
        date_prop = Date.from_start_date(name=self.PROP_NAME, start_date=datetime_)

        # When, Then
        actual = self._update_page(property=date_prop)
        self.assertEqual(actual.start_date, datetime_.date())
        print(actual.start_datetime)
        print(datetime_)
        self.assertEqual(actual.start_datetime, datetime_)
        self.assertEqual(actual.start_time, datetime_)
        self.assertEqual(actual.end_date, None)
        self.assertEqual(actual.end_datetime, None)
        self.assertEqual(actual.end_time, None)

    def _update_page(self, property: Property):
        # When
        properties = self.page.properties.append_property(property)
        self.suite.update_page(page_id=self.page.page_id.value, properties=properties.values)

        # Then
        page = self.suite.retrieve_page(page_id=self.page.page_id.value)
        return page.get_date(name=self.PROP_NAME)
