#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wechat import WeChat
from ldap import OpenLdap
from mail import Email
from ldap3 import MODIFY_REPLACE
import random,string
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Main:
    def __init__(self):
        self.wechat = WeChat()
        self.openldap = OpenLdap()
        self.e_mail = Email()

    def get_wechat_uid_info(self, uid):
        #根据uid获取企业微信中该用户的属性值
        wechat_user_list = self.wechat.get_user_list()
        for info in wechat_user_list:
            for k_info, v_info in info.items():
                if k_info == 'userid':
                    v = v_info.lower()
                    if v == uid:
                        return info

    def get_wechat_gid_info(self, gid):
        #跟据部门id获取企业微信中该部门的属性值
        wechat_department_list = self.wechat.get_department_list()
        for info in wechat_department_list:
            info.pop('id')
            if info.get('name') == gid:
              return info

    def get_wechat_ugid(self, uid):
        #根据uid获取企业微信的部门id,用于排除添加某部门用户
        wechat_user_list = self.wechat.get_user_list()
        for info in wechat_user_list:
            for k_info, v_info in info.items():
                if k_info == 'userid':
                    v = v_info.lower()
                    if v == uid:
                        dep_id = info.get('department')
                        return dep_id

    def sync(self):
        ldap_uid = self.openldap.get_ldap_uid()
        ldap_gid = self.openldap.get_ldap_gid()
        wechat_uid = self.wechat.get_wechat_userid()
        wechat_gid = self.wechat.get_wechat_gid()
        ldap_uid.sort()
        ldap_gid.sort()
        wechat_uid.sort()
        wechat_gid.sort()
        #print ldap_uid
        #print ldap_gid
        #print wechat_uid
        #print wechat_gid
        print('开始同步用户到ldap-server....')
        # 删除不在企业微信的用户
        for l_uid in ldap_uid:
            if l_uid not in wechat_uid:
                uid = ''.join(l_uid)
                if uid not in exclude_list:
                  #print('开始删除ldap用户:%s' % uid)
                  self.openldap.ldap_del_user(uid)

        # 删除不在企业微信的用户组
        #print ldap_gid
        #print wechat_gid
        for l_gid in ldap_gid:
            if l_gid not in wechat_gid:
                gid = l_gid[0]
                print('开始删除ldap用户组:%s' % gid)
                #print(help(self.openldap.ldap_del_group))
                self.openldap.ldap_del_group(gid)

        # 添加新的用户组        
        for w_gid in wechat_gid:
            # 判断微信部门是否已经存在ldap组中
            if w_gid not in ldap_gid:
                # 列表[id]转成字符串id
                #gid = [str(x) for x in w_gid]
                #gid_new = "".join(gid)
                group_name=w_gid[0]
                wechat_gid_info = self.get_wechat_gid_info(group_name)
                # 不存在则向ldap添加部门信息
                def f(name):
                    return self.openldap.ldap_add_group(name)
                f(**wechat_gid_info)
        # 添加用户
        for w_uid in wechat_uid:
            # 判断微信账号是否已经存在ldap中
            if w_uid not in ldap_uid:
                # 不存在则向ldap添加账号信息
                # 列表[uid]转成字符串'uid'
                uid = "".join(w_uid)
                #判断用户是否属于排除添加的部门:合作伙伴(:40)
                exclude = [40]
                wechat_dep_id = self.get_wechat_ugid(uid)
                if wechat_dep_id not in exclude:
                    #添加用户
                    wechat_uid_info = self.get_wechat_uid_info(uid)
                    def f(userid, name, mobile, email, position, department, department_name):
                        print('开始添加ldap用户:%s' % userid)
                        tmp = random.sample(string.ascii_letters + string.digits, 12)
                        passwd=''.join(tmp)
                        # print(userid, name, passwd, mobile, email, department)
                        if self.openldap.ldap_add_user(userid, name, passwd, mobile, email, position, department, department_name):
                            print('开始发送邮件')
                            self.e_mail.send_mail(email, userid, name, passwd)
                    f(**wechat_uid_info)
 
        # 修改/更新组属性
        ldap_group_info=self.openldap.search_group_all()
        ldap_user_info=self.openldap.search_user_all()
        #print ldap_group_info
        #print ldap_user_info
        for group_info in ldap_group_info:
          group_name=group_info.get('attributes').get('cn')
          member_list=group_info.get('attributes').get('uniqueMember')
          member_list.sort()
          uniquemember_list=[]
          #default_member='cn=default,'+self.openldap.user_ou+','+self.openldap.dn
          #uniquemember_list.append(default_member)
          for userinfo in ldap_user_info:
            user_ou=userinfo.get('attributes').get('ou')
            user_cn=userinfo.get('attributes').get('cn')
            if group_name == user_ou:
              user_dn='cn='+user_cn[0]+','+self.openldap.user_ou+','+self.openldap.dn
              uniquemember_list.append(user_dn)
              
              
          uniquemember_list.sort()
          if len(uniquemember_list) == 0:
            continue
          if member_list != uniquemember_list:
            print('开始更新用户组:%s的成员信息...' % group_name[0].encode('utf-8'))
            print "group_name:",group_name[0].encode('utf-8') 
            print member_list
            print uniquemember_list
            #attr={'uniqueMember': [(MODIFY_REPLACE, ['cn=default22,ou=group,dc=yeahgo,dc=com', 'cn=stevenyuan,ou=user,dc=yeahgo,dc=com', 'cn=t1,ou=user,dc=yeahgo,dc=com'])]}
            self.openldap.ldap_update_group_attr(group_name[0], {'uniqueMember': [(MODIFY_REPLACE,uniquemember_list)]})


if __name__ == "__main__":
    r = Main()
    #保留用户
    exclude_list=["cicd",]
    r.sync()
    #r.get_wechat_one_info('MeiCuiCui')
    #r.get_wechat_gid_info(40)
