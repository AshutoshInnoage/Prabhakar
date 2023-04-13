from odoo import fields, models, _


class Check(models.Model):
    _name = "check.shops"
    _description = "check24 Shop"
    _rec_name="shop_name"

    shop_name=fields.Char("Shop Name")
    url=fields.Char("URL")
    total_no_of_products=fields.Integer("Total Number of Products", compute ="_compute_check_product_count")


    ########################
    # STOCK PRODUCT METHOD #
    ########################

    def mapping_check_products_stock(self):
        self.ensure_one()
        offers = self.env['check.product'].search([ ])

        for offer in offers:
            product_id = self.env['product.pricing'].search([('product_name','=',offer.sku)])
            if product_id :
                product_id = self.env['product.pricing'].create({
                    'product_name':offer.sku,
                    'price' : offer.price,
                    'shop' : self.shop_name,
                })
            else:
                product_id.price = offer.price

    def product_pricing_action(self):
        self.ensure_one()
        return{
            'type':'ir.actions.act_window','type': 'ir.actions.act_window',
            'name': _("%s's Products", self.shop_name),
            'view_mode': 'list,form',
            'res_model': 'product.pricing',
            'domain': [('shop', '=', self.shop_name)],
        }

##########################
# PRODUCT lISTING METHOD #
########################## 


    def check_product_action(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _("%s's Products", self.shop_name),
            'view_mode': 'list,form',
            'res_model': 'check.product',
        } 
    
#############
# TOTAL SKU #
#############


    def _compute_check_product_count(self):
        for rec in self:
            total_no_of_products = self.env['check.product'].search([('check_shop_id', '=', rec.id)])
            rec.total_no_of_products=len(total_no_of_products)

########################
# SHOP PRICING METHODS #
########################

    def product_shopp_action(self):
        self.ensure_one()
        self.product_shop_pricing()
        return{
            'type':'ir.actions.act_window','type': 'ir.actions.act_window',
            'name': _("%s's Products", self.shop_name),
            'view_mode': 'list,form',
            'res_model': 'product.shop',
            

        }
    
    def product_shop_pricing(self):
        recs=self.env['check.product'].search([("check_shop_id","=", self.id) ])
        for rec in recs:
            productShop_object=self.env['product.shop'].search([('sku','=',rec.sku)])
            if not productShop_object :
                productShop_object =  productShop_object.create({'sku': rec.sku})

            if productShop_object:
                if self.shop_name == "Check24":
                    productShop_object.check = rec.price
                
        return rec