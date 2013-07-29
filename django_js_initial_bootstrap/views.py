import json
from django.utils.safestring import mark_safe
from rest_framework.serializers import ModelSerializer


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


class ListBasicBootstrapMixin(BaseBootstrapManager):
    bootstrapped_context_object = 'bootstrapped'

    def get_context_data(self, **kwargs):
        cd = super(ListBasicBootstrapMixin, self).get_context_data(**kwargs)
        cd[self.bootstrapped_context_object] = self.json_parse_code(json.dumps(self.prepare_queryset(cd['object_list'])))
        return cd

    def prepare_queryset(self, qs):
        return list(qs.values())


class ListSerializerBootstrapMixin(ListBasicBootstrapMixin):
    serializer_class = None
    model = None

    def prepare_queryset(self, qs):
        serializer = self.get_serializer(qs)
        return serializer.data

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'format': 'json',
            'view': self
        }

    def get_serializer(self, qs):
        serializer_class = self.get_serializer_class()
        context = self.get_serializer_context()
        return serializer_class(qs, many=True, context=context)

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if serializer_class is not None:
            return serializer_class

        assert self.model is not None, \
            "'%s' should either include a 'serializer_class' attribute, " \
            "or use the 'model' attribute as a shortcut for " \
            "automatically generating a serializer class." \
            % self.__class__.__name__

        class DefaultSerializer(ModelSerializer):
            class Meta:
                model = self.model
        return DefaultSerializer


class DetailJsonBootstrapMixin(BaseBootstrapManager):
    bootstrapped_context_object = 'bootstrapped'

    def get_context_data(self, **kwargs):
        cd = super(DetailJsonBootstrapMixin, self).get_context_data(**kwargs)
        cd[self.bootstrapped_context_object] = self.json_parse_code(json.dumps(self.prepare_object(self.object)))
        return cd

    def prepare_object(self, o):
        return o