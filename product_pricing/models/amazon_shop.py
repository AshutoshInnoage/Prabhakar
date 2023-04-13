from odoo import fields, models , _

class AmazonShop(models.Model):
    _name = "amazon.shops"
    _description = "Amazon shops"
    _rec_name="shop_name"

    shop_name=fields.Char("Shop Name")
    url=fields.Char("URL")
    total_no_of_products=fields.Integer("Total Number of Products", compute ="_compute_amazon_product_count" )

    ########################
    # STOCK PRODUCT METHOD #
    ######################## 

    def mapping_amazon_products_stock(self):
        self.ensure_one()
        offers = self.env['amazon.sku'].search([ ])
      
        for offer in offers :
            product_id = self.env['product.pricing'].search([('product_name','=',offer.vendor_sku)] , limit =1 )
            if product_id:
                product_id = self.env['product.pricing'].create({
                    'product_name': offer.vendor_sku,
                    'price': offer.list_price_with_tax,
                    'shop' : self.shop_name
                })
            else:
                product_id.price = offer.list_price_with_tax
 

    def product_pricing_action(self):
        self.ensure_one()
        return{
            'type':'ir.actions.act_window',
            'name': _("%s's Products", self.shop_name),
            'view_mode': 'list,form',
            'res_model': 'product.pricing',
            'domain': [('amazon_id', '=', self.id)],
        }

    ##########################
    # PRODUCT lISTING METHOD #
    ##########################   

    def amazon_sku_action(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _("%s's Products", self.shop_name),
            'view_mode': 'list,form',
            'res_model': 'amazon.sku',
            'domain': [('amazon_shop_id', '=', self.id)],
        }
    
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
        recs=self.env['amazon.sku'].search([("amazon_shop_id","=", self.id) ])
        for rec in recs:
            productShop_object=self.env['product.shop'].search([('sku','=',rec.vendor_sku)])
            if not productShop_object :
                productShop_object=  productShop_object.create({'sku': rec.vendor_sku})

            if productShop_object:
                if self.shop_name == "Amazon DE":
                    productShop_object.amazon_de = rec.list_price_with_tax
               
                if self.shop_name == "Amazon FR":
                    productShop_object.amazon_fr = rec.list_price_with_tax
                
                if self.shop_name == "Amazon UK":
                    productShop_object.amazon_uk = rec.list_price_with_tax

    #############
    # TOTAL SKU #
    #############
     
    def _compute_amazon_product_count(self):
        for rec in self:
            total_no_of_products = self.env['amazon.sku'].search([('amazon_shop_id', '=',rec.id)])
            rec.total_no_of_products=len(total_no_of_products)