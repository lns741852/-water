from django.db import models


class GroupTable(models.Model):

    group_no = models.CharField(
        db_column='GROUP_NO', max_length=20,primary_key=True)

    group_name=models.CharField(db_column='GROUP_NAME',max_length=20)
    class Meta:
        managed = False
        db_table = 'GROUP_TABLE'


class ZzEmpTable(models.Model):

    emp_no = models.CharField(
        db_column='EMP_NO', primary_key=True, max_length=20, unique=True)

    emp_name = models.CharField(
        db_column='EMP_NAME', max_length=20)

    dep_no = models.CharField(
        db_column='DEP_NO', max_length=20 )

    comp_no = models.CharField(
        db_column='COMP_NO', max_length=20)
    user_pwd = models.CharField(
        db_column='USER_PWD', max_length=20)
    line_id = models.CharField(
        db_column='line_id', max_length=50)
    tel = models.CharField(max_length=10)
    location_switch = models.IntegerField()
    working = models.IntegerField(db_column='WORKING', blank=True, null=True)  # Field name made lowercase.



    group_no = models.ForeignKey(GroupTable,models.DO_NOTHING,'GROUP_NO', blank=True, null=True, db_column="GROUP_NO",to_field="group_no")
    group_leader = models.IntegerField(
        db_column='GROUP_leader', default='0')
    # group_name=models.ForeignKey()
    class Meta:
        managed = False
        db_table = 'EMP_TABLE'



class CompanyTable(models.Model):

    comp_no = models.CharField(
        db_column='COMP_NO', primary_key=True, max_length=20)

    comp_name = models.CharField(db_column='COMP_NAME', max_length=50)
    main = models.IntegerField(db_column='main')

    class Meta:
        managed = False
        db_table = 'COMPANY_TABLE'


class LocationTable(models.Model):
    id= models.IntegerField( primary_key=True)
    no = models.CharField(max_length=10, blank=True, null=True)
    txt = models.CharField(max_length=25, blank=True, null=True)
    location_lng = models.CharField(max_length=25, blank=True, null=True)
    location_lat = models.CharField(max_length=25, blank=True, null=True)
    location_range = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'location_table'


class EmpLocationTable(models.Model):
    id = models.IntegerField(primary_key=True)
    emp_no = models.CharField(max_length=10, blank=True, null=True)
    group_no = models.CharField(max_length=10, blank=True, null=True)
    location_id = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'emp_location_table'


class PunchTable(models.Model):
    id = models.IntegerField(primary_key=True)
    emp_no = models.CharField(max_length=25, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    section = models.IntegerField(blank=True, null=True)
    work_time = models.DateTimeField(blank=True, null=True)
    gps = models.CharField(max_length=255, blank=True, null=True)
    gps_address = models.CharField(max_length=555, blank=True, null=True)
    distance = models.IntegerField(blank=True, null=True)
    location_id = models.IntegerField(blank=True, null=True)
    u_ip = models.CharField(max_length=255, blank=True, null=True)

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
    u_ip = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'punch_overtime'




class LineEmpError(models.Model):
    line_id = models.CharField(max_length=50, blank=True, null=True)
    error = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'line_emp_error'