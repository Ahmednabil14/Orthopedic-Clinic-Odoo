from odoo import models, fields

class PatientHistoryWizard(models.TransientModel):
    _name = 'clinic.wizard'
    _description = 'Patient History Wizard'

    c_o = fields.Text(string='C/O')
    o_e = fields.Text(string='O/E')
    description = fields.Text(string='D:')
    recommendation = fields.Text(string='For:')
    lab_results = fields.Text()
    patient_id = fields.Many2one('clinic.patient')
    date = fields.Date(default=fields.Date.today())

    def action_add_history(self):
        self.ensure_one()

        self.env['clinic.history'].create({
            'c_o': self.c_o,
            'o_e': self.o_e,
            'description': self.description,
            'recommendation': self.recommendation,
            'lab_results': self.lab_results,
            'patient_id': self.patient_id.id,
        })