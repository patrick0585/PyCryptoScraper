# coding: utf-8

from __future__ import absolute_import, unicode_literals

from marshmallow import Schema, fields


class DataSchema(Schema):
    name = fields.String(required=True)
    tags = fields.List(fields.String(), required=True)
