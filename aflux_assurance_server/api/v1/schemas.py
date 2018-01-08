"""
Similar to Serializers in Django, these manage the conversion between
raw JSON and models. This is where parsing validation should be done.
"""
from marshmallow import Schema, SchemaOpts, fields, post_load
from aflux_assurance_server.api.v1.models import RealtimeDevice  # Import your models
from aflux_assurance_server.utils.meta_models import ModelSchema  # Shared class to create ModelSchemas

# Example:
# class RealtimeProtocolProfileSchema(ModelSchema):
#     collector_class = fields.String(required=True)
#     protocol_profile_data = fields.Dict()
#
#     class Meta:
#         model = ProtocolProfile
#
# class RealtimeProfileSchema(ModelSchema):
#     polling_profile = fields.String(required=True)
#     protocol_profile = fields.Nested(RealtimeProtocolProfileSchema, required=True)  # Notice the nested schema here
#     profile_data = fields.Dict()
#
#     class Meta:
#         model = RealtimeProfile
