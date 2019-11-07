# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date, timedelta
import tempfile
import base64
import os
import binascii
import xlrd
from random import randint


class BudgetProgram(models.Model): #modleo para el programa
    _name = 'budget.program'
    _description = 'Programa'

    code = fields.Char(string='Código', required=True, size=2)
    name = fields.Char(string="Nombre", required=True)
    budget_subprogam_id = fields.Many2one('budget.subprogram', string="Subprograma")

    #funcion para autocompletar con un cero ala izquierda y validar que el codigo no se repirta y sea unico.
    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit():
                if len(val)<=1:
                    obj.code = '0'+obj.code
            else:
                raise ValidationError(_('Valor Invalido'))
        rec = self.env['budget.program'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único.'))

class BudgertSubprogram(models.Model):#se crea este modelo  SubPrograma (SP) con los siguientes campos 
    _name = 'budget.subprogram'
    _description = 'SubPrograma'

    code = fields.Char(string="Código", required=True, size=2)
    name = fields.Char(string="Nombre", required=True)

    #branch_id = fields.Many2one('res.branch',string="Dependencia",required=True,)
    subdependence_id = fields.Many2one('budget.subdependence',string="Subdependencia",required=True)
    program_id = fields.Many2one('budget.program',string="Programa",required=True)
    
    #funcion para autocompletar con un cero ala izquierda y validar que el codigo no se repirta y sea unico.
    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit():
                if len(val)<=1:
                    obj.code = '0'+obj.code
            else:
                raise ValidationError(_('Valor Invalido'))
        rec = self.env['budget.subprogram'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único.'))
###   VERIFICAR SI ES NECESARIO O NO CREAR MODELO BUDGET.DEPENDENCE    ###
#class campos_nuevos_branch(models.Model):#Este es un inherit al modelo del branch ,Dependencia (DEP).
#    _inherit = 'res.branch'
#    code = fields.Char(string="Código",required=True,size=3)
#    head = fields.Many2one('hr.employee',string="Titular",required=True)
#    secretary = fields.Many2one('hr.employee',string="Secretario Administrativo",required=True)#No_dependence = fields.Char(string="No. entidad o dependencia",required=True)
#    subdependence_id = fields.Many2one('budget.subdependence',string="Subdependencias")
#
#    #funcion para autocompletar con un cero ala izquierda y validar que el codigo no se repirta y sea unico.
#    @api.constrains('code')#def _check_code(self):
#        for obj in self: #val = obj.code
#            if val.isdigit():
#                if len(val)==1:
#                    obj.code = '00'+obj.code
#                if len(val)==2:
#                    obj.code = '0'+obj.code 
#            else:
#                raise ValidationError(_('Valor Invalido'))
#        rec = self.env['res.branch'].search(
#        [('code', '=', self.code),('id', '!=', self.id)])
#        if rec:

class  BudgetSubdependence(models.Model):#Modelo Subdependencia (SD)
    _name = 'budget.subdependence'
    _description = 'Subdepencencia'

    code = fields.Char(string="Código",required=True,size=2)
    name = fields.Char(string="Nombre",required=True)
#    branch_id = fields.Many2one('res.branch',string="Dependencia",required=True,)

    #funcion para autocompletar con un cero ala izquierda y validar que el codigo no se repirta y sea unico.
    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit():
                if len(val)<=1:
                    obj.code = '0'+obj.code
            else:
                raise ValidationError(_('Valor Invalido'))
        rec = self.env['budget.subdependence'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único por dependencia'))

class BudgetItem(models.Model):#Modelo para Partida de Gasto (PAR).
    _name = 'budget.item'
    _description = 'Partida de Gasto'

    code = fields.Char(string="Partida",required=True,size=3)
    name = fields.Char(string="Nombre",required=True)
    type_item = fields.Selection([('Regulada','R'),('Centralizada','C'),('Directa','D')],string="Tipo de ejercicio",required=True)
    description = fields.Char(string="Descripción")
    cogconac_id  = fields.Many2one('budget.cog.conac',string="COG CONAC",required=True)
    cogshcp_id = fields.Many2one('budget.item.conversion',string="COG SHCP",required=True)
    expense_account = fields.Many2one('account.account',string="Cuenta de gastos",required=True)
    debtor_account = fields.Many2one('account.account', string="Cuenta pasivo deudora",required=True)

    #funcion para autocompletar con un cero ala izquierda y validar que el codigo no se repirta y sea unico.
    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit():
                if len(val)==1:
                    obj.code = '00'+obj.code
                if len(val)==2:
                    obj.code = '0'+obj.code 
            else:
                raise ValidationError(_('Valor Invalido'))
        rec = self.env['budget.item'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único.'))

class BudgetResource_origin(models.Model):#Modelo para Origen del Recurso(OR).
    _name = 'budget.resource.origin'
    _description = 'Origen del Recurso'

    code = fields.Char(string="Código",required=True,size=2)
    name = fields.Char(string="Nombre",required=True)
    is_income_owne = fields.Boolean(string='Si')
    is_income_owne2 = fields.Boolean(string='No')
    observations = fields.Char(string="Observaciones")

    #funcion para autocompletar con un cero ala izquierda y validar que el codigo no se repirta y sea unico.
    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit():
                if len(val)<=1:
                    obj.code = '0'+obj.code
            else:
                raise ValidationError(_('Valor Invalido'))
        rec = self.env['budget.resource.origin'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único.'))

    #funcion para solo selecionar u solo boleano         
    @api.onchange('is_income_owne','is_income_owne2')
    def _onchange_seletion(self):
        if  self.is_income_owne == True:
            self.is_income_owne2 = False
        elif self.is_income_owne ==False: 
            self.is_income_owne2 == True    

class BudgetInstitutionalActivity(models.Model):# Modelo para Actividad Institucional(AI).
    _name = 'budget.institutional.activity'
    _description = 'Actividad Institucional'

    code = fields.Char(string="Código",required=True,size=5)
    name = fields.Char(string="Nombre",required=True)

    #funcion para autocompletar con un cero ala izquierda y validar que el codigo no se repirta y sea unico.
    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit():
                if len(val)==1:
                    obj.code = '0000'+obj.code
                if len(val)==2:
                    obj.code = '000'+obj.code 
                if len(val)==3:
                    obj.code = '00'+obj.code
                if len(val)==4:
                    obj.code ='0'+obj.code        
            else:
                raise ValidationError(_('Valor Invalido'))
        rec = self.env['budget.institutional.activity'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único.'))


class BudgetProgramConversion(models.Model):#modelo para Conversión de Programa Presupuestario(CONPP).
    _name = 'budget.program.conversion'
    _description = 'Conversión de Programa Presupuestario'

    code = fields.Char(string="Código",required=True,size=4)
    name = fields.Char(string="Nombre",required=True)
    cogshcp_id = fields.Many2one('budget.item.conversion',string="PP SHCP",required=True)
    activity = fields.Selection([('bachillerato','Bachillerato'),('licenciatura','Licenciatura'),('posgrado','Posgrado'),('becas','Becas'),('cultura','Cultura'),('mantenimiento','Mantenimiento'),('obras','Obras')],string="Actividad",required=True)

    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit():
                if len(val)==1:
                    obj.code = '000'+obj.code
                if len(val)==2:
                    obj.code = '00'+obj.code 
                if len(val)==3:
                    obj.code = '0'+obj.code
            else:
                raise ValidationError(_('Valor Invalido'))
        rec = self.env['budget.program.conversion'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único.'))



class BudgetItemConversion(models.Model):#modelo para Conversión con partida (CONPA).
    _name = 'budget.item.conversion'
    _description = 'Conversión con Partida'

    code = fields.Char(string="Código (partida)",required=True,size=5)
    name = fields.Char(string="Nombre",required=True)
    item_number = fields.Many2one('budget.item',string="Partida")
    type_item = fields.Selection([('Regulada','R'),('Centralizada','C'),('Directa','D')],string="Tipo de ejercicio",required=True)
    cogconac_id = fields.Many2one('budget.cog.conac',string="COG CONAC",required=True)


    #funcion para autocompletar con un cero ala izquierda y validar que el codigo no se repirta y sea unico.
    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit():
                if len(val)==1:
                    obj.code = '0000'+obj.code
                if len(val)==2:
                    obj.code = '000'+obj.code 
                if len(val)==3:
                    obj.code = '00'+obj.code
                if len(val)==4:
                    obj.code ='0'+obj.code        
            else:
                raise ValidationError(_('Valor Invalido'))
        rec = self.env['budget.item.conversion'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único por partida.'))


class BudgetExpenseType(models.Model):# modelo para Tipo de gasto (TG).
    _name = 'budget.expense.type'
    _description = 'Tipo de Gasto'

    code = fields.Char(string="Código",required=True,size=2)
    name = fields.Char(string="Nombre",required=True)
    
    #funcion para autocompletar con un cero ala izquierda y validar que el codigo no se repirta y sea unico.
    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit():
                if len(val)<=1:
                    obj.code = '0'+obj.code
            else:
                raise ValidationError(_('Valor Invalido'))
        rec = self.env['budget.expense.type'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único.'))

class BudgetGeographicLocation(models.Model):#modelo para Ubicación Geográfica (UG).
    _name = 'budget.geographic.location'
    _description = 'Ubicación Geográfica'

    code = fields.Char(string="Código",required=True,size=2)
    name = fields.Char(string="Nombre",required=True)
    
    #funcion para autocompletar con un cero ala izquierda y validar que el codigo no se repirta y sea unico.
    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit():
                if len(val)<=1:
                    obj.code = '0'+obj.code
            else:
                raise ValidationError(_('Valor Invalido'))
        rec = self.env['budget.geographic.location'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único.'))

class BudgetKeyPortfolio(models.Model):#modelo Clave cartera(CC).
    _name = 'budget.key.portfolio'
    _description = 'Clave Cartera'

    code = fields.Char(string="Código",required=True,size=4)
    name = fields.Char(string="Nombre",required=True)
    description = fields.Char(string="Descripción")
    entity_id = fields.Many2one('budget.geographic.location',string="Entidad",required=True)
    type_program = fields.Selection([('1','Proyecto de Inversión de Infraestructura social'),('2','Programa de Inversión de Mantenimiento'),('3','Programa de Inversión de Adquisiciones')],string="Tipo de programa o proyecto",required=True)

    #funcion para autocompletar con un cero ala izquierda y validar que el codigo no se repirta y sea unico.
    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit():
                if len(val)==1:
                    obj.code = '000'+obj.code
                if len(val)==2:
                    obj.code = '00'+obj.code
                if len(val)==3:
                    obj.code ='0'+obj.code    
            else:
                raise ValidationError(_('Valor Invalido'))
        rec = self.env['budget.key.portfolio'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único.'))
class BudgetProjectType(models.Model):#modelo para el Tipo de proyecto(TP).
    _name = 'budget.project.type'
    _description = 'Tipo de Proyecto'

    code = fields.Char(string="Código",required=True,size=2)
    name = fields.Char(string="Nombre",required=True)

    #funcion para autocomplementar y que solo sean esnteros y la duplicidad 
    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit()==False:
                raise ValidationError(_('Valor Invalido.'))
            else:
                if val.isdigit():
                    if len(val)==1:
                        obj.code = '0'+obj.code
                else:
                    raise ValidationError(_('Falta completar los caracteres necesarios del código.'))    
        rec = self.env['budget.project.type'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único.'))


class ProjectProjectMod(models.Model):# modelo para Proyectos (NP). haciendo inherit al modelo project.project
    _inherit = 'project.project'


    code = fields.Char(string="Código",required=True, size=6 )#aki falta lo relacionado al account.analityc.accoun
    type_project_id = fields.Many2one('budget.project.type',string="Tipo de proyecto",required=True)
    sub_type = fields.Selection([('spp','(SPP) Sistema de pagos a proveedores de bienes y prestadores de servicio.'),('cbc','(CBC) Cuenta bancaria con chequera.')],string="Subtipo de proyecto",required=True)
    amount_allocated = fields.Monetary(string="Monto asignado",required=True)
    consumed_amount = fields.Monetary(string="Monto ejercido",required=True)
    # date_start1 = fields.Date(string='Fecha de inicio del proyecto',required=True)
    # date1 = fields.Date(string='Fecha final del proyecto',required=True)

    #funcion para autocompletar con un cero ala izquierda y validar que el codigo no se repirta y sea unico.
    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit():
                if len(val)==1:
                    obj.code = '00000'+obj.code
                if len(val)==2:
                    obj.code = '0000'+obj.code
                if len(val)==3:
                    obj.code = '000'+obj.code
                if len(val)==4:
                    obj.code = '00'+obj.code 
                if len(val)==5:
                    obj.code = '0'+obj.code 
            else:
                raise ValidationError(_('Valor Invalido'))
        rec = self.env['project.project'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único.'))

class BudgetStage(models.Model):#modelo para Etapa(E).
    _name = 'budget.stage'
    _description = 'Etapa'

    code = fields.Char(string="Código",required=True,size=2)
    name = fields.Char(string="Nombre",required=True)

    #funcion para autocompletar con un cero ala izquierda y validar que el codigo no se repirta y sea unico.
    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit():
                if len(val)<=1:
                    obj.code = '0'+obj.code
            else:
                raise ValidationError(_('Valor Invalido'))
        rec = self.env['budget.stage'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único.'))

class BudgetAgreementType(models.Model):#modelo para Tipo de convenio(TC).
    _name = 'budget.agreement.type'
    _description = 'Tipo de Convenio'

    code = fields.Char(string="Código",required=True,size=2)
    name = fields.Char(string="Nombre",required=True)

    #funcion para autocompletar con un cero ala izquierda y validar que el codigo no se repirta y sea unico.
    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit():
                if len(val)<=1:
                    obj.code = '0'+obj.code
            else:
                raise ValidationError(_('Valor Invalido'))
        rec = self.env['budget.agreement.type'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único.'))


class AgreementAgreement(models.Model):#modelo para Convenios(NC)
    _name = 'agreement.agreement'
    _description = 'Convenios'

    code = fields.Char(string="Código",required=True,size=6)
    name = fields.Char(string="Nombre",required=True)
    agreement_type_id = fields.Many2one('budget.agreement.type',string="Tipo de convenio",required=True)
    #branch_id = fields.Many2one('res.branch',string="Dependencia",required=True)
    budget_subdependence_id = fields.Many2one('budget.subdependence',string="Subdepencencia",required=True)

    #funcion para autocomplementar y que solo sean esnteros y la duplicidad 
    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit()==False:
                raise ValidationError(_('Valor Invalido.'))
            else:
                if val.isdigit():
                    if len(val)==1:
                        obj.code = '00000'+obj.code
                    if len(val)==2:
                        obj.code = '0000'+obj.code
                    if len(val)==3:
                        obj.code = '000'+obj.code
                    if len(val)==4:
                        obj.code = '00'+obj.code 
                    if len(val)==5:
                        obj.code = '0'+obj.code 
                else:
                    raise ValidationError(_('Falta completar los caracteres necesarios del código.'))    
        rec = self.env['agreement.agreement'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único.'))



class BudgetCogConac(models.Model):#modelo para Catálogo COG CONAC ()
    _name = 'budget.cog.conac'
    _description = 'Catálogo COG CONAC'

    code = fields.Char(string="Código",required=True)
    name = fields.Char(string="Nombre",required=True)

    #funcion para autocompletar con un cero ala izquierda y validar que el codigo no se repirta y sea unico.
    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit():
                if len(val)<=1:
                    obj.code = '0'+obj.code
            else:
                raise ValidationError(_('Valor Invalido'))
        rec = self.env['budget.cog.conac'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único.'))


class InheritCrossoveredBudget(models.Model):# modelo el cual hace un inherit al modelo crossovered.budget
    _inherit = 'crossovered.budget'

    file_import  = fields.Binary(string='Archivo de importación')
    filename = fields.Char('file name') 
    total_budget = fields.Integer(string="Total de presupuesto",readonly=True, compute="compute_amount_tb")
    record_numbers = fields.Integer(string="Número de registros",readonly=True)
    imported_registration_numbers = fields.Integer(string="Número de registros importados",readonly=True)
    budget_of_project_dgpo = fields.Boolean(string="Presupuesto de DGPO")
    move_id = fields.Many2one('account.move',string="Asiento contable",readonly=True)
    invalid_rows = fields.One2many('invalid.row','crossovered_budget_id')
    programatic_code = fields.Text(string="codigo programático")
    correct_import = fields.Boolean(
        string='Importación Correcta?',
        default=False
    )

    @api.depends('crossovered_budget_line.authorized_amount')
    def compute_amount_tb(self):
        for rec in self:
            t = 0
            for x in rec.crossovered_budget_line:
                t += x.authorized_amount
            rec.update({'total_budget': t})

    #funcion para leer archivos txt 
    @api.onchange('filename')
    def onchange_file(self):
        self.invalid_rows = [(5, 0, 0)]
        if self.filename:
            ext = str(self.filename.split('.')[1])
            if ext != 'txt':
                raise ValidationError('El archivo adjunto no es compatible para la importación')
        else:
            self.record_numbers = 0 
            self.imported_registration_numbers = 0                  
    
    def action_budget_confirm(self):
        res = super(InheritCrossoveredBudget, self).action_budget_confirm()
        self.create_account_move_unam()
        return res

    def action_budget_cancel(self):
        res = super(InheritCrossoveredBudget, self).action_budget_cancel()
        self.move_id.unlink()
        return res

    def create_account_move_unam(self):
        vals = {
            'ref':self.name
        }
        move = self.env['account.move'].create(vals)
        for x in self.crossovered_budget_line:
            v1 = {
                'move_id':move.id,
                'account_id':x.item_id.expense_account.id,
                'partner_id':self.company_id.partner_id.id,
                'name':str(x.item_id.expense_account.code)+' Ley de ingresos por ejecutar',
                'debit':x.authorized_amount,
                'account_internal_type':'other',
                'programmatic_code':x.programmatic_account
                }
            v2 = {
                'move_id':move.id,
                'account_id':x.item_id.debtor_account.id,
                'partner_id':self.company_id.partner_id.id,
                'name':str(x.item_id.debtor_account.code)+' Ley de ingresos estimada',
                'credit':x.authorized_amount,
                'account_internal_type':'receivable',
                'programmatic_code':x.programmatic_account
                }
            v3 = {
                'move_id':move.id,
                'account_id':x.item_id.expense_account.id,
                'partner_id':self.company_id.partner_id.id,
                'name':str(x.item_id.expense_account.code)+' Presupuesto de egresos a ejercer',
                'debit':x.amount_allocate,
                'account_internal_type':'other',
                'programmatic_code':x.programmatic_account
                }
            v4 = {
                'move_id':move.id,
                'account_id':x.item_id.debtor_account.id,
                'partner_id':self.company_id.partner_id.id,
                'name':str(x.item_id.debtor_account.code)+' Presupuesto de egresos aprobado',
                'credit':x.amount_allocate,
                'account_internal_type':'receivable',
                'programmatic_code':x.programmatic_account
                }
            self.env['account.move.line'].with_context(check_move_validity=False).create(v1)
            self.env['account.move.line'].with_context(check_move_validity=False).create(v2)
            self.env['account.move.line'].with_context(check_move_validity=False).create(v3)
            self.env['account.move.line'].with_context(check_move_validity=False).create(v4)
        self.move_id = move.id


    #Lee el archivo para revisar si todas las filas del registro son correctas,
    # si no lo son guarda en una tabla la linea que esta mal y su lista de errores,
    # si todas son correctas ejecuta la siguiente funcion
    def read_file(self):
        self.invalid_rows = [(5, 0, 0)]
        if self.file_import:
            data = base64.decodestring(self.file_import)
            fobj = tempfile.NamedTemporaryFile(delete=False)
            fname = fobj.name
            fobj.write(data)
            fobj.close()
            file = open(fname,"r")
            structure = self.env['budget.structure'].search([('code_part_pro','=',True)])
            count_valid = 0
            tot_reg = 0
            message = " ERRORES: "
            valid = True
            data_code = ''
            number_line = 0
            for x in file:
                pc = ''
                data_code = ''
                number_line += 1
                for y in structure:
                    position = x[y.position_from:y.position_to]
                    if y.catalog_id.model:
                        search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                        if not search_model:
                            valid = False
                            message += ' Código invalido en el modelo '+ y.catalog_id.name + '. \n'
                    data_code += '\n'+y.name+', '  
                    pc += position + ' '
                if valid == True:
                    count_valid += 1
                else:
                    self.invalid_rows.create({
                        'code':pc,
                        'description':'Linea '+ str(number_line) +message, 
                        'crossovered_budget_id': self.id,
                    })
                tot_reg += 1
            self.record_numbers = tot_reg
            self.imported_registration_numbers = count_valid
            self.programatic_code = data_code
            if count_valid == tot_reg:
                self.correct_import = True
                try:
                    self.create_budget_post_from_file()
                except:
                    print('ERROR AL EJECUTAR create_budget_post_from_file()')
        else:
            self.record_numbers = 0
            self.imported_registration_numbers = 0
            self.programatic_code = False

    #Si la funcion anterior se termino correctamente se ejecuta la siguiente funcion para generar lss
    # lineas de presupuesto y sus posisiones.
    def create_budget_post_from_file(self):
        if self.file_import and (self.record_numbers == self.imported_registration_numbers):
            data = base64.decodestring(self.file_import)
            fobj = tempfile.NamedTemporaryFile(delete=False)
            fname = fobj.name
            fobj.write(data)
            fobj.close()
            file = open(fname,"r")
            model_budget_item = self.env['ir.model'].search([('model','=','budget.item')])
            structure = self.env['budget.structure'].search([('code_part_pro','=',True)])
            print(model_budget_item.name)
            account_budget_post = False
            budget_item_structure = self.env['budget.structure'].search([('code_part_pro','=',True),('catalog_id','=',model_budget_item.id)])
            print(budget_item_structure.name)
            for x in file:
                pc = ''
                position = x[budget_item_structure.position_from:budget_item_structure.position_to]
                search_budget_item = self.env[str('budget.item')].search([(budget_item_structure.to_search_field.name,'=',str(position))])
                print(">>>>>>>>>> CODIGOS <<<<<<<<<<",x,position,search_budget_item.name,search_budget_item.expense_account.name)
                vals = {
                    'name':x,
                    'account_ids':[(6, 0, [search_budget_item.expense_account.id])]
                }
                print(vals)
                account_budget_post = self.env['account.budget.post'].create(vals)
                # print(account_budget_post)
                subdependence_id = False
                program_id = False
                subprogram_id = False
                item_id = False
                resource_origin_id = False
                institutional_activity_id = False
                conpp_id = False
                conpa_id = False
                expense_type_id = False
                geographic_location_id = False
                key_portfolio_id = False
                year = ''
                verdigit = ''
                autorized = 0
                asigned = 0
                for y in structure:
                    position = x[y.position_from:y.position_to]
                    pc = pc + position + ' '
                    if y.is_year == True:
                        year = position
                    if y.is_check_digit == True:
                        verdigit = position
                    if y.is_authorized_budget == True:
                        autorized = position
                    if y.is_asigned_budget == True:
                        asigned = position
                    if y.catalog_id.model:
                        if y.catalog_id.model == 'budget.subdependence':
                            search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                            if search_model:
                                subdependence_id = search_model.id
                        if y.catalog_id.model == 'budget.program':
                            search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                            if search_model:
                                program_id = search_model.id
                        if y.catalog_id.model == 'budget.subprogram':
                            search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                            if search_model:
                                subprogram_id = search_model.id
                        if y.catalog_id.model == 'budget.item':
                            search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                            if search_model:
                                item_id = search_model.id
                        if y.catalog_id.model == 'budget.resource.origin':
                            search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                            if search_model:
                                resource_origin_id = search_model.id
                        if y.catalog_id.model == 'budget.institutional.activity':
                            search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                            if search_model:
                                institutional_activity_id = search_model.id
                        if y.catalog_id.model == 'budget.program.conversion':
                            search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                            if search_model:
                                conpp_id = search_model.id
                        if y.catalog_id.model == 'budget.item.conversion':
                            search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                            if search_model:
                                conpa_id = search_model.id
                        if y.catalog_id.model == 'budget.expense.type':
                            search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                            if search_model:
                                expense_type_id = search_model.id
                        if y.catalog_id.model == 'budget.geographic.location':
                            search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                            if search_model:
                                geographic_location_id = search_model.id
                        if y.catalog_id.model == 'budget.key.portfolio':
                            search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                            if search_model:
                                key_portfolio_id = search_model.id
                print(asigned,autorized,year)
                vars = {
                    'programmatic_account':pc,
                    'subdependence_id':subdependence_id,
                    'program_id':program_id,
                    'subprogram_id':subprogram_id,
                    'item_id':item_id,
                    'resource_origin_id':resource_origin_id,
                    'institutional_activity_id':institutional_activity_id,
                    'conpp_id':conpp_id,
                    'conpa_id':conpa_id,
                    'expense_type_id':expense_type_id,
                    'geographic_location_id':geographic_location_id,
                    'key_portfolio_id':key_portfolio_id,
                    'date_from':datetime(int(year), 1, 1),
                    'date_to':datetime(int(year), 3, 31),
                    'planned_amount':float(autorized),
                    'authorized_amount':float(autorized),
                    'amount_allocate':float(asigned),
                    'general_budget_id':account_budget_post.id,
                    'crossovered_budget_id': self.id
                }
                print(vars)
                account_budget_line = self.env['crossovered.budget.lines'].create(vars)

class InvalidDataTXT(models.Model):#tabla para crear los registros del txt incorrectos
    _name = 'invalid.row'

    crossovered_budget_id = fields.Many2one('crossovered.budget',ondelete="cascade")
    budget_amount_allocated_id = fields.Many2one('budget.amount.allocated', ondelete='cascade')
    budget_adjustement_id = fields.Many2one('budget.adjustement', ondelete='cascade')
    budget_import_recalendarization_id = fields.Many2one('budget.import.recalendarization', ondelete='cascade')
    code = fields.Text(string='Codido programático')
    description = fields.Char(string="Descripción")


class InheritCrossoveredBudgetLine(models.Model):# modelo en el cual se hace un inherit al modedlo existente crossovered.budget.lines pag del doc 24
    _inherit = 'crossovered.budget.lines'
    #campos replazables que utilice para ocultarlos
    paid_date = fields.Date('Paid Date')
    theoritical_amount = fields.Monetary(
    compute='_compute_theoritical_amount', string='Theoretical Amount',
    help="Amount you are supposed to have earned/spent at this date.")
    percentage = fields.Float(
    compute='_compute_percentage', string='Achievement',
    help="Comparison between practical and theoretical amount. This measure tells you if you are below or over budget.")

    #campos nuevos del diseño de unam
    authorized_amount = fields.Float(string="Autorizado")# en comentario dice si  falta checar aque se refiere este campo
    amount_allocate = fields.Float(string="Asignado",digits=(12,2))
    amount_committed = fields.Float(string="Comprometido",digits=(12,2))
    accrued_amount = fields.Float(string="Devengado",digits=(12,2))
    amount_available = fields.Float(string="Por ejercer",digits=(12,2))
    amount_paid = fields.Float(string="Pagado",digits=(12,2))
    amount_applied = fields.Float(string="Ejercido",digits=(12,2))
    amount_modified = fields.Float(string="Modificado",digits=(12,2))
    amount_available2 = fields.Float(string="Disponible",digits=(12,2))
    programmatic_account = fields.Text(string="Código programático")#El valor debe estar separado por (.) por cada segmento del código programático
    # branch_id = fields.Many2one('branch',string="Dependencia")
    subdependence_id = fields.Many2one('budget.subdependence',string="Subdependencia")
    program_id = fields.Many2one('budget.program',string="Programa")
    subprogram_id = fields.Many2one('budget.subprogram',string="Subprograma")
    item_id = fields.Many2one('budget.item',string="Partida")
    resource_origin_id = fields.Many2one('budget.resource.origin',string="Origen del recurso")
    institutional_activity_id = fields.Many2one('budget.institutional.activity',string="Actividad institucional")
    conpp_id = fields.Many2one('budget.program.conversion',string="Conversión de programa presupuestario")
    conpa_id = fields.Many2one('budget.item.conversion',string="Conversión con partida")
    expense_type_id = fields.Many2one('budget.expense.type',string="Tipo de gasto")
    geographic_location_id = fields.Many2one('budget.geographic.location',string="Ubicación geográfica")
    key_portfolio_id = fields.Many2one('budget.key.portfolio',string="Clave cartera")

class BudgetAmountAllocated(models.Model):# modelo para Control de montos asignados pag 24 doc
    _name = 'budget.amount.allocated'
    _description = "Budget Amount Allocated"
    code = fields.Char(string="Folio",required=True, default=lambda self: _('New'))
    name = fields.Char(string="Folio",required=True, compute="get_code")
    budget_id = fields.Many2one('crossovered.budget',string="Presupuesto",required=True)
    description = fields.Char(string="Observaciones")
    date_import = fields.Date(string="Fecha de importación",required=True)
    file_amount_allocated  = fields.Binary(string="Archivo estacionalidad",required=True)
    user_id = fields.Many2one('res.users',string="Realizado por",required=True)
    state = fields.Selection([('draft', 'Borrador'),('solicitud','Solicitud'),('approve','Aprobado'),('reject','Rechazado'),('cancel','Cancelado')], default="draft")
    reason_for_rejection = fields.Char(string="Motivo del rechazo")
    budget_amount_allocated_line_ids = fields.One2many('budget.amount.allocated.lines', 'allocated_deposit_id')

    currency_id = fields.Many2one('res.currency', string='Currency')
    assigment_amount = fields.Monetary(string="Monto asignado",digits=(12,2),required=True)
    deposit_amount = fields.Monetary(string="Monto depositado",required=True,readonly=True, compute="compute_amount_da")
    pending_amount = fields.Monetary(string="Monto pendiente",digits=(12,2),readonly=True, compute="compute_amount_da")
    deposit_date = fields.Date(string="Fecha depósito")
    deposit_account_bank_id = fields.Many2one('account.journal',string="Cuenta del depósito")
    comments = fields.Text(string="Observaciones")
    move_id = fields.Many2one('account.move',string="Asiento contable")

    filename = fields.Char()
    invalid_rows = fields.One2many('invalid.row','budget_amount_allocated_id')
    record_numbers = fields.Integer(string="Número de registros",readonly=True)
    imported_registration_numbers = fields.Integer(string="Número de registros importados",readonly=True)
    correct_import = fields.Boolean(
        string='Importación Correcta?',
        default=False
    )

    def get_code(self):
        for rec in self:
            rec.name = rec.code

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].get('budget.amount.allocated') or '/'
        vals['code'] = seq
        return super(BudgetAmountAllocated, self).create(vals)

    @api.depends('budget_amount_allocated_line_ids')
    def compute_amount_da(self):
        for rec in self:
            t = 0
            for x in rec.budget_amount_allocated_line_ids:
                t += x.amount
            rec.update({'deposit_amount': t})
            rec.pending_amount = rec.assigment_amount - rec.deposit_amount

    @api.onchange('filename')
    def onchange_file(self):
        self.invalid_rows = [(5, 0, 0)]
        if self.filename:
            ext = str(self.filename.split('.')[1])
            if ext != 'txt':
                raise ValidationError('El archivo adjunto no es compatible para la importación')
        else:
            self.record_numbers = 0 
            self.imported_registration_numbers = 0            

    def function_request(self):
        self.state = 'solicitud'

    def function_approve(self):
        self.create_account_move_unam()
        self.state = 'approve'

    def function_reject(self):
        self.state = 'reject'

    def function_cancel(self):
        self.state = 'cancel'

    def function_draft(self):
        self.state = 'draft'


    def create_account_move_unam(self):
        vals = {
            'ref':'CMA0'+self.code
        }
        move = self.env['account.move'].create(vals)
        for x in self.budget_amount_allocated_line_ids:
            v1 = {
                'move_id':move.id,
                'account_id':x.item_id.expense_account.id,
                'name':str(x.item_id.expense_account.code)+' Ley de ingresos por ejecutar',
                'debit':x.amount,
                'account_internal_type':'other',
                'programmatic_code':x.programmatic_code
                }
            v2 = {
                'move_id':move.id,
                'account_id':x.item_id.debtor_account.id,
                'name':str(x.item_id.debtor_account.code)+' Ley de ingresos estimada',
                'credit':x.amount,
                'account_internal_type':'receivable',
                'programmatic_code':x.programmatic_code
                }
            self.env['account.move.line'].with_context(check_move_validity=False).create(v1)
            self.env['account.move.line'].with_context(check_move_validity=False).create(v2)
        self.move_id = move.id

    def read_file(self):
        self.invalid_rows = [(5, 0, 0)]
        if self.file_amount_allocated:
            data = base64.decodestring(self.file_amount_allocated)
            fobj = tempfile.NamedTemporaryFile(delete=False)
            fname = fobj.name
            fobj.write(data)
            fobj.close()
            file = open(fname,"r")
            structure = self.env['budget.structure'].search([('code_part_pro','=',True)])
            count_valid = 0
            tot_reg = 0
            message = " ERRORES: "
            valid = True
            number_line = 0
            for x in file:
                pc = ''
                number_line += 1
                for y in structure:
                    position = x[y.position_from:y.position_to]
                    if y.catalog_id.model:
                        search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                        if not search_model:
                            valid = False
                            message += ' Código invalido en el modelo '+ y.catalog_id.name + '. \n'
                    pc += position + ' '
                if valid == True:
                    count_valid += 1
                else:
                    self.invalid_rows.create({
                        'code':pc,
                        'description':'Linea '+ str(number_line) +message, 
                        'budget_amount_allocated_id': self.id,
                    })
                tot_reg += 1
            self.record_numbers = tot_reg
            self.imported_registration_numbers = count_valid
            self.create_budget_allocated_lines_from_file()
                    # except:
                    #     print('ERROR AL EJECUTAR create_budget_allocated_lines_from_file()')
        else:
            self.record_numbers = 0
            self.imported_registration_numbers = 0

    def create_budget_allocated_lines_from_file(self):
        if self.file_amount_allocated:
            if self.record_numbers == self.imported_registration_numbers:
                data = base64.decodestring(self.file_amount_allocated)
                fobj = tempfile.NamedTemporaryFile(delete=False)
                fname = fobj.name
                fobj.write(data)
                fobj.close()
                file = open(fname,"r")
                structure = self.env['budget.structure'].search([('code_part_pro','=',True)])
                account_budget_post = False
                for x in file:
                    programmatic_code = ''
                    amount = ''
                    date = datetime.now()
                    subdependence_id = ''
                    program_id = ''
                    subprogram_id = ''
                    item_id = ''
                    resource_origin_id = ''
                    institutional_activity_id = ''
                    conpp_id = ''
                    conpa_id = ''
                    expense_type_id = ''
                    geographic_location_id = ''
                    key_portfolio_id = ''
                    for y in structure:
                        position = x[y.position_from:y.position_to]
                        programmatic_code += str(position + ' ')
                        if y.is_authorized_budget == True:
                            amount = position
                        if y.catalog_id.model:
                            if y.catalog_id.model == 'budget.subdependence':
                                search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                                if search_model:
                                    subdependence_id = search_model.id
                            if y.catalog_id.model == 'budget.program':
                                search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                                if search_model:
                                    program_id = search_model.id
                            if y.catalog_id.model == 'budget.subprogram':
                                search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                                if search_model:
                                    subprogram_id = search_model.id
                            if y.catalog_id.model == 'budget.item':
                                search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                                if search_model:
                                    item_id = search_model.id
                            if y.catalog_id.model == 'budget.resource.origin':
                                search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                                if search_model:
                                    resource_origin_id = search_model.id
                            if y.catalog_id.model == 'budget.institutional.activity':
                                search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                                if search_model:
                                    institutional_activity_id = search_model.id
                            if y.catalog_id.model == 'budget.program.conversion':
                                search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                                if search_model:
                                    conpp_id = search_model.id
                            if y.catalog_id.model == 'budget.item.conversion':
                                search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                                if search_model:
                                    conpa_id = search_model.id
                            if y.catalog_id.model == 'budget.expense.type':
                                search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                                if search_model:
                                    expense_type_id = search_model.id
                            if y.catalog_id.model == 'budget.geographic.location':
                                search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                                if search_model:
                                    geographic_location_id = search_model.id
                            if y.catalog_id.model == 'budget.key.portfolio':
                                search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                                if search_model:
                                    key_portfolio_id = search_model.id
                    vars = {
                        'allocated_deposit_id':self.id,
                        'programmatic_code':programmatic_code,
                        'amount':amount,
                        'date':date,
                        'subdependence_id':subdependence_id,
                        'program_id':program_id,
                        'subprogram_id':subprogram_id,
                        'item_id':item_id,
                        'resource_origin_id':resource_origin_id,
                        'institutional_activity_id':institutional_activity_id,
                        'conpp_id':conpp_id,
                        'conpa_id':conpa_id,
                        'expense_type_id':expense_type_id,
                        'geographic_location_id':geographic_location_id,
                        'key_portfolio_id':key_portfolio_id,
                    }
                    print(vars)
                    budget_amount_allocated_line = self.env['budget.amount.allocated.lines'].create(vars)
                self.correct_import = True




# class DepositControlTable(models.Model):#tabla control de montos 
#     _name = 'deposit.control.table'

#     budget_amount_allocated_id = fields.Many2one('budget.amount.allocated', ondelete="cascade")
#     currency_id = fields.Many2one('res.currency', string='Currency')
#     assigment_amount = fields.Monetary(string="Monto asignado",digits=(12,2),required=True)
#     deposit_amount = fields.Monetary(string="Monto depositado",required=True,readonly=True)
#     pending_amount = fields.Monetary(string="Monto pendiente",digits=(12,2),readonly=True)
#     deposit_date = fields.Date(string="Fecha depósito")
#     deposit_account_bank_id = fields.Many2one('account.journal',string="Cuenta del depósito")
#     comments = fields.Char(string="Observaciones")
#     move_id = fields.Many2one('account.move',string="Asiento contable")

class BudgetAmountAllocatedLines(models.Model): #parte del modelo budget.amount.allocated.lines que esta  Control de montos asignados pag 24 doc
    _name = 'budget.amount.allocated.lines'


    allocated_deposit_id = fields.Many2one('budget.amount.allocated',string="Control de monto asignado",required=True)
    programmatic_code = fields.Char(string="Código programático",required=True)
    amount = fields.Float(string="Monto",required=True)
    date  = fields.Date(string="Fecha",required=True)
    #branch_id = fields.Many2one('res.branch',string="Dependencia")
    subdependence_id = fields.Many2one('budget.subdependence',string="Subdependencia")
    program_id = fields.Many2one('budget.program',string="Programa")
    subprogram_id = fields.Many2one('budget.subprogram',string="Subprograma")
    item_id = fields.Many2one('budget.item',string="Partida")
    resource_origin_id = fields.Many2one('budget.resource.origin',string="Origen del recurso")
    institutional_activity_id = fields.Many2one('budget.institutional.activity',string="Actividad instituciona")
    conpp_id = fields.Many2one('budget.program.conversion',string="Conversión de programa presupuestario")
    conpa_id = fields.Many2one('budget.item.conversion',string="Conversión con partida")
    expense_type_id = fields.Many2one('budget.expense.type',string="Tipo de gasto")
    geographic_location_id = fields.Many2one('budget.geographic.location',string="Ubicación geográfica")
    key_portfolio_id = fields.Many2one('budget.key.portfolio',string="Clave cartera")

class BudgetAdjustement(models.Model):#modelo para las Adecuaciones 6.1
    _name='budget.adjustement'
    code = fields.Char(string="Folio",required=True)
    movement_date = fields.Date(string="Fecha",default=fields.Date.today(),required=True)
    budget_id = fields.Many2one('crossovered.budget',string="Presupuesto",required=True)
    description = fields.Char(string="Observaciones")
    file = fields.Binary(string="Archivo adecuación")
    state = fields.Selection([('draft', 'Borrador'),('approve','Aprovado'),('solicitud','Solicitud'),('reject','Rechazado'),('cancel','Cancelado')], default="draft")
    reason_for_rejection = fields.Char(string="Motivo del rechazo")
    move_id = fields.Many2one('account.move',string="Asiento contable")
    budget_adjustement_line= fields.One2many('budget.adjustement.lines','adjustement_id')
    filename = fields.Char()
    invalid_rows = fields.One2many('invalid.row','budget_adjustement_id')
    record_numbers = fields.Integer(string="Número de registros",readonly=True)
    imported_registration_numbers = fields.Integer(string="Número de registros importados",readonly=True)
    correct_import = fields.Boolean(
        string='Importación Correcta?',
        default=False
    )

    @api.onchange('filename')
    def onchange_file(self):
        self.invalid_rows = [(5, 0, 0)]
        if self.filename:
            ext = str(self.filename.split('.')[1])
            if ext != 'txt':
                raise ValidationError('El archivo adjunto no es compatible para la importación')
        else:
            self.record_numbers = 0 
            self.imported_registration_numbers = 0            

    def function_request(self):
        self.state = 'solicitud'

    def function_approve(self):
        self.create_account_move_unam()
        self.state = 'approve'

    def function_reject(self):
        self.state = 'reject'

    def function_cancel(self):
        self.state = 'cancel'

    def function_draft(self):
        self.state = 'draft'

    def create_account_move_unam(self):
        vals = {
            'ref':'ADE0'+self.code
        }
        move = self.env['account.move'].create(vals)
        for x in self.budget_adjustement_line:
            v1 = {
                'move_id':move.id,
                'account_id':x.item_id.expense_account.id,
                'name':str(x.item_id.expense_account.code)+' Ley de ingresos por ejecutar',
                'debit':x.amount,
                'account_internal_type':'other',
                'programmatic_code':x.programmatic_code
                }
            v2 = {
                'move_id':move.id,
                'account_id':x.item_id.debtor_account.id,
                'name':str(x.item_id.debtor_account.code)+' Ley de ingresos estimada',
                'credit':x.amount,
                'account_internal_type':'receivable',
                'programmatic_code':x.programmatic_code
                }
            self.env['account.move.line'].with_context(check_move_validity=False).create(v1)
            self.env['account.move.line'].with_context(check_move_validity=False).create(v2)
        self.move_id = move.id

    def read_file(self):
        self.invalid_rows = [(5, 0, 0)]
        if self.file:
            data = base64.decodestring(self.file)
            fobj = tempfile.NamedTemporaryFile(delete=False)
            fname = fobj.name
            fobj.write(data)
            fobj.close()
            file = open(fname,"r")
            structure = self.env['budget.structure.adjustement'].search([('code_part_pro','=',True)])
            count_valid = 0
            tot_reg = 0
            message = " ERRORES: "
            valid = True
            number_line = 0
            for x in file:
                pc = ''
                number_line += 1
                for y in structure:
                    position = x[y.position_from:y.position_to]
                    pc += str(position + ' ')
                    if y.to_search_field:
                        search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                        if not search_model:
                            valid = False
                            message += ' Código invalido en el modelo '+ y.catalog_id.name + '. \n'
                    
                if valid == True:
                    count_valid += 1
                else:
                    self.invalid_rows.create({
                        'code':pc,
                        'description':'Linea '+ str(number_line) +message, 
                        'budget_adjustement_id': self.id,
                    })
                tot_reg += 1
            self.record_numbers = tot_reg
            self.imported_registration_numbers = count_valid
            if count_valid == tot_reg:
                self.create_budget_adjustment_lines_from_file('a')
                self.create_budget_adjustment_lines_from_file('r')
        else:
            self.record_numbers = 0
            self.imported_registration_numbers = 0

    def create_budget_adjustment_lines_from_file(self,tipo):
        if self.file and (self.record_numbers == self.imported_registration_numbers):
            data = base64.decodestring(self.file)
            fobj = tempfile.NamedTemporaryFile(delete=False)
            fname = fobj.name
            fobj.write(data)
            fobj.close()
            file = open(fname,"r")
            structure = self.env['budget.structure.adjustement'].search([('code_part_pro','=',True),('is_more_less','!=',tipo)])
            account_budget_post = False
            for x in file:
                programmatic_code = ''
                amount = ''
                subdependence_id = ''
                program_id = ''
                subprogram_id = ''
                item_id = ''
                resource_origin_id = ''
                institutional_activity_id = ''
                conpp_id = ''
                conpa_id = ''
                expense_type_id = ''
                geographic_location_id = ''
                key_portfolio_id = ''
                for y in structure:
                    position = x[y.position_from:y.position_to]
                    print("POSISION :: ",position)
                    programmatic_code += str(position + ' ')
                    if y.is_amount == True:
                            amount = position
                    if y.catalog_id.model:
                        if y.catalog_id.model == 'budget.subdependence':
                            search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                            if search_model:
                                subdependence_id = search_model.id
                        if y.catalog_id.model == 'budget.program':
                            search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                            if search_model:
                                program_id = search_model.id
                        if y.catalog_id.model == 'budget.subprogram':
                            search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                            if search_model:
                                subprogram_id = search_model.id
                        if y.catalog_id.model == 'budget.item':
                            search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                            if search_model:
                                item_id = search_model.id
                        if y.catalog_id.model == 'budget.resource.origin':
                            search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                            if search_model:
                                resource_origin_id = search_model.id
                        if y.catalog_id.model == 'budget.institutional.activity':
                            search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                            if search_model:
                                institutional_activity_id = search_model.id
                        if y.catalog_id.model == 'budget.program.conversion':
                            search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                            if search_model:
                                conpp_id = search_model.id
                        if y.catalog_id.model == 'budget.item.conversion':
                            search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                            if search_model:
                                conpa_id = search_model.id
                        if y.catalog_id.model == 'budget.expense.type':
                            search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                            if search_model:
                                expense_type_id = search_model.id
                        if y.catalog_id.model == 'budget.geographic.location':
                            search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                            if search_model:
                                geographic_location_id = search_model.id
                        if y.catalog_id.model == 'budget.key.portfolio':
                            search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                            if search_model:
                                key_portfolio_id = search_model.id

                t = ''
                if tipo == 'a':
                    t = 'a'
                else:
                    t = 'd'
                vars = {
                    'adjustement_id':self.id,
                    'programmatic_code':programmatic_code,
                    'amount':amount,
                    'subdependence_id':subdependence_id,
                    'program_id':program_id,
                    'subprogram_id':subprogram_id,
                    'item_id':item_id,
                    'resource_origin_id':resource_origin_id,
                    'institutional_activity_id':institutional_activity_id,
                    'conpp_id':conpp_id,
                    'conpa_id':conpa_id,
                    'expense_type_id':expense_type_id,
                    'geographic_location_id':geographic_location_id,
                    'key_portfolio_id':key_portfolio_id,
                    'type':t
                }
                print(vars)
                budget_adjustement_line = self.env['budget.adjustement.lines'].create(vars)
            # self.correct_import = True
    
class BudgetAdjustementLines(models.Model):#modelo el cual se muestra en una pestaña con el nombre líneas de adecuación relacionada al budegte adjustement
    _name ='budget.adjustement.lines'

    adjustement_id = fields.Many2one('budget.adjustement',string="Adecuación",required=True)
    programmatic_code = fields.Text(string="Código programático",required=True)
    type = fields.Selection([('a','Aumento'),('d','Disminución')],string="Tipo",required=True, default='a')
    amount = fields.Float(string="Importe",required=True)
    #branch_id = fields.Many2one('res.branch',string="Dependencia",required=True)
    subdependence_id = fields.Many2one('budget.subdependence',string="Subdepencencia",required=True)
    program_id = fields.Many2one('budget.program',string="Programa",required=True)
    subprogram_id = fields.Many2one('budget.subprogram',string="Subprograma",required=True)
    item_id = fields.Many2one('budget.item',string="Partida",required=True)
    resource_origin_id = fields.Many2one('budget.resource.origin',string="Origen del recurso",required=True)
    institutional_activity_id = fields.Many2one('budget.institutional.activity',string="Actividad institucional",required=True)
    conpp_id = fields.Many2one('budget.program.conversion',string="Conversión de programa presupuestario",required=True)
    conpa_id = fields.Many2one('budget.item.conversion',string="Conversión con partida",required=True)
    expense_type_id = fields.Many2one('budget.expense.type',string="Tipo de gasto", required=True)
    geographic_location_id = fields.Many2one('budget.geographic.location',string="Ubicación Geográfica",required=True)
    key_portfolio_id = fields.Many2one('budget.key.portfolio',string="Clave cartera",required=True)

class BudgetImportRecalendarization(models.Model):#modelo para Recalendarizaciones pag 33
    _name = 'budget.import.recalendarization'

    code = fields.Char(string="Folio",required=True)
    budget_rescheduling_lines = fields.One2many('budget.rescheduling','import_recalendarization_id',string="Recalendarizaciones")
    budget_id = fields.Many2one('crossovered.budget',string="Presupuesto",required=True)
    file = fields.Binary(string="Archivo recalendarización",required=True)
    file2 = fields.Binary(string="Archivo recalendarización",required=True)
    description = fields.Char(string="Observaciones")
    record_number = fields.Integer(string="Numeros de registros",default=0,readonly=True)
    records_number_imported = fields.Integer(string="Número de registros importados",default=0,readonly=True)
    state = fields.Selection([('draft','Borrador'),('import','Importado'),('reject','Rechazado'),('cancel','Cancelado')],default="draft")
    reason_for_rejection = fields.Char(string="Motivo del rechazo")
    filename = fields.Char()
    filename2 = fields.Char()
    invalid_rows = fields.One2many('invalid.row','budget_import_recalendarization_id')
    correct_import = fields.Boolean(
        string='Importación Correcta?',
        default=False
    )

    @api.onchange('filename')
    def onchange_file(self):
        self.invalid_rows = [(5, 0, 0)]
        if self.filename:
            ext = str(self.filename.split('.')[1])
            if ext != 'txt':
                raise ValidationError('El archivo adjunto no es compatible para la importación')
        else:
            self.record_number = 0 
            self.records_number_imported = 0            

    def function_import(self):
        self.state = 'import'

    def function_reject(self):
        self.state = 'reject'

    def function_cancel(self):
        self.state = 'cancel'

    def function_draft(self):
        self.state = 'draft'


    def read_file(self):
        self.invalid_rows = [(5, 0, 0)]
        if self.file:
            data = base64.decodestring(self.file)
            fobj = tempfile.NamedTemporaryFile(delete=False)
            fname = fobj.name
            fobj.write(data)
            fobj.close()
            file = open(fname,"r")
            structure = self.env['budget.structure.recalendarization'].search([('code_part_pro','=',True)])
            count_valid = 0
            tot_reg = 0
            message = " ERRORES: "
            valid = True
            number_line = 0
            for x in file:
                pc = ''
                number_line += 1
                for y in structure:
                    position = x[y.position_from:y.position_to]
                    if y.catalog_id.model:
                        search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                        if not search_model:
                            valid = False
                            message += ' Código invalido en el modelo '+ y.catalog_id.name + '. \n'
                    pc += position + ' '
                if valid == True:
                    count_valid += 1
                else:
                    self.invalid_rows.create({
                        'code':pc,
                        'description':'Linea '+ str(number_line) +message, 
                        'budget_import_recalendarization_id': self.id,
                    })
                tot_reg += 1
            self.record_number = tot_reg
            self.records_number_imported = count_valid
            if self.record_number == self.records_number_imported:
                self.create_budget_rescheduling_from_file()
        else:
            self.record_number = 0
            self.records_number_imported = 0

    def create_budget_rescheduling_from_file(self):
        if self.file and (self.record_number == self.records_number_imported):
            data = base64.decodestring(self.file)
            fobj = tempfile.NamedTemporaryFile(delete=False)
            fname = fobj.name
            fobj.write(data)
            fobj.close()
            file = open(fname,"r")
            structure = self.env['budget.structure.recalendarization'].search([('code_part_pro','=',True)])
            account_budget_post = False
            for x in file:
                programmatic_code = ''
                subdependence_id = ''
                program_id = ''
                subprogram_id = ''
                item_id = ''
                resource_origin_id = ''
                institutional_activity_id = ''
                conpp_id = ''
                conpa_id = ''
                expense_type_id = ''
                geographic_location_id = ''
                key_portfolio_id = ''
                folio = '/'
                fecha = ''
                for y in structure:
                    position = x[y.position_from:y.position_to]
                    programmatic_code += str(position + ' ')
                    if y.is_amount == True:
                        amount = position
                    if y.is_number_doc == True:
                        folio = position
                    if y.is_date_doc == True:
                        fecha = date(int('20'+position[4:6]),int(position[2:4]),int(position[0:2]))
                    if y.catalog_id.model:
                        if y.catalog_id.model == 'budget.subdependence':
                            search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                            if search_model:
                                subdependence_id = search_model.id
                        if y.catalog_id.model == 'budget.program':
                            search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                            if search_model:
                                program_id = search_model.id
                        if y.catalog_id.model == 'budget.subprogram':
                            search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                            if search_model:
                                subprogram_id = search_model.id
                        if y.catalog_id.model == 'budget.item':
                            search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                            if search_model:
                                item_id = search_model.id
                        if y.catalog_id.model == 'budget.resource.origin':
                            search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                            if search_model:
                                resource_origin_id = search_model.id
                        if y.catalog_id.model == 'budget.institutional.activity':
                            search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                            if search_model:
                                institutional_activity_id = search_model.id
                        if y.catalog_id.model == 'budget.program.conversion':
                            search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                            if search_model:
                                conpp_id = search_model.id
                        if y.catalog_id.model == 'budget.item.conversion':
                            search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                            if search_model:
                                conpa_id = search_model.id
                        if y.catalog_id.model == 'budget.expense.type':
                            search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                            if search_model:
                                expense_type_id = search_model.id
                        if y.catalog_id.model == 'budget.geographic.location':
                            search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                            if search_model:
                                geographic_location_id = search_model.id
                        if y.catalog_id.model == 'budget.key.portfolio':
                            search_model = self.env[str(y.catalog_id.model)].search([(y.to_search_field.name,'=',str(position))])
                            if search_model:
                                key_portfolio_id = search_model.id
                vars = {
                    'programmatic_code':programmatic_code,
                    'subdependence_id':subdependence_id,
                    'program_id':program_id,
                    'subprogram_id':subprogram_id,
                    'item_id':item_id,
                    'resource_origin_id':resource_origin_id,
                    'institutional_activity_id':institutional_activity_id,
                    'conpp_id':conpp_id,
                    'conpa_id':conpa_id,
                    'expense_type_id':expense_type_id,
                    'geographic_location_id':geographic_location_id,
                    'key_portfolio_id':key_portfolio_id,
                    'date':fecha,
                    'to_period':'t1',
                    'import_recalendarization_id':self.id,
                    'budget_id':self.budget_id.id,
                    'code': folio
                }
                print(vars)
                budget_rescheduling_line = self.env['budget.rescheduling'].create(vars)
            #self.correct_import = True

class BudgetRescheduling(models.Model):# modelo para Control de recalendarizaciones. pag35
    _name = 'budget.rescheduling'

    code = fields.Char(string="Folio",required=True, default="/")
    amount = fields.Float(string='Monto')
    budget_id = fields.Many2one('crossovered.budget',string="Presupuesto",readonly=True)
    programmatic_code = fields.Char(string="Código programático",required=True)
    date = fields.Date(string="Fecha",default=fields.Date.today(),required=True)
    to_period = fields.Selection([('t1','Trimestre 1'),('t2','Trimestre 2'),('t3','Trimestre 3'),('t4','Trimestre 4')],string="Enviar a",required=True)
    state = fields.Selection([('draft','Borrador'),('import','Importado'),('reject','Rechazado'),('cancel','Cancelado')],default="draft")
    reason_for_rejection = fields.Char(string="Motivo del rechazo")
    import_recalendarization_id = fields.Many2one('budget.import.recalendarization',string="Recalendarización",required=True)
    #branch_id =fields.Many2one('res.branch',string="Dependencia",required=True)
    subdependence_id = fields.Many2one('budget.subdependence',string="Subdependencia",required=True)
    program_id = fields.Many2one('budget.program',string="Programa",required=True)
    subprogram_id = fields.Many2one('budget.subprogram',string="Subprograma",required=True)
    item_id = fields.Many2one('budget.item',string="Partida",required=True)
    resource_origin_id = fields.Many2one('budget.resource.origin',string="Origen del recurso",required=True)
    institutional_activity_id = fields.Many2one('budget.institutional.activity',string="Actividad institucional",required=True)
    conpp_id = fields.Many2one('budget.program.conversion',string="Conversión de programa presupuestario",required=True)
    conpa_id = fields.Many2one('budget.item.conversion',string="Conversión con partida",required=True)
    expense_type_id = fields.Many2one('budget.expense.type',string="Tipo de gasto",required=True)
    geographic_location_id = fields.Many2one('budget.geographic.location',string="Ubicación geográfica",required=True)
    key_portfolio_id = fields.Many2one('budget.key.portfolio',string="Clave cartera",required=True)
    move_id = fields.Many2one('account.move',string="Asiento contable")

    def create_account_move_unam(self):
        vals = {
            'ref':'BRE0'+self.code
        }
        move = self.env['account.move'].create(vals)
        for x in self:
            v1 = {
                'move_id':move.id,
                'account_id':x.item_id.expense_account.id,
                'name':str(x.item_id.expense_account.code)+' Ley de ingresos por ejecutar',
                'debit':0.0,
                'account_internal_type':'other',
                'programmatic_code':x.programmatic_code
                }
            v2 = {
                'move_id':move.id,
                'account_id':x.item_id.debtor_account.id,
                'name':str(x.item_id.debtor_account.code)+' Ley de ingresos estimada',
                'credit':0.0,
                'account_internal_type':'receivable',
                'programmatic_code':x.programmatic_code
                }
            self.env['account.move.line'].with_context(check_move_validity=False).create(v1)
            self.env['account.move.line'].with_context(check_move_validity=False).create(v2)
        self.move_id = move.id

class InheritAccountMoveLine(models.Model):#campos adicionales a este modelo Validación del presupuesto, solicitudes de pago.
    _inherit = 'account.move.line'

    programmatic_code = fields.Char(string="Código programático",required=False)
    #branch_id = fields.Many2one('res.branch',string="Dependencia")
    subdependence_id = fields.Many2one('budget.subdependence',string="Subdepencencia")
    program_id = fields.Many2one('budget.program',string="Programa")
    subprogram_id = fields.Many2one('budget.subprogram',string="SubPrograma")
    item_id = fields.Many2one('budget.item',string="Partida")
    check_digit_id = fields.Char(string="Dígito verificador")
    resource_origin_id = fields.Many2one('budget.resource.origin',string="Origen del recurso")
    institutional_activity_id = fields.Many2one('budget.institutional.activity',string="Actividad institucional")
    conpp_id = fields.Many2one('budget.program.conversion',string="Conversión de programa presupuesto")
    conpa_id = fields.Many2one('budget.program.conversion',string="Conversión de partida")
    expense_type_id = fields.Many2one('budget.expense.type',string="Tipo de gasto")
    geographic_location_id = fields.Many2one('budget.geographic.location',string="Ubicación geográfica")
    key_portfolio_id = fields.Many2one('budget.key.portfolio',string="Clave cartera")
    type_project_id = fields.Many2one('budget.project.type',string="Tipo de proyecto")
    stage = fields.Many2one('budget.stage',string="Etapa")
    agreement_type_id = fields.Many2one('budget.agreement.type',string="Tipo de convenio")
    agreement_number = fields.Many2one('agreement.agreement',string="Número de convenio")
    project_number_id = fields.Many2one('project.project',string="Número de proyecto")

class InheritAccountMove(models.Model):
    _inherit  = 'account.move'
    
    sub_state = fields.Selection([('so','Solicitud'),('ap','Aprovado'),('app','Aprovado para pago'),('ma','Medio de pago asignado'),('pa','Pagado'),('re','Rechazado'),('ca','Cancelado'),('pna','Pago no aplicado'),('mpc','Medio de pago cancelado'),('rpp','Rechazado por pago')],string="Sub-Estado",required=True,default='so')









