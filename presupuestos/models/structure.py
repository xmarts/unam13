# -*- coding: utf-8 -*-
# Copyright YEAR(S), AUTHOR(S)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date, timedelta
import tempfile
import base64
import os
import binascii
import xlrd
from random import randint

class BudgetStructure(models.Model):#modelo para Orden del código programático.
    _name = 'budget.structure'
    _description = 'Orden Programatico'

    sequence = fields.Char(string="Secuencia",required=True)
    name = fields.Char(string="Nombre",required=True)
    catalog_id = fields.Many2one('ir.model',string="Catálogo")
    to_search_field = fields.Many2one('ir.model.fields',string="Campo a buscar", help="Colocar nombre tecnico del campo a comparar en el modelo, por ejemplo 'code'")
    position_from  = fields.Integer(string='Posición inicial',required=True)
    position_to  = fields.Integer(string="Posición final",required=True)
    code_part_pro = fields.Boolean(string="Forma parte del codigo programático")
    is_year = fields.Boolean(
        string='Año',
        default=False
    )
    is_check_digit = fields.Boolean(
        string='Digito verificador',
        default=False
    )
    is_authorized_budget = fields.Boolean(
        string='Presupuesto Autorizado',
        default=False
    )
    is_asigned_budget = fields.Boolean(
        string='Presupuesto Asignado',
        default=False
    )

    @api.onchange('catalog_id')
    def _onchange_catalog_id(self):
        self.to_search_field = ''

    @api.onchange('is_year','is_check_digit','is_authorized_budget','is_asigned_budget')
    def _onchange_is_fields(self):
        if self.is_year == True or self.is_check_digit == True or self.is_authorized_budget == True or self.is_asigned_budget == True:
            self.catalog_id = ''
            self.to_search_field = ''

    @api.constrains('is_year')
    def _check_year(self):
        if self.is_year == True:
            search = self.env['budget.structure'].search(
                [('is_year','=',True),('code_part_pro', '=',True),('id','!=',self.id)],limit=1)
            if search:
                raise ValidationError(_('Solo puede haber un año por orden programático'))  

    @api.constrains('is_check_digit')
    def _check_cd(self):
        if self.is_check_digit == True:
            search = self.env['budget.structure'].search(
                [('is_check_digit','=',True),('code_part_pro', '=',True),('id','!=',self.id)],limit=1)
            if search:
                raise ValidationError(_('Solo puede haber un digito verificador por orden programático'))   

    @api.constrains('is_authorized_budget')
    def _check_autb(self):
        if self.is_authorized_budget == True:
            search = self.env['budget.structure'].search(
                [('is_authorized_budget','=',True),('code_part_pro', '=',True),('id','!=',self.id)],limit=1)
            if search:
                raise ValidationError(_('Solo puede haber un presupuesto autorizado por orden programático'))   

    @api.constrains('is_asigned_budget')
    def _check_asigb(self):
        if self.is_asigned_budget == True:
            search = self.env['budget.structure'].search(
                [('is_asigned_budget','=',True),('code_part_pro', '=',True),('id','!=',self.id)],limit=1)
            if search:
                raise ValidationError(_('Solo puede haber un presupuesto asignado por orden programático'))   

    #funcion para autocompletar con un cero ala izquierda y validar que el codigo no se repirta y sea unico.
    @api.constrains('sequence')
    def _check_code(self):
        for obj in self: 
            val = obj.sequence

            if val.isdigit()==False:
                raise ValidationError(_('Valor Invalido'))
            if val.isdigit():
                search = self.env['budget.structure'].search(
                    [('catalog_id','=',self.catalog_id.id),('sequence', '!=', self.sequence)],limit=1)
                if search and self.catalog_id:
                    raise ValidationError(_('Catálogo duplicado, solo puede haber un registro por catálogo '))   

        rec = self.env['budget.structure'].search(
        [('sequence', '=', self.sequence),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único.'))

class BudgetStructureRecalendarization(models.Model):#modelo para Orden del código programático.
    _name = 'budget.structure.recalendarization'
    _description = 'Orden Programatico para Recalendarizacion'

    sequence = fields.Char(string="Secuencia",required=True)
    name = fields.Char(string="Nombre",required=True)
    catalog_id = fields.Many2one('ir.model',string="Catálogo")
    to_search_field = fields.Many2one('ir.model.fields',string="Campo a buscar", help="Colocar nombre tecnico del campo a comparar en el modelo, por ejemplo 'code'")
    position_from  = fields.Integer(string='Posición inicial',required=True)
    position_to  = fields.Integer(string="Posición final",required=True)
    code_part_pro = fields.Boolean(string="Forma parte del codigo programático")
    no_catalog = fields.Boolean(
        string='Sin Catalogo',
        default=False
    )
    is_year = fields.Boolean(
        string='Año',
        default=False
    )
    is_check_digit = fields.Boolean(
        string='Digito verificador',
        default=False
    )

    ####################################################################################################################################
    is_key = fields.Boolean(
        string='Es Clave ?',
        default=False
    )
    is_control_number = fields.Boolean(
        string='Es No de control ?',
        default=False
    )
    is_date = fields.Boolean(
        string='Es Fecha ?',
        default=False
    )
    is_authorizer = fields.Boolean(
        string='Es Autorizador ?',
        default=False
    )
    is_error = fields.Boolean(
        string='Es Error ?',
        default=False
    )
    is_agreement_number = fields.Boolean(
        string='Es No Convenio ?',
        default=False
    )
    is_type_exercise = fields.Boolean(
        string='Es Tipo Ejercicio ?',
        default=False
    )
    is_amount = fields.Boolean(
        string='Es Monto ?',
        default=False
    )
    is_cve_mov = fields.Boolean(
        string='Es Clave Movimiento?',
        default=False
    )
    is_number_doc = fields.Boolean(
        string='Es Folio ?',
        default=False
    )
    is_date_doc = fields.Boolean(
        string='Es Fecha Folio ?',
        default=False
    )



    ####################################################################################################################################

    @api.onchange('catalog_id')
    def _onchange_catalog_id(self):
        self.to_search_field = ''

    @api.onchange('is_year','is_check_digit','is_key','is_control_number','is_date','is_authorizer','is_error','is_agreement_number','is_type_exercise','is_amount','is_cve_mov','is_number_doc','is_date_doc')
    def _onchange_is_fields(self):
        if self.is_year == True or self.is_check_digit == True or self.is_key == True or self.is_control_number == True or self.is_date == True or self.is_authorizer == True or self.is_error == True or self.is_agreement_number == True or self.is_type_exercise == True or self.is_amount == True or self.is_cve_mov == True or self.is_number_doc == True or self.is_date_doc == True:
            self.catalog_id = ''
            self.to_search_field = ''
            self.no_catalog = True
        else:
        	self.no_catalog = False

    @api.constrains('is_year')
    def _check_year(self):
        if self.is_year == True:
            search = self.env['budget.structure.recalendarization'].search(
                [('is_year','=',True),('code_part_pro', '=',True),('id','!=',self.id)],limit=1)
            if search:
                raise ValidationError(_('Solo puede haber un año por orden programático'))  

    @api.constrains('is_check_digit')
    def _check_digit(self):
        if self.is_check_digit == True:
            search = self.env['budget.structure.recalendarization'].search(
                [('is_check_digit','=',True),('code_part_pro', '=',True),('id','!=',self.id)],limit=1)
            if search:
                raise ValidationError(_('Solo puede haber un digito verificador por orden programático'))  

    @api.constrains('is_key')
    def _check_key(self):
        if self.is_key == True:
            search = self.env['budget.structure.recalendarization'].search(
                [('is_key','=',True),('code_part_pro', '=',True),('id','!=',self.id)],limit=1)
            if search:
                raise ValidationError(_('Solo puede haber una calve por orden programático')) 

    @api.constrains('is_control_number')
    def _check_control_number(self):
        if self.is_control_number == True:
            search = self.env['budget.structure.recalendarization'].search(
                [('is_control_number','=',True),('code_part_pro', '=',True),('id','!=',self.id)],limit=1)
            if search:
                raise ValidationError(_('Solo puede haber un numero de control por orden programático')) 

    @api.constrains('is_date')
    def _check_date(self):
        if self.is_date == True:
            search = self.env['budget.structure.recalendarization'].search(
                [('is_date','=',True),('code_part_pro', '=',True),('id','!=',self.id)],limit=1)
            if search:
                raise ValidationError(_('Solo puede haber una fecha por orden programático')) 

    @api.constrains('is_authorizer')
    def _check_authorizer(self):
        if self.is_authorizer == True:
            search = self.env['budget.structure.recalendarization'].search(
                [('is_authorizer','=',True),('code_part_pro', '=',True),('id','!=',self.id)],limit=1)
            if search:
                raise ValidationError(_('Solo puede haber un autorizador por orden programático')) 

    @api.constrains('is_error')
    def _check_error(self):
        if self.is_error == True:
            search = self.env['budget.structure.recalendarization'].search(
                [('is_error','=',True),('code_part_pro', '=',True),('id','!=',self.id)],limit=1)
            if search:
                raise ValidationError(_('Solo puede haber un error por orden programático')) 

    @api.constrains('is_agreement_number')
    def _check_agree_number(self):
        if self.is_agreement_number == True:
            search = self.env['budget.structure.recalendarization'].search(
                [('is_agreement_number','=',True),('code_part_pro', '=',True),('id','!=',self.id)],limit=1)
            if search:
                raise ValidationError(_('Solo puede haber un convenio por orden programático')) 

    @api.constrains('is_type_exercise')
    def _check_type_ex(self):
        if self.is_type_exercise == True:
            search = self.env['budget.structure.recalendarization'].search(
                [('is_type_exercise','=',True),('code_part_pro', '=',True),('id','!=',self.id)],limit=1)
            if search:
                raise ValidationError(_('Solo puede haber un tipo por orden programático')) 

    @api.constrains('is_amount')
    def _check_amount(self):
        if self.is_amount == True:
            search = self.env['budget.structure.recalendarization'].search(
                [('is_amount','=',True),('code_part_pro', '=',True),('id','!=',self.id)],limit=1)
            if search:
                raise ValidationError(_('Solo puede haber un monto por orden programático')) 

    @api.constrains('is_cve_mov')
    def _check_cve_mov(self):
        if self.is_cve_mov == True:
            search = self.env['budget.structure.recalendarization'].search(
                [('is_cve_mov','=',True),('code_part_pro', '=',True),('id','!=',self.id)],limit=1)
            if search:
                raise ValidationError(_('Solo puede haber movimiento año por orden programático')) 

    @api.constrains('is_number_doc')
    def _check_numb_doc(self):
        if self.is_number_doc == True:
            search = self.env['budget.structure.recalendarization'].search(
                [('is_number_doc','=',True),('code_part_pro', '=',True),('id','!=',self.id)],limit=1)
            if search:
                raise ValidationError(_('Solo puede haber un folio por orden programático')) 

    @api.constrains('is_date_doc')
    def _check_date_doc(self):
        if self.is_date_doc == True:
            search = self.env['budget.structure.recalendarization'].search(
                [('is_date_doc','=',True),('code_part_pro', '=',True),('id','!=',self.id)],limit=1)
            if search:
                raise ValidationError(_('Solo puede haber una fecha de folio por orden programático')) 


    #funcion para autocompletar con un cero ala izquierda y validar que el codigo no se repirta y sea unico.
    @api.constrains('sequence')
    def _check_code(self):
        for obj in self: 
            val = obj.sequence

            if val.isdigit()==False:
                raise ValidationError(_('Valor Invalido'))
            if val.isdigit():
                search = self.env['budget.structure.recalendarization'].search(
                    [('catalog_id','=',self.catalog_id.id),('sequence', '!=', self.sequence)],limit=1)
                if search and self.catalog_id:
                    raise ValidationError(_('Catálogo duplicado, solo puede haber un registro por catálogo '))   

        rec = self.env['budget.structure.recalendarization'].search(
        [('sequence', '=', self.sequence),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único para la estructura de racalendarizacion.'))


class BudgetStructure(models.Model):#modelo para Orden del código programático.
    _name = 'budget.structure.adjustement'
    _description = 'Orden Programatico Adecuaciones'

    sequence = fields.Char(string="Secuencia",required=True)
    name = fields.Char(string="Nombre",required=True)
    catalog_id = fields.Many2one('ir.model',string="Catálogo")
    to_search_field = fields.Many2one('ir.model.fields',string="Campo a buscar", help="Colocar nombre tecnico del campo a comparar en el modelo, por ejemplo 'code'")
    position_from  = fields.Integer(string='Posición inicial',required=True)
    position_to  = fields.Integer(string="Posición final",required=True)
    code_part_pro = fields.Boolean(string="Forma parte del codigo programático")
    is_more_less  = fields.Selection(
        [('na','No Aplica'),('a','Aumento'),('r','Reduccion')],
        string='Es aumento o reduccion ?',
        default = 'na'
    )
    no_catalog = fields.Boolean(
        string='Sin Catalogo',
        default=False
    )
    is_year = fields.Boolean(
        string='Año',
        default=False
    )
    is_check_digit = fields.Boolean(
        string='Digito verificador',
        default=False
    )

    ####################################################################################################################################
    is_key = fields.Boolean(
        string='Es Clave ?',
        default=False
    )
    is_control_number = fields.Boolean(
        string='Es No de control ?',
        default=False
    )
    is_date = fields.Boolean(
        string='Es Fecha ?',
        default=False
    )
    is_authorizer = fields.Boolean(
        string='Es Autorizador ?',
        default=False
    )
    is_error = fields.Boolean(
        string='Es Error ?',
        default=False
    )
    is_agreement_number = fields.Boolean(
        string='Es No Convenio ?',
        default=False
    )
    is_type_exercise = fields.Boolean(
        string='Es Tipo Ejercicio ?',
        default=False
    )
    is_amount = fields.Boolean(
        string='Es Monto ?',
        default=False
    )
    is_cve_mov = fields.Boolean(
        string='Es Clave Movimiento?',
        default=False
    )
    is_number_doc = fields.Boolean(
        string='Es Folio ?',
        default=False
    )
    is_date_doc = fields.Boolean(
        string='Es Fecha Folio ?',
        default=False
    )



    ####################################################################################################################################

    @api.onchange('catalog_id')
    def _onchange_catalog_id(self):
        self.to_search_field = ''

    @api.onchange('is_year','is_check_digit','is_key','is_control_number','is_date','is_authorizer','is_error','is_agreement_number','is_type_exercise','is_amount','is_cve_mov','is_number_doc','is_date_doc')
    def _onchange_is_fields(self):
        if self.is_year == True or self.is_check_digit == True or self.is_key == True or self.is_control_number == True or self.is_date == True or self.is_authorizer == True or self.is_error == True or self.is_agreement_number == True or self.is_type_exercise == True or self.is_amount == True or self.is_cve_mov == True or self.is_number_doc == True or self.is_date_doc == True:
            self.catalog_id = ''
            self.to_search_field = ''
            self.is_more_less = 'na'
            self.no_catalog = True
        else:
            self.no_catalog = False

    @api.constrains('is_year')
    def _check_year(self):
        if self.is_year == True:
            search = self.env['budget.structure.adjustement'].search(
                [('is_year','=',True),('code_part_pro', '=',True),('id','!=',self.id)],limit=1)
            if search:
                raise ValidationError(_('Solo puede haber un año por orden programático'))  

    @api.constrains('is_check_digit')
    def _check_digit(self):
        if self.is_check_digit == True:
            search = self.env['budget.structure.adjustement'].search(
                [('is_check_digit','=',True),('code_part_pro', '=',True),('id','!=',self.id),('is_more_less','=',self.is_more_less)],limit=1)
            if search:
                raise ValidationError(_('Solo puede haber un digito verificador por orden programático'))  

    @api.constrains('is_key')
    def _check_key(self):
        if self.is_key == True:
            search = self.env['budget.structure.adjustement'].search(
                [('is_key','=',True),('code_part_pro', '=',True),('id','!=',self.id)],limit=1)
            if search:
                raise ValidationError(_('Solo puede haber una clave por orden programático')) 

    @api.constrains('is_control_number')
    def _check_control_number(self):
        if self.is_control_number == True:
            search = self.env['budget.structure.adjustement'].search(
                [('is_control_number','=',True),('code_part_pro', '=',True),('id','!=',self.id)],limit=1)
            if search:
                raise ValidationError(_('Solo puede haber un numero de control por orden programático')) 

    @api.constrains('is_date')
    def _check_date(self):
        if self.is_date == True:
            search = self.env['budget.structure.adjustement'].search(
                [('is_date','=',True),('code_part_pro', '=',True),('id','!=',self.id)],limit=1)
            if search:
                raise ValidationError(_('Solo puede haber una fecha por orden programático')) 

    @api.constrains('is_authorizer')
    def _check_authorizer(self):
        if self.is_authorizer == True:
            search = self.env['budget.structure.adjustement'].search(
                [('is_authorizer','=',True),('code_part_pro', '=',True),('id','!=',self.id)],limit=1)
            if search:
                raise ValidationError(_('Solo puede haber un autorizador por orden programático')) 

    @api.constrains('is_error')
    def _check_error(self):
        if self.is_error == True:
            search = self.env['budget.structure.adjustement'].search(
                [('is_error','=',True),('code_part_pro', '=',True),('id','!=',self.id)],limit=1)
            if search:
                raise ValidationError(_('Solo puede haber un error por orden programático')) 

    @api.constrains('is_agreement_number')
    def _check_agree_number(self):
        if self.is_agreement_number == True:
            search = self.env['budget.structure.adjustement'].search(
                [('is_agreement_number','=',True),('code_part_pro', '=',True),('id','!=',self.id),('is_more_less','=',self.is_more_less)],limit=1)
            if search:
                raise ValidationError(_('Solo puede haber un convenio por orden programático')) 

    @api.constrains('is_type_exercise')
    def _check_type_ex(self):
        if self.is_type_exercise == True:
            search = self.env['budget.structure.adjustement'].search(
                [('is_type_exercise','=',True),('code_part_pro', '=',True),('id','!=',self.id),('is_more_less','=',self.is_more_less)],limit=1)
            if search:
                raise ValidationError(_('Solo puede haber un tipo por orden programático')) 

    @api.constrains('is_amount')
    def _check_amount(self):
        if self.is_amount == True:
            search = self.env['budget.structure.adjustement'].search(
                [('is_amount','=',True),('code_part_pro', '=',True),('id','!=',self.id)],limit=1)
            if search:
                raise ValidationError(_('Solo puede haber un monto por orden programático')) 

    @api.constrains('is_cve_mov')
    def _check_cve_mov(self):
        if self.is_cve_mov == True:
            search = self.env['budget.structure.adjustement'].search(
                [('is_cve_mov','=',True),('code_part_pro', '=',True),('id','!=',self.id)],limit=1)
            if search:
                raise ValidationError(_('Solo puede haber movimiento año por orden programático')) 

    @api.constrains('is_number_doc')
    def _check_numb_doc(self):
        if self.is_number_doc == True:
            search = self.env['budget.structure.adjustement'].search(
                [('is_number_doc','=',True),('code_part_pro', '=',True),('id','!=',self.id)],limit=1)
            if search:
                raise ValidationError(_('Solo puede haber un folio por orden programático')) 

    @api.constrains('is_date_doc')
    def _check_date_doc(self):
        if self.is_date_doc == True:
            search = self.env['budget.structure.adjustement'].search(
                [('is_date_doc','=',True),('code_part_pro', '=',True),('id','!=',self.id)],limit=1)
            if search:
                raise ValidationError(_('Solo puede haber una fecha de folio por orden programático')) 


    #funcion para autocompletar con un cero ala izquierda y validar que el codigo no se repirta y sea unico.
    @api.constrains('sequence')
    def _check_code(self):
        for obj in self: 
            val = obj.sequence

            if val.isdigit()==False:
                raise ValidationError(_('Valor Invalido'))
            if val.isdigit():
                search = self.env['budget.structure.adjustement'].search(
                    [('catalog_id','=',self.catalog_id.id),('sequence', '!=', self.sequence),('position_from','=',self.position_from),('position_to','=',self.position_to),('is_more_less','=',self.is_more_less)],limit=1)
                if search and self.catalog_id:
                    raise ValidationError(_('Catálogo duplicado, solo puede haber un registro por catálogo '))   

        rec = self.env['budget.structure.adjustement'].search(
        [('sequence', '=', self.sequence),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único para la estructura de adecuacion.'))