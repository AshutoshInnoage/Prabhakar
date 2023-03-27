from odoo import fields, models, _


class ManoManoShop(models.Model):
    _name = "manomano.shops"
    _description = "ManoMano Shops"
    _rec_name="shop_name"

    shop_name=fields.Char("Shop Name")
    url=fields.Char("URL")
    total_no_of_products=fields.Integer("Total Number of Products" , compute ="_compute_mano_product_count")

    

    # def manomano_productlisting_action(self):
    #    action = self.env.ref('product_pricing.manomano_productlisting_action').read()[0]
    #    return action  

    def product_pricing_action(self):
        self.ensure_one()
        return{
            'type':'ir.actions.act_window','type': 'ir.actions.act_window',
            'name': _("%s's Products", self.shop_name),
            'view_mode': 'list,form',
            'res_model': 'product.pricing',
            'domain': [('shop', '=', self.shop_name)],

        }

    

    def mano_product_action(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _("%s's Products", self.shop_name),
            'view_mode': 'list,form',
            'res_model': 'manomano.productlisting',
            
        }
    def _compute_mano_product_count(self):
        for rec in self:
            total_no_of_products = self.env['manomano.productlisting'].search([('manomano_shop_id', '=', rec.id)])
            rec.total_no_of_products=len(total_no_of_products)