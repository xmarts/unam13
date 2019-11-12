# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class reorderchecks(models.Model):
	_name = 'checks.reorder.point'

	name=fields.Text(string='Nombre', required=True)
	bank_id=fields.Many2one('res.bank',string='Banco',required=True, readonly=True, related="bank_account_id.bank_id")
	bank_account_id=fields.Many2one('res.partner.bank',string='Cuenta Bancaria', required=True)
	minimum_of_chek=fields.Integer(string='Mínimo de cheques', required=True)
	reorder_point=fields.Integer(string='Punto de reorden', required=True)

#class actionR(models.Model):
#	_inherit = 'ir.action.report'
#
#	bank_id=fields.Many2one('res.bank',string='Banco')
class rcancellation(models.Model):
	_name = 'reason.for.cancellation'

	code=fields.Text(string='Código', required=True)
	name=fields.Text(string='Nombre', required=True)

class check(models.Model):
	_name = 'checks.checkbook'

	name = fields.Char(string="N° Solicitud")
	#code=fields.Char(string='Número de solicitud', required=True)
	trade_number=fields.Text(string='Número de Oficio', required=True)
	checkbook_number=fields.Text(string='Número de chequera')
	date=fields.Date(string='Fecha', required=True)
	bank_id=fields.Many2one('res.bank',string='Banco', required=True)
	journal_id=fields.Many2one('account.journal',string='Cuenta bancaria', required=True)
	qty_checks=fields.Integer(string='Cantidad de cheques', required=True)
	user_id=fields.Many2one('res.users',string='Solicitante', required=True)
	request_file=fields.Binary(string='Archivo de solicitud', required=True)
	comments=fields.Text(string='Observaciones')
	initial_check_number=fields.Integer(string='Folio inicial')
	final_check_number=fields.Integer(string='Folio Final')
	confirmation_document=fields.Text(string='Oficio de confirmación')
	checks_test_print=fields.Boolean(string='Se envían formatos para prueba de impresión', required=True)
	checks_received=fields.Integer(string='Cheques recibidos')
	checks_per_box=fields.Integer(string='Cheques por caja')
	number_check=fields.Integer(string='Número de folios')
	bankcheck_testprint_id=fields.Many2one('checks.checkbook.print.test', string='Folios de muestra')
	reason_for_rejection=fields.Text(string='Motivo del rechazo')
	state =fields.Selection(
		[('1','Borrador'),
		('2','Solicitud'),
		('3','Aprobada'),
		('4','Confirmada'),
		('5','Enviada'),
		('6','Rechazada')], default="1", string='Estado', required=True)

	
	rel_chekes = fields.One2many('checks.bank.check', 'checkbook_id','state')

      #Cambios de estado 
	def request(self):
		self.state="2"

		#vals = {
		#'check_bank_id':self.id,
		#'state':'2'
		#}
		#self.env['checks.bank.check.history'].create(vals)

	def approve(self):
		self.state="3"
	def send(self):
		self.state="5"
	def confirm(self):
		self.state="4"

		#if self.checks_test_print==True:
			#vals = {
			#'bankcheck_number':'123456',
			#'g_state':'3'
			#}
			#check = self.env['checks.bank.check'].create(vals)

	def to_refuse(self):
		self.state="6"
	def Generate_trade(self):
		vals = {
		'checkbook_id':self.id,
		'bankcheck_number':self.id,
		'state':'1',
		}
		self.env['checks.bank.check'].create(vals)
		print(state)

	def get_code(self):
		for x in self:
			x.name = x.code

	#def name_get(self):
	#	result = []
	#	for record in self:
	#		record_name = str(record.checkbook_number)
	#		result.append((record.id, record_name))
	#	return result
	#@api.onchange('checks_test_print')
	#def check_change(self):
		
		#if self.checks_test_print==True:
			#self.state='6'
			#print(self.state)
			
			#print('Deadpool Malo')
		#else:
			#self.state='1'
			#print(self.state)


class printcheck(models.Model):
	_name="checks.checkbook.print.test"

	name=fields.Char(string="No° de registro")
	checkbook_id=fields.Many2one('checks.checkbook',string='Chequera', required=True)
	bankcheck_number=fields.Integer(string='Folio', required=True)
	comments=fields.Text(string='Observaciones', required=True)

class checkbank(models.Model):
	_name='checks.bank.check'

	name=fields.Char(string="Registro")
	checkbook_id=fields.Many2one('checks.checkbook',string='Chequera')
	acheck_id=fields.Many2one('checks.request.check', string='chequera')
	bankcheck_number=fields.Integer(string='Número de cheque')
	state=fields.Selection([
		('1', 'Alta de chequeras'),
		('2', 'Asignado para envío'),
		('3', 'Disponible para impresión'),
		('4', 'Impreso'),
		('5', 'En tránsito'),
		('6', 'Protegido'),
		('7', 'Retenido'),
		('8', 'Retirado de circulación'),
		('9', 'Pagado'),
		('10', 'Cancelado'),
		('11', 'Cancelado en custodia de finanzas'),
		('12', 'En archivo'),
		('13', 'Reexpedido'),
		('14', 'Destruido')], default="1", string='Último estado', required=True)
	#branch_id=fields.Many2one('branch',string='Dependencia',required=True)
	reason_for_cancellation_id=fields.Many2one('reason.for.cancellation',string='Motivo de cancelación')
	g_state=fields.Selection(
		[('0','Espera'),
		('1','Disponible'),
		('2','Asignado'),
		('3','Cancelado'),
		('4','Pagado')],default='0', string='Estado general', required=True)
	history_c=fields.One2many('checks.bank.check.history','check_bank_id')

class checkbankhistory(models.Model):
	_name='checks.bank.check.history'

	check_bank_id=fields.Many2one('checks.bank.check', string='Cheque', required=True)
	movmente_date=fields.Date(string='Fecha de tansacción')
	state=fields.Selection([
		('1', 'Alta de chequeras'),
		('2', 'Asignado para envío'),
		('3', 'Disponible para impresión'),
		('4', 'Impreso'),
		('5', 'En tránsito'),
		('6', 'Protegido'),
		('7', 'Retenido'),
		('8', 'Retirado de circulación'),
		('9', 'Pagado'),
		('10', 'Cancelado'),
		('11', 'Cancelado en custodia de finanzas'),
		('12', 'En archivo'),
		('13', 'Reexpedido'),
		('14', 'Destruido')], string='Estado del cheque', required=True)
	reason_for_cancellation_id = fields.Many2one('reason.for.cancellation', string='Motivo de cancelación')
	bank_check_archive_id=fields.Many2one('checks.bank.check.archive', string='Archivo de cheques')

	

class requestcheck(models.Model):
	_name='checks.request.check'

	name=fields.Char(string="Numero de registro")
	document_no=fields.Char(string='Número de solicitud', required=True)
	state=fields.Selection(
		[('1','Borrador'),
		('2','Solicitud'),
		('3','Aprobada'),
		('4','Confirmada'),
		('5','Rechazada')], default="1", string='Estado')
	date=fields.Date(string='Fecha de solicitud', required=True)
	checks_qty=fields.Integer(string='Cantidad de cheques', required=True)
	user_id=fields.Many2one('res.users', string='Solicitante', required=True)
	#branch_id=fields.Many2one('branch',string='Dependencia', required=True)
	reason=fields.Char(string='Motivo de la solicitud', required=True)
	is_test_print=fields.Boolean(string='¿Son para pruebas de impresión?')
	checks_autorized= fields.Integer(string='Cantidad de cheques autorizados')
	checkbook_id=fields.Many2one('checks.checkbook', string='Chequera')
	start_document=fields.Integer(string='Folio inicial')
	end_document=fields.Integer(string='Folio final')

	assign_check=fields.One2many('checks.bank.check','acheck_id', 'state')

	def request(self):
		self.state="2"

		#vals = {
		#'check_bank_id':self.id,
		#'state':'2'
		#}
		#self.env['checks.bank.check.history'].create(vals)

	def approve(self):
		self.state="3"
	def confirm(self):
		self.state="4"
	def to_refuse(self):
		self.state="5"

class checkrequestline(models.Model):
	_name='checks.request.check.line'


	request_check_id=fields.Many2one(string='Solicitud de cheque en banco', required=True)
	check_id=fields.Many2one(string='Cheque', required=True)
	state=fields.Selection([
		('1', 'Alta de chequeras'),
		('2', 'Asignado para envío'),
		('3', 'Disponible para impresión'),
		('4', 'Impreso'),
		('5', 'En tránsito'),
		('6', 'Protegido'),
		('7', 'Retenido'),
		('8', 'Retirado de circulación'),
		('9', 'Pagado'),
		('10', 'Cancelado'),
		('11', 'Cancelado en custodia de finanzas'),
		('12', 'En archivo'),
		('13', 'Reexpedido'),
		('14', 'Destruido')], string='Estado de cheque', required=True)
	reason_for_cancellation_id=fields.Many2one(string='Motivo de cancelación')
	bank_check_archive_id=fields.Many2one(string='Archivo de cheques')
class bankcheckarchive(models.Model):
	_name='checks.bank.check.archive'

	code = fields.Text(string='Número de Solicitud', required=True)
	date = fields.Date(string='Fecha', required=True)
	package_identifier=fields.Text(string='Identificador del paquete en archivo', required=True)
	approval_date=fields.Date(string='Fecha de Aprobación', required=True)
	user_id=fields.Many2one('res.users',string='Responsable del envio', required=True)
	department_id=fields.Many2one('hr.departments', string='Puesto de trabajo', required=True)
	comments=fields.Text(string='Observaciones')
	status_bar=fields.Selection(
		[('1','Borrador'),
		('2','Solicitud'),
		('3','Aprobado'),
		('4','Rechazado'),
		('5','Destruido')], string='Estado', required=True)
	reason_for_rejection=fields.Text(string='Motivo del rechazo',required=True)
	document_for_destruction=fields.Binary(string='Acta para destrucción de cheques')