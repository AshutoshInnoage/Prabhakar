from odoo import fields, models, _ 
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)


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


    
    def product_shop_pricing(self):
        recs=self.env['product.pricing'].search([("shop","=", self.shop_name) ])
        for rec in recs:
            productShop_object=self.env['product.shop'].search([('sku','=',rec.product_name)])
            if not productShop_object :
                productShop_object=  productShop_object.create({'sku': rec.product_name})

            if productShop_object:
                if self.shop_name == "Wayfair UK":
                    productShop_object.wayfair_uk = rec.price

                if self.shop_name == "Wayfair DE":
                    productShop_object.wayfair_de = rec.price
    
                
    def product_shopp_action(self):
        self.ensure_one()
        self.product_shop_pricing()
        return{
            'type':'ir.actions.act_window','type': 'ir.actions.act_window',
            'name': _("%s's Products", self.shop_name),
            'view_mode': 'list,form',
            'res_model': 'product.shop',
        }
        # return rec
        
    ##########################
    # PRODUCT lISTING METHOD #
    ##########################
    

    def wayfair_product_listing_action(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _("%s's Products", self.shop_name),
            'view_mode': 'list,form',
            'res_model': 'wayfair.product',
            'domain': [('wayfair_shop_id', '=', self.id),('is_odoo_product','=', True)],
        } 

    #############
    # TOTAL SKU #
    #############    

    def _compute_wayfair_product_count(self):
        for rec in self:
            total_no_of_products = self.env['wayfair.product'].search([('wayfair_shop_id', '=', rec.id),('is_odoo_product','=', True)])
            # _logger.info("........%r.......",len(total_no_of_products))
            rec.total_no_of_products=len(total_no_of_products)


    ########################
    # STOCK PRODUCT METHOD #
    ########################

    def mapping_wayfair_product_stock(self):
        self.ensure_one()
        offers = self.env['wayfair.product'].search([("wayfair_shop_id","=", self.id),('is_odoo_product','=', True)])
        _logger.info(">>>>>>>>>PRE....Offers........  %r ,...........",len(offers))

        for offer in offers :
            product_id = self.env['product.pricing'].search([('product_name','=',offer.supplier_part_number),('wayfair_id','=',self.id)], limit = 1)
            _logger.info(">>>>>>>>>PRE............  %r ,...........",len(product_id))
            if len(product_id)>= 1:
                found = False
                for product in product_id :
                    if product.create_date.date() == datetime.now().today().date():
                        product.price = offer.price
                        found = True
                        break
                    else:
                        found = False
                if not found:
                    product_id = self.env['product.pricing'].create({
                        'product_name' : offer.supplier_part_number,
                        'price' : offer.retail_price,
                        'shop': self.shop_name
                    })
            else :
                product_id = self.env['product.pricing'].create({
                            'product_name' : offer.supplier_part_number,
                            'price' : offer.retail_price,
                            'shop': self.shop_name
                        })
                _logger.info(">>>>>>>>>POST............  %r ,...........",len(product_id))
            _logger.info(">>>>>>>>>,...........")

    def product_pricing_action(self):
        self.ensure_one()
        return{
            'type':'ir.actions.act_window',
            'name': _("%s's Products", self.shop_name),
            'view_mode': 'list,form',
            'res_model': 'product.pricing',
            'domain': [('shop', '=', self.shop_name)],
            'context' : {'search_default_group_by_date': 1,'search_default_group_by_product': 1,}
        }


