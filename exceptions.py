
class SchemaException(BaseException):

    def __unicode__(self):

        return "Schemaless handlers are not allowed, please, define self.output_schema in handler"
