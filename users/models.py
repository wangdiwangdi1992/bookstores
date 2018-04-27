from hashlib import sha1
from django.db import models
from db.base_model import BaseModel

class PassportManger(models.Manager):
    def add_one_passport(self,username,password,email):
        passport = self.create(username=username,password=get_hash(password),email=email)
        return passport
    def get_one_passport(self,username,password):
        try:
            passport = self.get(username=username,password=get_hash(password))
        # except self.model.DoesNotExist:
        except self.model.DoesNotExist:
            passport = None
        return passport

    def check_passport(self, username):
        '''检查是否存在用户名'''
        try:
            passport = self.get(username=username)
        except self.model.DoesNotExist:
            passport = None
        return passport

class Passport(BaseModel):
    username = models.CharField(max_length=20,verbose_name='用户名')
    password = models.CharField(max_length=40,verbose_name='用户密码')
    email = models.EmailField(verbose_name='用户邮箱')
    is_active = models.BooleanField(default=False,verbose_name='激活状态')

    objects = PassportManger()
    class Meta:
        db_table = 'username_password'
    def __str__(self):
        return self.username
def get_hash(str):
    sh = sha1()
    sh.update(str.encode('utf8'))
    return sh.hexdigest()
class AddressManager(models.Manager):
    def get_default_address(self,passport_id):
        '''查询指定用户的默认收货地址'''
        try:
            addr = self.get(passport_id=passport_id,is_default=True)
        except self.model.DoesNotExist:
            addr = None
        return addr
    def add_one_address(self,passsport_id,recipient_name,recipient_addr,zip_code, recipient_phone):
        '''添加收货地址'''
        # 判断用户是否有默认收货地址
        addr = self.get_default_address(passport_id=passsport_id)
        if addr:
            is_default = False
        else:
            is_default = True
        addr =self.create(passsport_id=passsport_id,
                          recipient_name=recipient_name,
                          recipient_addr=recipient_addr,
                          zip_code=zip_code,
                          recipient_phone=recipient_phone,
                          is_default=is_default)
        return addr
class Address(BaseModel):
    recipient_name = models.CharField(max_length=10,verbose_name='收件人')
    recipient_addr = models.CharField(max_length=256,verbose_name='收件地址')
    zip_code = models.CharField(max_length=6,verbose_name='邮政编码')
    recipient_phone = models.CharField(max_length=11,verbose_name='联系电话')
    is_default = models.BooleanField(default=False,verbose_name='是否默认')
    passport = models.ForeignKey('Passport',verbose_name='账户')

    objects = AddressManager()

    class Meta:
        db_table = 'user_address'
    def __str__(self):
        return self.recipient_name