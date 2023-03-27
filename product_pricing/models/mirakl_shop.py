from odoo import fields , models , _
import logging
_logger = logging.getLogger(__name__)


class MiraklShops(models.Model):
    _name="mirakl.shops"
    _description="Mirakl Marketplace Shops"
    _rec_name="shop_name"

    shop_name=fields.Char("Shop Name")
    total_no_of_products=fields.Integer("Total Number of Products" , compute ="_compute_amazon_product_count")
    shop_code=fields.Char("Shop Code")
    # product_ids = product_model.search([("name", "=", product_name)])

    def mirakl_product_action(self):
        self.ensure_one()
        offers = self.env['mirakl.offers'].search([('shop_id', '=' , 'shop_code')])
        _logger.info("............  %r ,...........",offers)
        for offer in offers:
            product_ids=self.env['mirakl.product'].search([('product_sku','=',offer.product_sku)])
            if product_ids:
                pass
            else:
                vals = {
                    'mirakl_shop_id': offer.id,
                    'product_sku': offer.product_sku,
                    'price': offer.price
                }
            
                self.env['mirakl.product'].create(vals)
            

        return {
            'type': 'ir.actions.act_window',
            'name': _("%s's Products", self.shop_name),
            'view_mode': 'list,form',
            'res_model': 'mirakl.product',
            # 'context': {
            # },
            # 'domain': [('mirakl_shop_id', '=', self.id)],
        }
    
    def _compute_amazon_product_count(self):
        for rec in self:
            total_no_of_products = self.env['mirakl.product'].search([('mirakl_shop_id', '=',rec.id)])
            rec.total_no_of_products=len(total_no_of_products)

    def product_pricing_action(self):
        self.ensure_one()
        return{
            'type':'ir.actions.act_window','type': 'ir.actions.act_window',
            'name': _("%s's Products", self.shop_name),
            'view_mode': 'list,form',
            'res_model': 'product.pricing',
            'domain': [('shop', '=', self.shop_name)],

        }
