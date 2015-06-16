"""
Most code parts from:
https://docs.djangoproject.com/en/dev/howto/custom-model-fields/#converting-values-to-python-objects
"""
from django.db import models

class CommaSeparatedModelField1(models.CharField):
    description = "Implements comma-separated storage of lists"

    def __init__(self, separator=",", *args, **kwargs):
        self.separator = separator
        super(CommaSeparatedModelField1, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(CommaSeparatedModelField1, self).deconstruct()
        # Only include kwarg if it's not the default
        if self.separator != ",":
            kwargs['separator'] = self.separator
        return name, path, args, kwargs

    def get_prep_value(self, value):
        return self.separator.join(value)

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)

    def to_python(self, value):
        if isinstance(value, (list, tuple)):
            return value

        if value is None:
            return value

        return value.split(self.separator)


class TestModel1(models.Model):
    test_data = CommaSeparatedModelField1(max_length=256)

"""
Testing against Django installed in '/home/jens/PyLucid_env/src/django/django'
Importing application custom_model_fields
Traceback (most recent call last):
  File "/home/jens/PyLucid_env/src/django/tests/runtests.py", line 448, in <module>
    options.debug_sql)
  File "/home/jens/PyLucid_env/src/django/tests/runtests.py", line 235, in django_tests
    state = setup(verbosity, test_labels)
  File "/home/jens/PyLucid_env/src/django/tests/runtests.py", line 214, in setup
    apps.set_installed_apps(settings.INSTALLED_APPS)
  File "/home/jens/PyLucid_env/src/django/django/apps/registry.py", line 324, in set_installed_apps
    self.populate(installed)
  File "/home/jens/PyLucid_env/src/django/django/apps/registry.py", line 108, in populate
    app_config.import_models(all_models)
  File "/home/jens/PyLucid_env/src/django/django/apps/config.py", line 198, in import_models
    self.models_module = import_module(models_module_name)
  File "/usr/lib/python2.7/importlib/__init__.py", line 37, in import_module
    __import__(name)
  File "/home/jens/PyLucid_env/src/django/tests/custom_model_fields/models.py", line 41, in <module>
    class CommaSeparatedModelField2(CommaSeparatedModelField1):
  File "/home/jens/PyLucid_env/src/django/django/db/models/fields/subclassing.py", line 22, in __new__
    RemovedInDjango20Warning)
django.utils.deprecation.RemovedInDjango20Warning: SubfieldBase has been deprecated. Use Field.from_db_value instead.

"""
# class CommaSeparatedModelField2(CommaSeparatedModelField1):
#     __metaclass__ = models.SubfieldBase
#
#
# class TestModel2(models.Model):
#     test_data = CommaSeparatedModelField2(max_length=256)