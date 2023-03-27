from odoo import fields , models , _
import logging
_logger = logging.getLogger(__name__)


class CDiscount(models.Model):
    _name="cdiscount.shops"
    _description="CDiscount Shops"
    _rec_name="shop_name"

    shop_name=fields.Char("Shop Name")
    total_no_of_products=fields.Integer("Total Number of Products")

    def product_pricing_action(self):
        self.ensure_one()
        return{
            'type':'ir.actions.act_window','type': 'ir.actions.act_window',
            'name': _("%s's Products", self.shop_name),
            'view_mode': 'list,form',
            'res_model': 'product.pricing',
            'domain': [('shop', '=', self.shop_name)],

        }

    def cdiscount_product_action(self):
        self.ensure_one()
        products = self.env['cdiscount.product'].search([])
        _logger.info("............  %r ,...........",products)
        for product in products:
        
            vals = {
                'cdiscount_shop_id': product.id,
                'product_sku': product.product_sku,
                'price': product.price
            }
        
            self.env['cdiscount.product'].create(vals)
            

        return {
            'type': 'ir.actions.act_window',
            'name': _("%s's Products", self.shop_name),
            'view_mode': 'list,form',
            'res_model': 'cdiscount.product',
            
        }