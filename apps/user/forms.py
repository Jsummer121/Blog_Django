# -*- coding: utf-8 -*-
# @Auther:Summer
from django import forms
from django.db.models import Q
from django_redis import get_redis_connection

from .models import Users


class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=20, min_length=5,
                               error_messages={"min_length": "用户名长度要大于5",
                                               "max_length": "用户名长度要小于20",
                                               "required": "用户名不能为空"}
                               )
    password = forms.CharField(label='密码', max_length=20, min_length=6,
                               error_messages={"min_length": "密码长度要大于6",
                                               "max_length": "密码长度要小于20",
                                               "required": "密码不能为空"}
                               )
    password_repeat = forms.CharField(label='确认密码', max_length=20, min_length=6,
                                      error_messages={"min_length": "密码长度要大于6",
                                                      "max_length": "密码长度要小于20",
                                                      "required": "密码不能为空"}
                                      )
    mobile = forms.CharField(label='手机号', max_length=11, min_length=11,
                             error_messages={"min_length": "手机号长度有误",
                                             "max_length": "手机号长度有误",
                                             "required": "手机号不能为空"})

    sms_code = forms.CharField(label='短信验证码', max_length=6, min_length=6,
                               error_messages={"min_length": "短信验证码长度有误",
                                               "max_length": "短信验证码长度有误",
                                               "required": "短信验证码不能为空"})

    def clean_mo_un(self):
        """校验用户名和手机号是否存在"""
        users = self.cleaned_data.get('username')
        tel = self.cleaned_data.get('mobile')
        if Users.objects.filter(Q(username=users) | Q(mobile=tel)).exists():
            raise forms.ValidationError("用户名或手机号已注册，请重新输入！")
        return users, tel

    def clean(self):
        cleaned_data = super().clean()
        passwd = cleaned_data.get('password')
        passwd_repeat = cleaned_data.get('password_repeat')

        if passwd != passwd_repeat:
            raise forms.ValidationError("两次密码不一致")

        # 校验短信验证码
        tel = cleaned_data.get('mobile')
        sms_text = cleaned_data.get('sms_code')

        # 建立redis连接
        redis_conn = get_redis_connection(alias='verify_codes')
        sms_fmt = "sms_{}".format(tel).encode('utf8')
        real_sms = redis_conn.get(sms_fmt)
        if (not real_sms) or (sms_text != real_sms.decode('utf-8')):
            raise forms.ValidationError("短信验证码错误")


class ChangePswForm(forms.Form):
    password = forms.CharField(label="密码", max_length=20, min_length=6,error_messages={
        "max_length": "密码长度必须小于20位",
        "min_length": "密码长度必须大于6位",
        "required": "密码不能为空"
    })
    password_repeat = forms.CharField(label="确认密码", max_length=20, min_length=6,
                               error_messages={
                                   "max_length": "密码长度必须小于20位",
                                   "min_length": "密码长度必须大于6位",
                                   "required": "密码不能为空"
                               })
    mobile = forms.CharField(label="手机号", max_length=11, min_length=11,
                               error_messages={
                                   "max_length": "手机号长度有误",
                                   "min_length": "手机号长度有无",
                                   "required": "手机号不能为空"})
    sms_code = forms.CharField(label="验证码", max_length=6, min_length=6,
                               error_messages={"max_length": "验证码长度有误",
                                               "min_length": "验证码长度有误",
                                               "required": "验证码不能为空"})

    # 检查手机号是否存在
    def clean_mobile(self):
        tel = self.cleaned_data.get('mobile')
        if not Users.objects.filter(mobile=tel).exists():
            raise forms.ValidationError("手机号输入有误，请重新输入！")
        return tel

    def clean(self):
        cleaned_data = super().clean()
        passwd = cleaned_data.get('password')
        passwd_repeat = cleaned_data.get('password_repeat')

        if passwd != passwd_repeat:
            raise forms.ValidationError("两次密码不一致")

        # 校验短信验证码
        tel = cleaned_data.get('mobile')
        sms_text = cleaned_data.get('sms_code')

        # 建立redis连接
        redis_conn = get_redis_connection(alias='verify_codes')
        sms_fmt = "sms_{}".format(tel).encode('utf8')
        real_sms = redis_conn.get(sms_fmt)
        if (not real_sms) or (sms_text != real_sms.decode('utf-8')):
            raise forms.ValidationError("短信验证码错误")


