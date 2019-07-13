from kivy.uix.modalview import ModalView
from datetime import datetime
from kivy.properties import StringProperty




class InfoWindow(ModalView):
    copyright_date = StringProperty('Def')
    software_version = StringProperty('Def')
    software_title = StringProperty('Def')

    def __init__(self, ml_object, **kwargs):
        super(InfoWindow, self).__init__(**kwargs)
        self.copyright_date = text= datetime.now().strftime('%Y')
        self.software_version = str(ml_object.software_version)
        self.software_title = str(ml_object.software_title)
