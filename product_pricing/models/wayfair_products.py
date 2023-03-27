from odoo import fields, models,api
# import logging
# _logger = logging.getLogger(__name__)
import logging
_logger = logging.getLogger(__name__)


class WayfairProduct(models.Model):
    _name = "wayfair.product"
    _description = "Wayfair Product"
    _rec_name="supplier_part_number"

    supplier_part_number=fields.Char("SKU")
    brand_catalog=fields.Char("Brand Catalog")
    retail_price=fields.Char("Retail Price")
    status=fields.Char("Status")
    link=fields.Char("Link")
    wayfair_uk=fields.Char("Waifair UK" , invisible='0')
    wayfair_de=fields.Char("Wayfair DE" , invisible='0')
    wayfair_shop_id = fields.Many2one("wayfair.shops","Wayfair Shop")


    @api.model_create_multi
    def create(self, vals):
        res = super(WayfairProduct, self).create(vals)
        if res._context.get('import_file'):
            for product in res:
                wayfair_shop_id =self.env['wayfair.shops'].search([('shop_name','=',product.brand_catalog)])
                product.wayfair_shop_id = wayfair_shop_id.id

                _logger.info("............  %r ,...........",product.brand_catalog)
                if product.brand_catalog == "Wayfair UK":
                    product.wayfair_de=False
                else:
                    product.wayfair_uk=False
        return res
            
            