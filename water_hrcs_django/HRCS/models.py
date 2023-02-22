from tokenize import group
from django.db import models

# Create your models here.
class Token(models.Model):
    emp_no = models.CharField(db_column='EMP_NO', max_length=20,primary_key=True)  # Field name made lowercase.
    token = models.CharField(max_length=500)
    deadline = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'TOKEN'


class CompanyTable(models.Model):
    comp_id = models.CharField(db_column='COMP_ID', max_length=11)
    comp_no = models.CharField(db_column='COMP_NO', primary_key=True, max_length=20)
    comp_name = models.CharField(db_column='COMP_NAME', max_length=50)
    main = models.CharField(db_column='main', max_length=50)

    class Meta:
        managed = False
        db_table = 'COMPANY_TABLE'




class DepTable(models.Model):
    # Field name made lowercase.
    dep_no = models.CharField(db_column='DEP_NO', primary_key=True, max_length=3)
    # Field name made lowercase.
    dep_name = models.CharField(db_column='DEP_NAME', max_length=20)

    class Meta:
        managed = False
        db_table = 'DEP_TABLE'





class EmpTable(models.Model):
    emp_id = models.CharField(db_column='EMP_ID', max_length=11)  # Field name made lowercase.
    emp_no = models.CharField(db_column='EMP_NO', primary_key=True, max_length=20)  # Field name made lowercase.
    emp_name = models.CharField(db_column='EMP_NAME', unique=True, max_length=20)  # Field name made lowercase.
    comp_no = models.CharField(db_column='COMP_NO', max_length=20)  # Field name made lowercase.
    dep_no = models.CharField(db_column='DEP_NO', max_length=20)  # Field name made lowercase.
    work_position = models.CharField(db_column='WORK_POSITION', max_length=20)  # Field name made lowercase.
    user_pwd = models.CharField(db_column='USER_PWD', max_length=500)  # Field name made lowercase.
    line_id = models.CharField(max_length=50)
    tel = models.CharField(max_length=10, blank=True, null=True)
    group_no = models.CharField(db_column='GROUP_NO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    group_leader = models.IntegerField(db_column='GROUP_leader', blank=True, null=True)  # Field name made lowercase.
    working = models.IntegerField(db_column='WORKING', blank=True, null=True)  # Field name made lowercase.
    auth = models.CharField(db_column='AUTH', max_length=1)  # Field name made lowercase.
    mail = models.CharField(max_length=30)
    location_switch = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'EMP_TABLE'
        unique_together = (('emp_no', 'line_id'),)


class EmpTable_AUTH(models.Model):
    emp_no = models.CharField(db_column='EMP_NO', primary_key=True, max_length=20)  # Field name made lowercase.
    emp_name = models.CharField(db_column='EMP_NAME', unique=True, max_length=20)  # Field name made lowercase.
    auth = models.CharField(db_column='AUTH', max_length=1)  # Field name made lowercase.
    auth_name = models.CharField(db_column='AUTH_NAME', max_length=1)

    class Meta:
        managed = False
        db_table = 'EMP_AUTH_VIEW'


class EmpLocationTable(models.Model):
    id = models.IntegerField(primary_key=True)  # Field name made lowercase.
    emp_no = models.CharField(max_length=10)
    group_no = models.CharField(max_length=10, blank=True, null=True)
    location_id = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'EMP_LOCATION_TABLE'


class GroupTable(models.Model):
    # Field name made lowercase.
    group_no = models.CharField(
        db_column='GROUP_NO', primary_key=True, max_length=20)
    # Field name made lowercase.
    group_name = models.CharField(db_column='GROUP_NAME', max_length=50)

    class Meta:
        managed = False
        db_table = 'GROUP_TABLE'


class MenuTable(models.Model):
    id = models.CharField(db_column='ID', max_length=11)
    menu_no = models.CharField(
        db_column='MENU_NO', primary_key=True, max_length=20)
    menu_name = models.CharField(db_column='MENU_NAME', max_length=50)
    url= models.CharField(db_column='URL', max_length=50)
    parent_no = models.CharField(db_column='PARENTNO', max_length=20)

    class Meta:
        managed = False
        db_table = 'MENU_TABLE'


class AuthMenu(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=11)
    auth_no= models.CharField(db_column='AUTH_NO', max_length=50)
    menu_no = models.CharField(db_column='MENU_NO', max_length=20)

    class Meta:
        managed = False
        db_table = 'auth_menu_table'


class AuthTable(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=11)
    auth_no= models.CharField(db_column='AUTH_NO', max_length=50)
    auth_name = models.CharField(db_column='AUTH_NAME', max_length=20)
    create_date = models.DateTimeField(db_column='CREATE_DATE', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_table'



class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)
    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey(
        'DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

class JwtToken(models.Model):
    username = models.CharField(primary_key=True,max_length=45)
    token = models.CharField(max_length=400)
    exp_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'JWT_TOKEN'



class WorkpositionList(models.Model):
    wp_name = models.CharField(db_column='WP_name', max_length=1)  # Field name made lowercase.
    wp_code = models.CharField(db_column='WP_code', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'workPosition_list'


class LocationTable(models.Model):
    id = models.IntegerField(primary_key=True)  # Field name made lowercase.
    no = models.CharField(max_length=10)
    txt = models.CharField(max_length=50, blank=True, null=True)
    select = models.CharField(max_length=2)
    location_lng = models.CharField(db_column='location_lng', max_length=25, blank=True, null=True)
    location_lat = models.CharField(db_column='location_lat', max_length=25, blank=True, null=True)
    location_range = models.CharField(max_length=100, blank=True, null=True)
    note = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'location_table'


class EmpAndGroupTable(models.Model):
    id = models.IntegerField(primary_key=True)
    location_id = models.CharField(max_length=10, blank=True, null=True)
    emp_name = models.CharField( max_length=25, blank=True, null=True)
    group_name = models.CharField( max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'emp_location_view'


class PunchTable(models.Model):
    id = models.IntegerField(primary_key=True)
    emp_no = models.CharField(max_length=25, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    section = models.IntegerField(blank=True, null=True)
    work_time = models.DateTimeField(blank=True, null=True)
    gps = models.CharField(max_length=255, blank=True, null=True)
    gps_address = models.CharField(max_length=555, blank=True, null=True)
    distance = models.IntegerField(blank=True, null=True)
    in_type = models.IntegerField(blank=True, null=True)
    u_ip = models.CharField(max_length=255, blank=True, null=True)
    location_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'punch_table'


class PunchOvertime(models.Model):
    id = models.IntegerField(primary_key=True)
    emp_no = models.CharField(max_length=25, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    section = models.IntegerField(blank=True, null=True)
    work_time = models.DateTimeField(blank=True, null=True)
    gps = models.CharField(max_length=255, blank=True, null=True)
    gps_address = models.CharField(max_length=555, blank=True, null=True)
    distance = models.IntegerField(blank=True, null=True)
    in_type = models.IntegerField(blank=True, null=True)
    u_ip = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'punch_overtime'

class Action_log(models.Model):
    id = models.IntegerField(primary_key=True)  # Field name made lowercase.
    action = models.CharField(max_length=100)
    content = models.CharField(max_length=5000, blank=True, null=True)
    action_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'action_log'

