from fabric.contrib.console import confirm
from fabric.operations import prompt, sudo
from fabric.api import *
from fabric.state import env

import files, web, portail, mail, sql, python
import config, gen_mdp

#env.use_ssh_config = True
env.roledefs = {
  'portail': ['portail.mde.utc'],
  'web': ['web.mde.utc'],
  'files': ['files.mde.utc'],
  'mail': ['mail.mde.utc'],
  'sql': ['sql.mde.utc'],
  'python': ['python.mde.utc'],
}

@task(default=True)
@runs_once
def main():
  print("Run 'fab list' to see all commands")

@task
@runs_once
def precreate_asso(login_asso, login_president):
  execute(sql.add_to_portal,login_asso)
  execute(mail.howto_signup,login_president)

@task
@runs_once
def create_asso(login_asso):
  login_president = execute(sql.get_asso_president,login_asso)['sql.mde.utc']
  if not confirm("Are you sure the asso does not exist already ?", False):
    abort("")
  mdp1 = gen_mdp.gen_mdp(8)
  mdp2 = gen_mdp.gen_mdp(8)
  execute(files.add_user,login_asso, mdp1)
  execute(mail.add_mail,login_asso)
  execute(mail.add_assotous,login_asso)
  execute(web.add_web,login_asso)
  execute(portail.add_portail,login_asso)
  execute(sql.add_sql,login_asso, mdp2)
  execute(python.add_user,login_asso)
  execute(mail.send_passwords,login_asso, login_president, mdp1, mdp2)
  
@task
@runs_once
def create_service(login_asso, login_president):
  if not confirm("Are you sure the service or asso does not exist already ?", False):
    abort("")
  mdp1 = gen_mdp.gen_mdp(8)
  mdp2 = gen_mdp.gen_mdp(8)
  execute(files.add_user,login_asso, mdp1)
  execute(web.add_web,login_asso)
  execute(portail.add_portail,login_asso)
  execute(sql.add_sql,login_asso, mdp2)
  execute(python.add_user,login_asso)
  execute(mail.send_passwords,login_asso, login_president, mdp1, mdp2)
  
@task
@runs_once
def change_password_asso(login_asso):
  login_president = execute(sql.get_asso_president,login_asso)['sql.mde.utc']
  mdp = gen_mdp.gen_mdp(8)
  execute(files.change_passwd,login_asso, mdp)
  execute(mail.send_new_password_asso,login_asso, login_president, mdp)

@task
@runs_once
def change_password_mysql(login_asso):
  login_president = execute(sql.get_asso_president,login_asso)['sql.mde.utc']
  mdp = gen_mdp.gen_mdp(8)
  execute(sql.change_passwd,login_asso, mdp)
  execute(mail.send_new_password_sql,login_asso, login_president, mdp)
  
@task
@runs_once
def change_password_service(login_service,login_president):
  mdp = gen_mdp.gen_mdp(8)
  execute(files.change_passwd,login_service, mdp)
  execute(mail.send_new_password_asso,login_service, login_president, mdp)

@task
@runs_once
def change_password_mysql_service(login_service,login_president):
  mdp = gen_mdp.gen_mdp(8)
  execute(sql.change_passwd,login_service, mdp)
  execute(mail.send_new_password_sql,login_service, login_president, mdp)

@task
@runs_once
def reload_generate_vhost():
  execute(portail.generate_vhost_portail)
  execute(web.generate_vhost_web)

@task
@runs_once
def change_for_python(login_asso):
  execute(portail.change_for_python,login_asso)
  execute(web.change_for_python,login_asso)

@task
@runs_once
def change_for_php(login_asso):
  execute(portail.change_for_php,login_asso)
  execute(web.change_for_php,login_asso)

@task
@runs_once
def get_president(login_asso):
  execute(sql.get_asso_president,login_asso)

@task
@runs_once
def delete_asso(login_asso):
  execute(files.del_user,login_asso)
  execute(mail.del_mail,login_asso)
  execute(mail.del_mailings,login_asso)
  execute(web.del_web,login_asso)
  execute(portail.del_portail,login_asso)
  execute(sql.del_sql,login_asso)
  execute(python.del_user,login_asso)
  execute(sql.del_from_portal,login_asso)

@task
@runs_once
def delete_service(login_asso):
  execute(files.del_user,login_asso)
  execute(web.del_web,login_asso)
  execute(portail.del_portail,login_asso)
  execute(sql.del_sql,login_asso)
  execute(python.del_user,login_asso)
  print("If the servie has been modified run delete_asso")
  print("(this will delete the service from the assos website and from the mail server)")
