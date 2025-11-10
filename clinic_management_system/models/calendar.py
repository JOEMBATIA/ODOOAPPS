from odoo import fields, models, api


class Calendar(models.Model):
    # defines the table name inside the database
    _name = "syscraft.clinic.calendar.tbl"
    _description = "Calendar records"
    _rec_name = "NAME"

    NAME = fields.Char(String="NAME", required=True, tracking=True)
    IMAGE = fields.Image(String="", tracking=True)
    NEXTAPPT = fields.Date(String="NEXTAPPT", required=True, tracking=True)
    REF_NO = fields.Char(String="Reference No", tracking=True)
    GENDER = fields.Selection([('male', 'Male'), ('female', 'Female')], String="Gender")
    PHYSICIAN = fields.Selection([('Dr.Paras Rathod', 'Dr.Paras Rathod'), ('Dr.S.K Patel', 'Dr.S.K Patel'),
                                  ('Dr.Andrea', 'Dr.Andrea')], String="Physician", tracking=True)
    AVANE = fields.Selection(
        [('scheduled', 'Scheduled'), ('waiting', 'Waiting'), ('confirmed', 'Confirmed'), ('engaged', 'Engaged'),
         ('check out', 'Check Out'), ('cancelled', 'Cancelled')], string="Appointment Status ")
    AGE = fields.Integer(String="Age", tracking=True)
    BELONGSTOCLINIC = fields.Selection(
        [('Avane Dermatology Clinic, Girigiri(G)', 'Avane Dermatology Clinic, Girigiri(G)'),
         ('Avane Dermatology Clinic, Girigiri(USD)(USG)',
          'Avane Dermatology Clinic, Girigiri(USD)(USG)'),
         ('Avane Dermatology Clinic, Park Suites(P)',
          'Avane Dermatology Clinic, Park Suites(P)'),
         ('Avane Dermatology Clinic, Park Suites(USD)(USG)',
          'Avane Dermatology Clinic, Park Suites(USD)(USG)'),
         ('Avane Dermatology Clinic, Yaya (Y)', 'Avane Dermatology Clinic, Yaya (Y)'),
         ('Avane Dermatology Clinic, Yaya (USD)(USG)', 'Avane Dermatology Clinic, Yaya (USD)(USG)'),
         ('Avane SPA, (SPA)', 'Avane SPA, (SPA)'),
         ('Avane SPA, (USD)(USG)', 'Avane SPA, (USD)(USG)'),
         ('Avane Store, (AVS)', 'Avane Store, (AVS)')],
        String="Clinic name", tracking=True)
    NETBALANCE = fields.Char(String="Net balance", tracking=True)
    EMAIL = fields.Text(String="Email address ", tracking=True)
    CATEGORY = fields.Selection([(';Consultation', ';Consultation'), ('BotoxF;Fillers', 'BotoxF;Fillers'),
                                 ('Consultation;Fillers', 'Consultation;Fillers'),
                                 ('Consultation;Fillers;Botox', 'Consultation;Fillers;Botox'),
                                 ('Consultation;Fillers;Hydrafacial', 'Consultation;Fillers;Hydrafacial'),
                                 ('massage', 'massage')],
                                String="Gender")


