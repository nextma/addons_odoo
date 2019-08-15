# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2017 Vertel AB (<http://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import models, fields, api, _
from odoo.exceptions import except_orm, Warning, RedirectWarning
from odoo import tools

from odoo.tools import float_compare
from odoo.addons import decimal_precision as dp


import math

import logging
_logger = logging.getLogger(__name__)

class purchase_order(models.Model):
    _inherit = 'purchase.order'

    @api.one
    def _calc_pallets(self):
        #raise Warning(self.order_line)
        #~ self.calc_pallets = 222
       self.calc_pallets = int(math.ceil(sum(self.order_line.mapped('calc_pallets')) + 0.0001))
    calc_pallets = fields.Integer(compute="_calc_pallets",string="Nombre de Pallets Total")
    
    
class sale_order(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, values):
        """Override default Odoo create function and extend."""
        res = super(sale_order,self).create(values)
        res.insert_data()
        return res
        
    # @api.multi
    # def write(self, values):
        # """Override default Odoo create function and extend."""
        # res = super(sale_order,self).write(values)
        # if values.get('order_line'):
            # self.client_order_ref = self.calc_pallets
        # return res
                
    # @api.multi
    # def action_confirm(self):
        # self.insert_data()
        # return super(sale_order,self).action_confirm()
        
    @api.multi
    def insert_data(self):
        order = self.env['sale.order'].search([('id','=',self.id)])
        if order :
            for line in order.order_line :
                    if line.product_id.pallet :
                        pos = -1
                        for lines in order.order_line:
                            pos += 1
                            if lines.product_id.id == line.product_id.pallet.id:                        
                                break;
                            
                        if self.order_line[pos].product_id.id == line.product_id.pallet.id:
                            self.order_line[pos].product_uom_qty += line.calc_pallets
                            #self.client_order_ref = 'ajout'
                        else :
                            vals = {'order_id': self.id ,
                            'product_id': line.product_id.pallet.id ,
                            'name': line.product_id.pallet.name , 
                            'product_uom_qty': line.calc_pallets ,
                            'price_unit': line.product_id.pallet.lst_price 
                            }
                            self.order_line += self.env['sale.order.line'].new(vals)

    @api.one
    def _calc_pallets(self):
        #raise Warning(self.order_line)
        #~ self.calc_pallets = 222
        self.calc_pallets = int(self.order_line.calc_pallets)
    
    calc_pallets = fields.Integer(compute="_calc_pallets",string="Nombre de Pallets Total")
    
    

class sale_order_line(models.Model):  
    _inherit = 'sale.order.line'
    
    @api.one
    def _calc_pallets(self):
        if self.product_id.categ_id.name == 'Pallet':
            self.calc_pallets = 0
        else :
            self.calc_pallets = self.product_id.get_calc_pallets(self.product_uom_qty)
        
    pallet = fields.Many2one('product.product','Pallet',related="product_id.pallet")
    calc_pallets = fields.Float(compute="_calc_pallets",string="Nombre de Pallet")

class purchase_order_line(models.Model):  
    _inherit = 'purchase.order.line'
    
    @api.one
    def _calc_pallets(self):
        self.calc_pallets = self.product_id.get_calc_pallets(self.product_qty)


    calc_pallets = fields.Float(compute="_calc_pallets",string="Nombre de Pallet")

class product_product(models.Model):  
    _inherit = 'product.product'

    qty_par_pallet = fields.Integer('Quantite par pallet ',readonly=False)
    type_pallet = fields.Selection([('pallet1','Pallet1'),('type2','Type2'),('type3','Type3')],string='Type de Pallet')
    pallet = fields.Many2one('product.product',string='Pallet',readonly=False)
    category_id = fields.Char('pallet category id ',compute='get_categorie_pallet_id')
    
    @api.multi
    def get_pallet(self):
        return self.pallet.id   
        
    @api.one
    def get_categorie_pallet_id(self):
        cat = self.env['product.category'].sudo().search([('name','=','Pallet')])
        if cat:
            self.category_id = cat.id

            
        
    
    @api.multi
    def get_calc_pallets(self,product_qty):
        pallets = 0
        pallet = self.packaging_ids.filtered(lambda p: p.ul_container.type == 'pallet').mapped('calc_pallets')
        #pallet.sort()
        if self.qty_par_pallet > 0:
            pallets = int(round(product_qty  / self.qty_par_pallet))
        else:
            pallets = int(product_qty)
        return pallets
        


class product_packaging(models.Model):  
    _inherit = 'product.packaging'

    @api.one
    def _calc_pallets(self):
        self.calc_pallets = self.qty * self.ul_qty * self.rows
    calc_pallets = fields.Float(compute="_calc_pallets")

class stock_picking(models.Model):  
    _inherit = 'stock.picking'

    @api.one
    def _calc_pallets(self):
        self.calc_pallets = int(math.ceil(sum(self.move_lines.mapped('calc_pallets')) + 0.0001))
    calc_pallets = fields.Float(compute="_calc_pallets")


class stock_move(models.Model):  
    _inherit = 'stock.move'

    calc_pallets = fields.Float(related="purchase_line_id.calc_pallets")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: