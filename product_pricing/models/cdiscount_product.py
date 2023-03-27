from odoo import fields, models,api
import logging
_logger = logging.getLogger(__name__)

class MiraklProduct(models.Model):
    _name = "cdiscount.product"
    _description = "CDiscount Products"
    _rec_name="product_sku"

    product_sku=fields.Char("Product SKU")
    price=fields.Integer("Price")
    cdiscount_shop_id = fields.Many2one("manomano.productlisting","CDiscount Shop ID")
    link=fields.Char("Product URL")
    status=fields.Char("Status")

