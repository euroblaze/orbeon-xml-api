import unittest
import re

from builder import Builder, Bind, Control
from utils import xml_from_file

TEXT_CONTROLS_BIND = ['text-controls-bind', 'input-bind', 'htmlarea-bind', 'output-bind',
                      'secret-bind', 'input-counter-bind', 'textarea-bind', 'textarea-counter-bind']

DATE_TIME_CONTROLS_BIND = ['date-time-controls-bind', 'date-bind', 'time-bind', 'datetime-bind',
                           'dropdown-date-bind', 'fields-date-bind']

SELECTION_CONTROLS_BIND = ['selection-controls-bind', 'autocomplete-bind', 'yesno-input-bind',
                           'checkbox-input-bind', 'radio-buttons-bind', 'open-select1-bind',
                           'dropdown-bind', 'dynamic-data-dropdown-bind', 'checkboxes-bind',
                           'multiple-list-bind']

# What about? image-attachments-iteration-bind
ATTACHMENT_CONTROLS_BIND = ['attachment-controls-bind', 'image-attachments-bind',
                            'image-attachments-iteration-bind', 'image-attachment-bind',
                            'file-attachment-bind', 'static-image-bind']

BUTTONS_BIND = ['buttons-bind', 'standard-button-bind', 'link-button-bind']

TYPED_CONTROLS_BIND = ['typed-controls-bind', 'email-bind', 'currency-bind', 'us-phone-bind',
                       'number-bind', 'us-state-bind']

US_ADDRESS_BIND = ['us-address-bind']

BINDS = TEXT_CONTROLS_BIND + DATE_TIME_CONTROLS_BIND + SELECTION_CONTROLS_BIND + \
            ATTACHMENT_CONTROLS_BIND + BUTTONS_BIND + TYPED_CONTROLS_BIND + US_ADDRESS_BIND


class BuilderTestCase(unittest.TestCase):

    def setUp(self):
        super(BuilderTestCase, self).setUp()

        xml = xml_from_file('tests/data', 'test_controls_builder.xml')
        self.builder_1 = Builder(xml)
        self.bind_names = BINDS
        self.control_names = self._set_control_names()

    def _set_control_names(self):
        return [re.sub(r'-bind$', '', b) for b in self.bind_names]

    def test_set_binds(self):
        for name, bind in self.builder_1.binds.items():
            self.assertIn(name, self.bind_names)
            self.assertIsInstance(bind, Bind)

    def test_set_controls(self):
        for name, control in self.builder_1.controls.items():
            self.assertIn(name, self.control_names)
            self.assertIsInstance(control, Control)

    def test_input_control_bind(self):
        _input = self.builder_1.controls['input']
        self.assertEqual(_input.bind.id, 'input-bind')
        self.assertEqual(_input.bind.name, 'input')

    def test_input_control_element(self):
        _input = self.builder_1.controls['input']
        self.assertEqual(_input.element.label, 'Input Field')
        self.assertEqual(_input.element.hint, 'Standard input field')
        self.assertEqual(_input.default_value, 'Michelle')

        # Doesn't exist, but shouldn't raise Exception
        self.assertEqual(_input.element.alert, None)

    def test_input_control_parent(self):
        _input = self.builder_1.controls['input']
        self.assertEqual(_input.parent.bind.id, 'text-controls-bind')
        self.assertEqual(_input.parent.bind.name, 'text-controls')
        self.assertEqual(_input.parent.element.label, 'Text Controls')

    def test_htmlarea_control_bind(self):
        htmlarea = self.builder_1.controls['htmlarea']
        self.assertEqual(htmlarea.bind.id, 'htmlarea-bind')
        self.assertEqual(htmlarea.bind.name, 'htmlarea')

    def test_htmlarea_control_element(self):
        htmlarea = self.builder_1.controls['htmlarea']
        self.assertEqual(htmlarea.element.label, 'Formatted Text')
        self.assertEqual(htmlarea.element.hint, 'Rich text editor')
        self.assertIn('Giuseppe Fortunino Francesco Verdi', htmlarea.default_value)

        # Doesn't exist, but shouldn't raise Exception
        self.assertEqual(htmlarea.element.alert, None)

    def test_htmlarea_control_parent(self):
        htmlarea = self.builder_1.controls['htmlarea']
        self.assertEqual(htmlarea.parent.bind.id, 'text-controls-bind')
        self.assertEqual(htmlarea.parent.bind.name, 'text-controls')
        self.assertEqual(htmlarea.parent.element.label, 'Text Controls')

    """
    Enough for 'bind' and 'parent' tests.
    """

    def test_output_control(self):
        _output = self.builder_1.controls['output']
        self.assertEqual(_output.element.label, 'Text Output')
        self.assertEqual(_output.default_value, 'Great love and great achievements involve great risk.')
        self.assertEqual(_output.element.hint, None)
        self.assertEqual(_output.element.alert, None)

    def test_secret_control(self):
        secret = self.builder_1.controls['secret']
        self.assertEqual(secret.element.label, 'Password Field')
        self.assertEqual(secret.element.hint, 'The password is 42 ;)')
        self.assertEqual(secret.default_value, '42')
        self.assertEqual(secret.element.alert, None)

    def test_input_counter_control(self):
        input_counter = self.builder_1.controls['input-counter']
        self.assertEqual(input_counter.element.label, 'Input Field with Character Counter')
        self.assertEqual(input_counter.default_value, 'This must not be "too long"!')
        self.assertEqual(input_counter.element.alert, '30 characters maximum')
        self.assertEqual(input_counter.element.hint, None)

    def test_textarea_control(self):
        textarea = self.builder_1.controls['textarea']
        self.assertEqual(textarea.element.label, 'Text Area')
        self.assertEqual(textarea.element.hint, 'Standard text area')
        self.assertIn('Music is an art', textarea.default_value)
        self.assertEqual(textarea.element.alert, None)

    def test_textarea_counter_control(self):
        textarea_counter = self.builder_1.controls['textarea-counter']
        self.assertEqual(textarea_counter.element.label, 'Text Area with Character counter')
        self.assertEqual(textarea_counter.default_value, "Let's write a Tweet. It must fit in 140 characters.")
        self.assertEqual(textarea_counter.element.alert, '140 characters at most')
        self.assertEqual(textarea_counter.element.hint, None)

    def test_date_control(self):
        date_control = self.builder_1.controls['date']
        self.assertEqual(date_control.element.label, 'Date')
        self.assertEqual(date_control.element.hint, 'Standard date field')
        self.assertEqual(date_control.element.alert, None)

    def test_time_control(self):
        time_control = self.builder_1.controls['time']
        self.assertEqual(time_control.element.label, 'Time')
        self.assertEqual(time_control.element.hint, 'Standard time field')
        self.assertEqual(time_control.element.alert, None)

    def test_datetime_control(self):
        datetime_control = self.builder_1.controls['datetime']
        self.assertEqual(datetime_control.element.label, 'Date and Time')
        self.assertEqual(datetime_control.element.hint, 'Standard date and time field')
        self.assertEqual(datetime_control.element.alert, None)

    def test_dropdown_date_control(self):
        dropdown_date_control = self.builder_1.controls['dropdown-date']
        self.assertEqual(dropdown_date_control.element.label, 'Dropdown Date')
        self.assertEqual(dropdown_date_control.element.hint, 'Date selector with dropdown menus')
        self.assertEqual(dropdown_date_control.element.alert, None)

    def test_fields_date_control(self):
        fields_date_control = self.builder_1.controls['fields-date']
        self.assertEqual(fields_date_control.element.label, 'Fields Date')
        self.assertEqual(fields_date_control.element.hint, 'Date selector with separate fields')
        self.assertEqual(fields_date_control.element.alert, None)
