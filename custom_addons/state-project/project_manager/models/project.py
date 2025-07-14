from odoo import models, fields,api
from odoo.exceptions import UserError
class Project(models.Model):
    _name = 'project'
    _description = 'Project'

    name = fields.Char()
    start_date = fields.Date()
    end_date = fields.Date()
    description = fields.Text()
    manager_id = fields.Many2one('hr.employee', string='Project Manager', required=True)
    owner_id = fields.Many2one('hr.employee', string='Project Owner', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('manager_approval', 'Waiting Manager Approval'),
        ('owner_approval', 'Waiting Owner Approval'),
        ('open', 'Open'),
        ('closed', 'Closed')
    ], string='Status', default='draft', tracking=True)

    @api.model
    def create(self, vals):
        for rec in self:
            if not self.env.user.has_group('project_manager.project_manager_group'):
                raise UserError("Only Project Managers can create.")
        return super().create(vals)

    def action_submit_to_manager(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError("Only draft projects can be submitted.")
            rec.state = 'manager_approval'

    def action_approve_by_manager(self):
        for rec in self:
            if not self.env.user.has_group('project_manager.project_manager_group'):
                raise UserError("Only Project Managers can approve.")
            if rec.state != 'manager_approval':
                raise UserError("Project not waiting for manager approval.")
            rec.state = 'owner_approval'

    def action_approve_by_owner(self):
        for rec in self:
            if rec.owner_id.user_id != self.env.user:
                raise UserError("Only the assigned Project Owner can approve.")
            if rec.state != 'owner_approval':
                raise UserError("Project not waiting for owner approval.")
            rec.state = 'open'
    #
    def action_close_project(self):
        for rec in self:
            if not self.env.user.has_group('project_manager.project_manager_group'):
                raise UserError("Only Project Managers can approve.")
            if rec.state != 'open':
                raise UserError("Only open projects can be closed.")
            rec.state = 'closed'

    # manager_id = fields.Many2one('hr', string='Project Manager', required=True)
    # owner_id = fields.Many2one('hr', string='Project Owner', required=True)

    # @api.model
    # def _search_projects_for_user(self, operator, value):
    #     employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
    #     if not employee:
    #         return [('id', '=', 0)]
    #
    #     domain = ['|',
    #               ('manager_id', '=', employee.id),
    #               ('owner_id', '=', employee.id)]
    #     return domain
    # @api.model
    # def search(self, args, offset=0, limit=None, order=None, count=False):
    #     if self.env.user.has_group('project_manager.group_project_owner') or self.env.user.has_group('project_manager.group_project_manager'):
    #         employee = self.env['hr'].search([('user_id', '=', self.env.uid)], limit=1)
    #         if employee:
    #             args += ['|', ('owner_id', '=', employee.id), ('manager_id', '=', employee.id)]
    #     return super(Project, self).search(args, offset=offset, limit=limit, order=order, count=count)


