from odoo import models, fields, api

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    name = fields.Char(required=True)
    user_id = fields.Many2one('res.users', string='Salesperson')
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=fields.Date.today)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    property_type_id = fields.Many2one('estate.property.type')
    tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    state = fields.Selection(
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        required=True,
        default='new'
    )
    invoice_id = fields.Many2one('account.move', string='Invoice', readonly=True)

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    best_price = fields.Float(compute='_compute_best_price')

    def write(self, vals):
        if 'state' in vals and vals['state'] == 'sold':
            # Ajoutez ici l'action que vous souhaitez déclencher lorsque l'état passe à 'sold'
            self._action_on_sold()
        return super(EstateProperty, self).write(vals)

    def _action_on_sold(self):
        # Exemple d'action : créer une facture
        for property in self:
            invoice = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': property.user_id.partner_id.id,
                'invoice_line_ids': [(0, 0, {
                    'name': property.name,
                    'quantity': 1,
                    'price_unit': property.selling_price,
                })],
            })
            property.invoice_id = invoice.id

    def action_redirect_to_internal_module(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Internal Module',
            'res_model': 'internal.module.model',  # Remplacez par le modèle du module interne
            'view_mode': 'tree,form',
            'target': 'current',
        }