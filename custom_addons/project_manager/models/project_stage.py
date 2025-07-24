from odoo import models, fields

class ProjectStage(models.Model):
    _name = 'project.stage'
    _description = 'Project Stage'
    # _order = 'sequence, id'

    name = fields.Char(string="اسم المرحلة", required=True)
    weight = fields.Float(string="وزن المرحلة")
    hours = fields.Float(string="عدد الساعات")
    manager_id = fields.Many2one('hr.employee', string='stage Manager', required=True)
    description = fields.Text(string="الوصف")
    attachment = fields.Text(string="المرفقات")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting_approval', 'Waiting approve by stage manager'),
        ('approved', 'Approved')
    ], string="الحالة", default='draft')


    show_button_manager_stage = fields.Boolean(
        string="Show Manager Button",
        compute="_compute_show_button_manager_stage",
        store=False
    )



    def _compute_show_button_manager_stage(self):
        current_user = self.env.user
        for record in self:
            is_current_user_manager = (
                    record.manager_id
                    and record.manager_id.user_id == current_user
            )
            record.show_button_manager_stage = is_current_user_manager


    def action_submit_to_stage_manager(self):
        self.write({'state': 'waiting_approval'})

    def action_approve(self):
        self.write({'state': 'approved'})







    # project_id = fields.Many2one('project', string="المشروع", required=True, ondelete='cascade')