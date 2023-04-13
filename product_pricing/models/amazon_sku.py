from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)

class AmazonSKU(models.Model):
    _name = "amazon.sku"
    _description = "Amazon SKU"
    _rec_name="vendor_sku"

    vendor_sku=fields.Char("Vendor SKU")
    list_price_currency=fields.Char("List Price Currency")
    list_price_with_tax=fields.Char("List Price with Tax")
    cost_price=fields.Char("Cost Price")
    cost_price_currency=fields.Char("Cost Price Currency")
    amazon_shop_id = fields.Many2one("amazon.shops")
    product_url=fields.Char("Product URL")
    merchant_suggested_asin=fields.Char("Merchant Suggested Asin")
    
    @api.model_create_multi
    def create(self, vals):
        res = super(AmazonSKU, self).create(vals)
        if res._context.get('import_file'):
            for product in res:
                amazon_shop_id =self.env['amazon.shops'].search([('id', '=', res._context.get('active_id'))])
                product.amazon_shop_id = amazon_shop_id.id
                if product.amazon_shop_id.url:
                    # _logger.info("............  %r ,.....%r......",product.merchant_suggested_asin, product.amazon_shop_id.url)
                    product.product_url = product.amazon_shop_id.url + product.merchant_suggested_asin
        return res
    
