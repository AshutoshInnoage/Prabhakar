from odoo import fields, models, _


class Check(models.Model):
    _name = "check.shops"
    _description = "check24 Shop"
    _rec_name="shop_name"

    shop_name=fields.Char("Shop Name")
    url=fields.Char("URL")
    total_no_of_products=fields.Integer("Total Number of Products", compute ="_compute_check_product_count")

    def product_pricing_action(self):
        self.ensure_one()
        return{
            'type':'ir.actions.act_window','type': 'ir.actions.act_window',
            'name': _("%s's Products", self.shop_name),
            'view_mode': 'list,form',
            'res_model': 'product.pricing',
            'domain': [('shop', '=', self.shop_name)],

        }

    def check_product_action(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _("%s's Products", self.shop_name),
            'view_mode': 'list,form',
            'res_model': 'check.product',
        } 
    def _compute_check_product_count(self):
        for rec in self:
            total_no_of_products = self.env['check.product'].search([('check_shop_id', '=', rec.id)])
            rec.total_no_of_products=len(total_no_of_products)