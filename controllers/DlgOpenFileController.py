from PyQt6.QtWidgets import QFileDialog


class DlgOpenFileController(QFileDialog):
    """

    Controlador para la gestión de acceso a datos permanentes en ficheros.
    Utilidad específica para la exportación/importación de datos.

    """
    def __init__(self):
        super(DlgOpenFileController, self).__init__()
