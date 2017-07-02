from datetime import datetime

from . import CommonTestCase
from orbeon_xml_api.controls import DateControl


class FieldsDateTestCase(CommonTestCase):

    def setUp(self):
        super(FieldsDateTestCase, self).setUp()
        self.control = self.builder.controls['fields-date']

    def test_control(self):
        self.assertIsInstance(self.control, DateControl)

        date_obj = datetime.strptime('2018-01-01', '%Y-%m-%d').date()

        self.assertEqual(self.control.encode(date_obj), '2018-01-01')
        self.assertEqual(self.control.decode('2018-01-01'), date_obj)

    def test_builder_bind(self):
        self.assertEqual(self.control.bind.id, 'fields-date-bind')
        self.assertEqual(self.control.bind.name, 'fields-date')

    def test_builder_parent(self):
        self.assertEqual(self.control.parent.bind.id, 'date-time-controls-bind')
        self.assertEqual(self.control.parent.bind.name, 'date-time-controls')

        self.assertEqual(self.control.parent.label, 'Date and Time')
        self.assertEqual(self.control.parent.element.label, 'Date and Time')

    def test_builder_form(self):
        self.assertEqual(self.control.element.label, 'Fields Date')
        self.assertEqual(self.control.element.hint, 'Date selector with separate fields')
        self.assertEqual(self.control.element.alert, None)

        # Shortcut via element
        self.assertEqual(self.control.label, 'Fields Date')
        self.assertEqual(self.control.hint, 'Date selector with separate fields')
        self.assertEqual(self.control.alert, None)

    def test_builder_form_default_value(self):
        date_obj = datetime.strptime('2009-10-16', '%Y-%m-%d').date()

        self.assertEqual(self.control.default_raw_value, '2009-10-16')
        self.assertEqual(self.control.default_value, date_obj)

    def test_runner_form(self):
        date_obj = datetime.strptime('2017-07-01', '%Y-%m-%d').date()

        self.assertEqual(self.runner.get_value('fields-date'), date_obj)
        self.assertEqual(self.runner.form.fieldsdate, date_obj)
