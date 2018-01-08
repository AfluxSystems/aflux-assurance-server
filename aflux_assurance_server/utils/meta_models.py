from marshmallow import Schema, SchemaOpts, fields, post_load


class MetaModelSchemaOpts(SchemaOpts):
    """
    Used to set the Meta class settings for ModelSchema.
    """
    def __init__(self, meta):
        super().__init__(meta)
        self.model = getattr(meta, 'model', None)


class ModelSchema(Schema):
    OPTIONS_CLASS = MetaModelSchemaOpts

    def _get_schema_model_class(self):
        return self.opts.model

    @post_load
    def to_object(self, data):
        return self._get_schema_model_class()(**data)
