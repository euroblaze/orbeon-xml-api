import unittest
import re

from builder import Builder, Bind
from controls import Control
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
        self.builder = Builder(xml)
        self.bind_names = BINDS
        self.control_names = self._set_control_names()

    def _set_control_names(self):
        return [re.sub(r'-bind$', '', b) for b in self.bind_names]

    def test_set_binds(self):
        for name, bind in self.builder.binds.items():
            self.assertIn(name, self.bind_names)
            self.assertIsInstance(bind, Bind)

    def test_set_controls(self):
        for name, control in self.builder.controls.items():
            self.assertIn(name, self.control_names)
            self.assertIsInstance(control, Control)

    """
    Text Controls
    """
    def test_input(self):
        _input = self.builder.controls['input']

        self.assertEqual(_input.label, 'Input Field')
        self.assertEqual(_input.hint, 'Standard input field')
        self.assertEqual(_input.alert, None)
        self.assertEqual(_input.default_value, 'Michelle')

        self.assertEqual(_input.element.label, 'Input Field')
        self.assertEqual(_input.element.hint, 'Standard input field')

        # Doesn't exist, but shouldn't raise Exception
        self.assertEqual(_input.element.alert, None)

    def test_input_bind(self):
        _input = self.builder.controls['input']

        self.assertEqual(_input.bind.id, 'input-bind')
        self.assertEqual(_input.bind.name, 'input')

    def test_input_parent(self):
        _input = self.builder.controls['input']

        self.assertEqual(_input.parent.bind.id, 'text-controls-bind')
        self.assertEqual(_input.parent.bind.name, 'text-controls')
        self.assertEqual(_input.parent.element.label, 'Text Controls')

    def test_htmlarea(self):
        htmlarea = self.builder.controls['htmlarea']

        self.assertEqual(htmlarea.label, 'Formatted Text')
        self.assertEqual(htmlarea.hint, 'Rich text editor')
        self.assertEqual(htmlarea.alert, None)
        self.assertIn('Giuseppe Fortunino Francesco Verdi', htmlarea.default_value)

        self.assertEqual(htmlarea.element.label, 'Formatted Text')
        self.assertEqual(htmlarea.element.hint, 'Rich text editor')

        # Doesn't exist, but shouldn't raise Exception
        self.assertEqual(htmlarea.element.alert, None)

    def test_htmlarea_bind(self):
        htmlarea = self.builder.controls['htmlarea']

        self.assertEqual(htmlarea.bind.id, 'htmlarea-bind')
        self.assertEqual(htmlarea.bind.name, 'htmlarea')

    def test_htmlarea_parent(self):
        htmlarea = self.builder.controls['htmlarea']

        self.assertEqual(htmlarea.parent.bind.id, 'text-controls-bind')
        self.assertEqual(htmlarea.parent.bind.name, 'text-controls')
        self.assertEqual(htmlarea.parent.element.label, 'Text Controls')

    # Enough for (text-controls) 'bind' and 'parent' tests.
    def test_output(self):
        _output = self.builder.controls['output']

        self.assertEqual(_output.label, 'Text Output')
        self.assertEqual(_output.hint, None)
        self.assertEqual(_output.alert, None)
        self.assertEqual(_output.default_value, 'Great love and great achievements involve great risk.')

        self.assertEqual(_output.element.label, 'Text Output')
        self.assertEqual(_output.element.hint, None)
        self.assertEqual(_output.element.alert, None)

    def test_secret(self):
        secret = self.builder.controls['secret']

        self.assertEqual(secret.label, 'Password Field')
        self.assertEqual(secret.hint, 'The password is 42 ;)')
        self.assertEqual(secret.alert, None)
        self.assertEqual(secret.default_value, '42')

        self.assertEqual(secret.element.label, 'Password Field')
        self.assertEqual(secret.element.hint, 'The password is 42 ;)')
        self.assertEqual(secret.element.alert, None)

    def test_input_counter(self):
        input_counter = self.builder.controls['input-counter']

        self.assertEqual(input_counter.label, 'Input Field with Character Counter')
        self.assertEqual(input_counter.alert, '30 characters maximum')
        self.assertEqual(input_counter.hint, None)
        self.assertEqual(input_counter.default_value, 'This must not be "too long"!')

        self.assertEqual(input_counter.element.label, 'Input Field with Character Counter')
        self.assertEqual(input_counter.element.alert, '30 characters maximum')
        self.assertEqual(input_counter.element.hint, None)

    def test_textarea(self):
        textarea = self.builder.controls['textarea']

        self.assertEqual(textarea.label, 'Text Area')
        self.assertEqual(textarea.hint, 'Standard text area')
        self.assertIn('Music is an art', textarea.default_value)
        self.assertEqual(textarea.alert, None)

        self.assertEqual(textarea.element.label, 'Text Area')
        self.assertEqual(textarea.element.hint, 'Standard text area')

        self.assertEqual(textarea.element.alert, None)

    def test_textarea_counter(self):
        textarea_counter = self.builder.controls['textarea-counter']

        self.assertEqual(textarea_counter.default_value, "Let's write a Tweet. It must fit in 140 characters.")

        self.assertEqual(textarea_counter.element.label, 'Text Area with Character counter')
        self.assertEqual(textarea_counter.element.alert, '140 characters at most')
        self.assertEqual(textarea_counter.element.hint, None)

    """
    Date Controls
    """
    def test_date(self):
        date_control = self.builder.controls['date']

        self.assertEqual(date_control.label, 'Date')
        self.assertEqual(date_control.hint, 'Standard date field')
        self.assertEqual(date_control.alert, None)

        self.assertEqual(date_control.element.label, 'Date')
        self.assertEqual(date_control.element.hint, 'Standard date field')
        self.assertEqual(date_control.element.alert, None)

    def test_date_bind(self):
        date_control = self.builder.controls['date']

        self.assertEqual(date_control.bind.id, 'date-bind')
        self.assertEqual(date_control.bind.name, 'date')

    def test_date_parent(self):
        date_control = self.builder.controls['date']

        self.assertEqual(date_control.parent.bind.id, 'date-time-controls-bind')
        self.assertEqual(date_control.parent.bind.name, 'date-time-controls')

        self.assertEqual(date_control.parent.label, 'Date and Time')
        self.assertEqual(date_control.parent.element.label, 'Date and Time')

    def test_time(self):
        time_control = self.builder.controls['time']
        self.assertEqual(time_control.element.label, 'Time')
        self.assertEqual(time_control.element.hint, 'Standard time field')
        self.assertEqual(time_control.element.alert, None)

    def test_time_bind(self):
        time_control = self.builder.controls['time']

        self.assertEqual(time_control.bind.id, 'time-bind')
        self.assertEqual(time_control.bind.name, 'time')

    def test_time_parent(self):
        time_control = self.builder.controls['time']

        self.assertEqual(time_control.parent.bind.id, 'date-time-controls-bind')
        self.assertEqual(time_control.parent.bind.name, 'date-time-controls')

        self.assertEqual(time_control.parent.label, 'Date and Time')
        self.assertEqual(time_control.parent.element.label, 'Date and Time')

    def test_datetime(self):
        datetime_control = self.builder.controls['datetime']
        self.assertEqual(datetime_control.element.label, 'Date and Time')
        self.assertEqual(datetime_control.element.hint, 'Standard date and time field')
        self.assertEqual(datetime_control.element.alert, None)

    def test_dropdown_date(self):
        dropdown_date = self.builder.controls['dropdown-date']
        self.assertEqual(dropdown_date.element.label, 'Dropdown Date')
        self.assertEqual(dropdown_date.element.hint, 'Date selector with dropdown menus')
        self.assertEqual(dropdown_date.element.alert, None)

    def test_fields_date(self):
        fields_date_control = self.builder.controls['fields-date']
        self.assertEqual(fields_date_control.element.label, 'Fields Date')
        self.assertEqual(fields_date_control.element.hint, 'Date selector with separate fields')
        self.assertEqual(fields_date_control.element.alert, None)

    """
    Selection Controls
    """
    def test_autocomplete(self):
        autocomplete = self.builder.controls['autocomplete']
        self.assertEqual(autocomplete.element.label, 'Autocomplete')
        self.assertEqual(autocomplete.element.hint, 'Enter the name of a country')
        # TODO code (us-code?)
        # self.assertEqual(autocomplete.element.code, 'Country code')
        self.assertEqual(autocomplete.element.alert, None)

    def test_yesno_input(self):
        yesno_input = self.builder.controls['yesno-input']
        self.assertEqual(yesno_input.element.label, 'Yes/No Answer')
        self.assertEqual(yesno_input.element.hint, None)

    def test_checkbox_input(self):
        checkbox_input = self.builder.controls['checkbox-input']
        self.assertEqual(checkbox_input.element.label, 'Single Checkbox')
        self.assertEqual(checkbox_input.element.hint, 'An input which captures "true" or "false"')

    def test_radio_buttons(self):
        radio_buttons = self.builder.controls['radio-buttons']
        self.assertEqual(radio_buttons.element.label, 'Radio Buttons')
        self.assertEqual(radio_buttons.element.hint, 'Standard radio buttons')
        # TODO item(s) see itemset on control

    def test_open_select1(self):
        open_select1 = self.builder.controls['open-select1']
        self.assertEqual(open_select1.element.label, 'Ice Cream Flavor')
        self.assertEqual(open_select1.element.hint, None)
        # TODO item(s) see itemset on control

    def test_dropdown(self):
        dropdown = self.builder.controls['dropdown']
        self.assertEqual(dropdown.element.label, 'Dropdown Menu')
        self.assertEqual(dropdown.element.hint, 'Standard dropdown')
        # TODO item(s) see itemset on control

    def test_dynamic_data_dropdown(self):
        dynamic_data_dropdown = self.builder.controls['dynamic-data-dropdown']
        self.assertEqual(dynamic_data_dropdown.element.label, 'Dynamic Data Dropdown')
        self.assertEqual(dynamic_data_dropdown.element.hint, None)

    def test_checkboxes(self):
        checkboxes = self.builder.controls['checkboxes']
        self.assertEqual(checkboxes.element.label, 'Checkboxes')
        self.assertEqual(checkboxes.element.hint, 'Standard checkboxes')
        # TODO item(s) see itemset on control

    def test_multiple_list(self):
        multiple_list = self.builder.controls['multiple-list']
        self.assertEqual(multiple_list.element.label, 'Scrollable Checkboxes')
        self.assertEqual(multiple_list.element.hint, 'Scrollable selector with checkboxes')
        # TODO item(s) see itemset on control

    """
    Attachment Controls

    TODO:
    special data/binding etc.
    """
    def test_image_attachment(self):
        image_attachment = self.builder.controls['image-attachment']
        self.assertEqual(image_attachment.element.label, 'Image Attachment')
        self.assertEqual(image_attachment.element.hint, None)

    def test_file_attachment(self):
        file_attachment = self.builder.controls['file-attachment']
        self.assertEqual(file_attachment.element.label, 'File Attachment')
        self.assertEqual(file_attachment.element.hint, None)

    def test_static_image(self):
        static_image = self.builder.controls['static-image']
        self.assertEqual(static_image.element.label, 'Static Image')
        self.assertEqual(static_image.element.hint, None)

    """
    Button Controls
    """
    def test_standard_button(self):
        standard_button = self.builder.controls['standard-button']
        self.assertEqual(standard_button.element.label, 'Standard Button')
        self.assertEqual(standard_button.element.hint, 'Standard browser button')

    def test_link_button(self):
        link_button = self.builder.controls['link-button']
        self.assertEqual(link_button.element.label, 'Link Button')
        self.assertEqual(link_button.element.hint, 'Button as a link')

    """
    Typed Controls
    """
    def test_email(self):
        email = self.builder.controls['email']
        self.assertEqual(email.element.label, 'Email Address')
        self.assertEqual(email.element.hint, 'Email field with validation')

    def test_currency(self):
        currency = self.builder.controls['currency']
        self.assertEqual(currency.element.label, 'Currency')
        self.assertEqual(currency.element.hint, 'Currency field')

    def test_us_phone(self):
        us_phone = self.builder.controls['us-phone']
        self.assertEqual(us_phone.element.label, 'US Phone Number')
        self.assertEqual(us_phone.element.hint, 'US phone number field')

    def test_number(self):
        number = self.builder.controls['number']
        self.assertEqual(number.element.label, 'Number')
        self.assertEqual(number.element.hint, 'Number field with validation')

    def test_us_state(self):
        us_state = self.builder.controls['us-state']
        self.assertEqual(us_state.element.label, 'US State')
        self.assertEqual(us_state.element.hint, 'US state selector')

    def test_us_address(self):
        us_address = self.builder.controls['us-address']
        self.assertEqual(us_address.element.label, 'US Address Template')
        self.assertEqual(us_address.element.hint, None)
