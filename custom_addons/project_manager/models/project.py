from odoo import models, fields,api

class Project(models.Model):
    _name = 'project'
    _description = 'Project'

    name = fields.Char()
    start_date = fields.Date()
    end_date = fields.Date()
    description = fields.Text()
    manager_id = fields.Many2one('hr.employee', string='Project Manager', required=True)
    owner_id = fields.Many2one('hr.employee', string='Project Owner', required=True)

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


