from attr import attrs, attrib
@attrs
class JSONFilter(object):
    filter_json = attrib()

    def filter(self):
        criteria = (self)

