import datetime


class CFDI_Obj(object):
    # ["SubTotal", "Descuento", "Subtotal Neto", "Base 0", "16% IVA", "No deducible", "Total", "Diferencias"]
    def __init__(self, _dict, date_time=None):
        self.total = None
        self.IVA = None
        self.Imp_tras = None
        self.RFC_E = None
        self.num = None
        self.SubTotal_cfdi = None
        self.SubTotal = None
        self.base_cero = None
        self.ivaRetenido = None
        self.isrRetenido = None
        self.descuento = None
        self.nota = None
        self.SubTotal_pre_descuento = None

        self.aditional_properties = _dict  # type: dict
        # New

        self.fecha = date_time  # type: datetime.datetime

