from odoo import fields, models, _ 


class WayfairShop(models.Model):
    _name = "wayfair.shops"
    _description = "Wayfair"
    _rec_name="shop_name"

    shop_name=fields.Char("Shop Name")
    url=fields.Char("URL")
    total_no_of_products=fields.Integer("Total Number of Products" , compute='_compute_wayfair_product_count')

########################
#PRODUCT PRICING METHOD
########################

    def product_pricing_action(self):
        self.ensure_one()
        return{
            'type':'ir.actions.act_window','type': 'ir.actions.act_window',
            'name': _("%s's Products", self.shop_name),
            'view_mode': 'list,form',
            'res_model': 'product.pricing',
            'domain': [('shop', '=', self.shop_name)],

        }
    
########################
#PRODUCT lISTING METHOD
########################
    

    def wayfair_product_action(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _("%s's Products", self.shop_name),
            'view_mode': 'list,form',
            'res_model': 'wayfair.product',
            'context': {
            },
            'domain': [('wayfair_shop_id', '=', self.id)],
        } 
    

    def _compute_wayfair_product_count(self):
        for rec in self:
            total_no_of_products = self.env['wayfair.product'].search([('wayfair_shop_id', '=', rec.id)])
            rec.total_no_of_products=len(total_no_of_products)
