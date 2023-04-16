from marshmallow import fields, Schema


class Frame(Schema):
    captured = fields.Str(required=True)


class Response(Schema):
    ear = fields.Number(required=True)
    status = fields.Boolean(required=True, default=False)
