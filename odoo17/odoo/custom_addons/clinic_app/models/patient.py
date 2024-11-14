from email.policy import default

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re
from dateutil.relativedelta import relativedelta



class Patient(models.Model):
    _name = 'clinic.patient'
    _description = 'Patient'
    _rec_name = 'full_name'

    full_name = fields.Char(required=True)
    # birth_date = fields.Date()
    history = fields.Html()
    image_ids = fields.One2many('clinic.image','patient_id', string='Images')
    address = fields.Text()
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], default='male')
    phone = fields.Char()
    age = fields.Integer()
    h_o = fields.Text(string='H/O')

    history_ids = fields.One2many('clinic.history',
                                  'patient_id')
    state = fields.Selection([
        ('check', 'Check'),
        ('recheck', 'Recheck'),
    ], default='check')

    def check_action(self):
        self.state = 'check'

    def recheck_action(self):
        self.state = 'recheck'

    @api.model
    def write(self, vals):
        if 'state' in vals:
            self.env['clinic.history'].create({
                'description': f"{vals['state']}",
                'patient_id': self.id
            }
            )
        res = super(Patient, self).write(vals)
        return res

    @api.onchange('phone')
    def _onchange_valid_phone(self):
        if self.phone:
            match = re.match('^(010|011|015|012)\d{8}$', self.phone)
            if not  match:
                raise ValidationError('please enter a valid number')


    @api.model
    def increase_age(self):
        patients = self.search([])
        for patient in patients:
            patient.age += 1

    def action_add_log_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('clinic_app.add_log_action')
        action['context'] = {
            'default_patient_id': self.id
        }
        return action


class History(models.Model):
    _name = 'clinic.history'
    _description = 'History'

    date = fields.Date(default=fields.Date.today())
    description = fields.Text()
    recommendation = fields.Text()
    c_o = fields.Text()
    o_e = fields.Text(string='O/E')
    lab_results = fields.Text()
    patient_id = fields.Many2one('clinic.patient')


class Image(models.Model):
    _name = 'clinic.image'

    image = fields.Image()
    date_taken = fields.Date(default=fields.Date.today())
    description = fields.Text()
    patient_id = fields.Many2one('clinic.patient')

