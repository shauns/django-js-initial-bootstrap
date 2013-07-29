import json
from django.utils.safestring import mark_safe


class BaseBootstrapManager(object):
    def json_parse_code(self, json_string):
        """
        Provide Javascript statement to parse a JSON string into an object. Override this if you want to create your
        object in a different way.

        @param json_string: The JSON string we should be parsing in Javascript
        @type json_string: str
        @return: A safe string with a Javascript expression to insert directly into a template
        @rtype: SafeString
        """
        return mark_safe("JSON.parse('%s')" % json_string)


class ListJsonBootstrapMixin(BaseBootstrapManager):
    bootstrapped_context_object = 'bootstrapped'

    def get_context_data(self, **kwargs):
        cd = super(ListJsonBootstrapMixin, self).get_context_data(**kwargs)
        cd[self.bootstrapped_context_object] = self.json_parse_code(json.dumps(self.prepare_queryset(cd['object_list'])))
        return cd

    def prepare_queryset(self, qs):
        return list(qs.values())


class DetailJsonBootstrapMixin(BaseBootstrapManager):
    bootstrapped_context_object = 'bootstrapped'

    def get_context_data(self, **kwargs):
        cd = super(DetailJsonBootstrapMixin, self).get_context_data(**kwargs)
        cd[self.bootstrapped_context_object] = self.json_parse_code(json.dumps(self.prepare_object(self.object)))
        return cd

    def prepare_object(self, o):
        return o