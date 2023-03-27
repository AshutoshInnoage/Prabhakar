from odoo import fields, models , _

class AmazonShop(models.Model):
    _name = "amazon.shops"
    _description = "Amazon shops"
    _rec_name="shop_name"

    shop_name=fields.Char("Shop Name")
    url=fields.Char("URL")
    total_no_of_products=fields.Integer("Total Number of Products", compute ="_compute_amazon_product_count" )

    # FOR ALL PRODUCTS 

    def product_pricing_action(self):
        self.ensure_one()
        return{
            'type':'ir.actions.act_window',
            'name': _("%s's Products", self.shop_name),
            'view_mode': 'list,form',
            'res_model': 'product.pricing',
            # 'domain': [('shop_name', '=', self.id)],
            'domain': [('amazon_id', '=', self.id)],

        
        }

        pass

    def amazon_sku_action(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _("%s's Products", self.shop_name),
            'view_mode': 'list,form',
            'res_model': 'amazon.sku',
            'domain': [('amazon_shop_id', '=', self.id)],

            
        }
    
    
    def _compute_amazon_product_count(self):
        for rec in self:
            total_no_of_products = self.env['amazon.sku'].search([('amazon_shop_id', '=',rec.id)])
            rec.total_no_of_products=len(total_no_of_products)