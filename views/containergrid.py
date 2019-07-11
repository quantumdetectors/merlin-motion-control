from kivy.uix.gridlayout import GridLayout
from views.actionbuttons import ActionButtons
from views.statusfields import StatusFields
from views.labels import Labels

class ContainerGrid(GridLayout):
    def __init__(self, **kwargs):
        super(ContainerGrid, self).__init__(**kwargs)
