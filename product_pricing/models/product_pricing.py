from odoo import fields, models , api
import logging
_logger = logging.getLogger(__name__)

class ProductPricing(models.Model):
    _name = "product.pricing"
    _description = "Product Pricing Analysis"
    _rec_name="product_name"
    # _inherit="amazon.sku"

       
    product_name=fields.Char("Product")
    shop=fields.Char("Shop")
    price=fields.Char("Price")
    dicount=fields.Float("Discount")
    standard=fields.Float("Standard")
    # record = fields.Reference(string='Record', selection='_get_model_selection')


    amazon_id=fields.Many2one("amazon.shops" , "Amazon Shop")
    wayfair_id=fields.Many2one("wayfair.shops" , "Wayfair Shop")
    cdiscount_id=fields.Many2one("cdiscount.shops" , "Cdiscount Shop")
    check_id=fields.Many2one("check.shops" , "Check24 Shop")
    mirakl_id=fields.Many2one("mirakl.shops" , "Mirakl Shop")
    manomano_id=fields.Many2one("manomano.shops" , "Manomano Shop")

    # def _get_model_selection(self):
    #     models = self.env['ir.model'].search([])
    #     return [(model.model, model.name) for model in models]
    
    @api.model_create_multi
    def create(self, vals):
        res = super(ProductPricing, self).create(vals)
        if res._context.get('import_file'):
            shop_id =self.env[res._context.get("active_model")].search([('id','=', res._context.get("active_id"))])
            for product in res:
                _logger.info("............  %r ,...........",product.product_name )
                product.shop = shop_id.shop_name
                if res._context.get("active_model") == "amazon.shops":
                    product.amazon_id = shop_id
                elif res._context.get("active_model") == "wayfair.shops":
                    product.wayfair_id = shop_id                
                elif res._context.get("active_model") == "cdiscount.shops":
                    product.cdiscount_id = shop_id                
                elif res._context.get("active_model") == "check.shops":
                    product.check_id = shop_id                
                # elif res._context.get("active_model") == "wayfair_shops":
                #     product.wayfair_id = shop_id                
        return res



    