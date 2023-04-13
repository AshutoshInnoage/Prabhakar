from odoo import fields , models , _
import logging
from datetime import datetime
_logger = logging.getLogger(__name__)


class MiraklShops(models.Model):
    _name="mirakl.shops"
    _description="Mirakl Marketplace Shops"
    _rec_name="shop_name"

    shop_name=fields.Char("Shop Name")
    total_no_of_products=fields.Integer("Total Number of Products" , compute ="_compute_mirakl_product_count")
    mirakl_shop_id=fields.Many2one("shop.integrator","Shop" , required=True)

    ##########################
    # PRODUCT LISTING METHOD #
    ##########################

    def mirakl_product_action(self):
        for rec in self:
            rec.mirakl_shop_id.mirakl_inventory_offers()   
            if rec.mirakl_shop_id:

                           
                offers = self.env['mirakl.offers'].search([('shop_id','=',rec.id)])
                # _logger.info(">PRE............  %r ,...........",len(offers))

                for offer in offers:
                    
                    product_id=self.env['mirakl.product'].search([('product_sku','=',offer.product_id.default_code), ('mirakl_shop_id', '=', rec.id)], limit=1)
                    if not product_id:
                        product_id = rec.env['mirakl.product'].create({
                            'product_sku': offer.product_id.default_code,
                            'price': offer.price,
                            'on_shop_quantity': offer.quantity,
                            'mirakl_shop_id': rec.id,
                        })
                    else:
                        product_id.on_shop_quantity = offer.quantity
                        product_id.price = offer.price 
                count=self.env['mirakl.product'].search([('mirakl_shop_id','=',rec.id)])
            else:
                pass
                # _logger.info(">>POST>.....count.......  %r ,...........",count)


    def product_listing_action(self):
        self.ensure_one()
        return {
                'type': 'ir.actions.act_window',                                            
                'name': _("%s's Products", self.shop_name),
                'view_mode': 'list,form',
                'res_model': 'mirakl.product',
                'domain': [('mirakl_shop_id', '=', self.id)],
                # 'context' : {'search_default_group_by_date': 1,'search_default_group_by_product': 1,}
            }

    #############
    # TOTAL SKU #
    #############

    def _compute_mirakl_product_count(self):
        for rec in self:
            if rec.mirakl_shop_id:
                total_no_of_products = self.env['mirakl.product'].search([('mirakl_shop_id', '=',rec.id)])
                rec.total_no_of_products=len(total_no_of_products)
            else: 
                pass

    ########################
    # STOCK PRODUCT METHOD #
    ########################

    

    def mirakl_product_mapping_action(self):
        self.ensure_one()
        self.mirakl_shop_id.mirakl_inventory_offers()                       
        offers = self.env['mirakl.offers'].search([('shop_id','=',self.mirakl_shop_id.id)])
        _logger.info("Product Pricing Updated ~~~~~~~~~~~~~~ %r ",offers)

        for offer in offers:
            product_id=self.env['product.pricing'].search([('product_name','=',offer.product_id.default_code), ('mirakl_id', '=', self.id)])
            if len(product_id) >= 1:
                for product in product_id:
                    if product.create_date.date() == datetime.now().today().date():
                        product.price = offer.price
                        product.on_shop_quantity = offer.quantity
                        _logger.info("Product Pricing Updated ~~~~~~~~~~~~~~ %r ",product_id)
                   
                    else:
                        product_id = self.env['product.pricing'].create({
                                    'product_name': offer.product_id.default_code,
                                    'price': offer.price,
                                    'on_shop_quantity': offer.quantity,
                                    'shop' : self.shop_name,
                                    'mirakl_id': self.id,
                                })        
                        _logger.info("Product Pricing Created ~~~~~~~~~~~~~~ %r~~~~~~",product_id)


    
    def product_priciing_action(self):
        self.ensure_one()
        return{
            'type':'ir.actions.act_window',
            'name': _("%s's Products", self.shop_name),
            'view_mode': 'list,form',
            'res_model': 'product.pricing',
            'domain': [('mirakl_id', '=', self.id)],
            'context' : {'search_default_group_by_date': 1,'search_default_group_by_product': 1,}
        }
    

    ###########################
    # PRODUCT PRICING METHODS #
    ###########################

    def map_product_listing(self):
            self.ensure_one()
            self.product_shop_pricing()
            return{
                'type':'ir.actions.act_window',
                'name': _("%s's Products", self.shop_name),
                'view_mode': 'list,form',
                'res_model': 'product.shop',
            }

    def product_shop_pricing(self):
            self.ensure_one()
            self.mirakl_product_action()
            
            recs=self.env['mirakl.product'].search([("mirakl_shop_id","=", self.id)])
            for rec in recs:
                productShop_object=self.env['product.shop'].search([('sku','=',rec.product_sku)])
                _logger.info("~~~~~~PRO~~~~~~~%r~~~~~~~~~~~",productShop_object)
                found = False
                if productShop_object:
                    for product in productShop_object:
                        if product.create_date == datetime.now().today().date():
                            if self.shop_name == "Maison":
                                productShop_object.maison = rec.price

                            if self.shop_name == "Conforama":
                                productShop_object.conforama = rec.price

                            if self.shop_name == "Bricoprive":
                                productShop_object.bricoprive = rec.price

                            if self.shop_name == "Home24 DE":
                                productShop_object.home24_de = rec.price
                            
                            if self.shop_name == "Pccomponentes":
                                productShop_object.pccomponentes = rec.price
                            
                            if self.shop_name == "Rueduco":
                                productShop_object.rueduco = rec.price
                            
                            if self.shop_name == "Carrefoures":
                                productShop_object.carrefoures = rec.price
                            
                            if self.shop_name == "Adeo":
                                productShop_object.adeo = rec.price
                            
                            if self.shop_name == "Leclerc":
                                productShop_object.leclerc = rec.price
                            
                            if self.shop_name == "Carrefourfr":
                                productShop_object.carrefourfr = rec.price
                            
                            if self.shop_name == "But":
                                productShop_object.but = rec.price
                            
                            if self.shop_name == "Empik Place":
                                productShop_object.empik_place = rec.price
                            
                            if self.shop_name == "INNO":
                                productShop_object.inno = rec.price
                            
                            if self.shop_name == "VenteUnique":
                                productShop_object.vente_unique = rec.price
                            
                            if self.shop_name == "Worten":
                                productShop_object.worten = rec.price
                            
                            if self.shop_name == "Home24 AT":
                                productShop_object.home24_at = rec.price
                            
                            if self.shop_name == "Home24 FR":
                                productShop_object.home24_fr = rec.price
                            
                            if self.shop_name == "Darty":
                                productShop_object.darty = rec.price
                            
                            if self.shop_name == "VenteUnique ES":
                                productShop_object.vente_unique_es = rec.price
                            
                            if self.shop_name == "VenteUnique IT":
                                productShop_object.vente_unique_it = rec.price
                            
                            if self.shop_name == "ClubeFashion":
                                productShop_object.clube_fashion = rec.price
                            found = True
                            product.write({
                                'price' : rec.price,
                            })
                            break
                if not found:
                    product_id = productShop_object.create({
                        "sku": rec.product_sku,
                        # "price": rec.price
                    })
                    if product_id:
                        if self.shop_name == "Maison":
                            productShop_object.maison = rec.price

                        if self.shop_name == "Conforama":
                            productShop_object.conforama = rec.price

                        if self.shop_name == "Bricoprive":
                            productShop_object.bricoprive = rec.price

                        if self.shop_name == "Home24 DE":
                            productShop_object.home24_de = rec.price
                        
                        if self.shop_name == "Pccomponentes":
                            productShop_object.pccomponentes = rec.price
                        
                        if self.shop_name == "Rueduco":
                            productShop_object.rueduco = rec.price
                        
                        if self.shop_name == "Carrefoures":
                            productShop_object.carrefoures = rec.price
                        
                        if self.shop_name == "Adeo":
                            productShop_object.adeo = rec.price
                        
                        if self.shop_name == "Leclerc":
                            productShop_object.leclerc = rec.price
                        
                        if self.shop_name == "Carrefourfr":
                            productShop_object.carrefourfr = rec.price
                        
                        if self.shop_name == "But":
                            productShop_object.but = rec.price
                        
                        if self.shop_name == "Empik Place":
                            productShop_object.empik_place = rec.price
                        
                        if self.shop_name == "INNO":
                            productShop_object.inno = rec.price
                        
                        if self.shop_name == "VenteUnique":
                            productShop_object.vente_unique = rec.price
                        
                        if self.shop_name == "Worten":
                            productShop_object.worten = rec.price
                        
                        if self.shop_name == "Home24 AT":
                            productShop_object.home24_at = rec.price
                        
                        if self.shop_name == "Home24 FR":
                            productShop_object.home24_fr = rec.price
                        
                        if self.shop_name == "Darty":
                            productShop_object.darty = rec.price
                        
                        if self.shop_name == "VenteUnique ES":
                            productShop_object.vente_unique_es = rec.price
                        
                        if self.shop_name == "VenteUnique IT":
                            productShop_object.vente_unique_it = rec.price
                        
                        if self.shop_name == "ClubeFashion":
                            productShop_object.clube_fashion = rec.price
                # _logger.info(">>>>>>>>>>>>>>...........  %r .........", productShop_object)
                # _logger.info(">>>>>>>>>>>>>>...........  %r .........", rec.mirakl_shop_id)


    ########################
    # PRODUCT LISTING CRON #
    ######################## 

    def product_listing_cron(self):
        shops = self.env['mirakl.shops'].search([ ])
        for shop in shops:
            shop.mirakl_product_action()
    
        shops = self.env['cdiscount.shops'].search([ ])
        for shop in shops:
            shop.cdiscount_product_action()



  
    




