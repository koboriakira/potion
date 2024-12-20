from unittest import TestCase


from lotion.filter import Builder, Cond, Prop

# https://developers.notion.com/reference/post-database-query-filter

import pytest


class TestBuilder(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_タイトルで絞りこむ(self):
        actual = (
            Builder.create()
            .add(prop_type=Prop.RICH_TEXT, prop_name="名前", cond_type=Cond.EQUALS, value="テストA")
            .build()
        )
        expected = {
            "property": "名前",
            "rich_text": {
                "equals": "テストA",
            },
        }
        self.assertEqual(expected, actual)

    def test_作成日時で絞り込む(self):
        actual = Builder.create().add_created_at(cond_type=Cond.ON_OR_BEFORE, value="2024-12-16").build()
        expected = {
            "timestamp": "created_time",
            "created_time": {
                "on_or_before": "2024-12-16",
            },
        }
        self.assertEqual(expected, actual)

    def test_and条件で絞り込む(self):
        actual = (
            Builder.create()
            .add(prop_type=Prop.RICH_TEXT, prop_name="名前", cond_type=Cond.EQUALS, value="テストA")
            .add(prop_type=Prop.RICH_TEXT, prop_name="名前", cond_type=Cond.EQUALS, value="テストB")
            .build()
        )
        print(actual)
        expected = {
            "and": [
                {
                    "property": "名前",
                    "rich_text": {"equals": "テストA"},
                },
                {
                    "property": "名前",
                    "rich_text": {"equals": "テストB"},
                },
            ],
        }
        self.assertEqual(expected, actual)

    def test_or条件で絞り込む(self):
        actual = (
            Builder.create()
            .add(prop_type=Prop.RICH_TEXT, prop_name="名前", cond_type=Cond.EQUALS, value="テストA")
            .add(prop_type=Prop.RICH_TEXT, prop_name="名前", cond_type=Cond.EQUALS, value="テストB")
            .build(mode="or")
        )
        expected = {
            "or": [
                {
                    "property": "名前",
                    "rich_text": {"equals": "テストA"},
                },
                {
                    "property": "名前",
                    "rich_text": {"equals": "テストB"},
                },
            ],
        }
        self.assertEqual(expected, actual)
