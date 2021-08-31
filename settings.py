#!/usr/bin/env python
# -*- coding: utf-8 -*-

# wechat
WECHAT_CORPID = 'test'      # 企业ID
WECHAT_SECRET = 'test'    # 通讯录secrete
WECHAT_DEPART_ID = 1  # 部门id
WECHAT_FETCH_CHILD = 1  # 是否递归获取子部门(1-递归获取，0-只获取本部门)


# ldap
LDAP_HOST = '127.0.0.1' 
LDAP_PORT = 389
LDAP_BINDDN = 'cn=Manager,dc=test,dc=com' 
LDAP_BINDPW = '123456'
LDAP_BASE = 'dc=test,dc=com'
LDAP_USER_OU = 'ou=user'  # 用户所在的ou，需要提前创建
LDAP_GROUP_OU = 'ou=group' # 部门所在的ou，需要提前创建
EXCLUDE_LIST=["cicd",]  #保留用户 用于公共账号配置

# mail
SMTP_HOST = 'smtp.sina.com'
SMTP_PORT = 465
SMTP_USER = 'testservice@sina.com'
SMTP_PASSWD = '958bf56e3eaba9fe'

MESSAGE = """
<p>LDAP账号可用于登入 Gitlab、jira 、wiki、yearning、jenkins、apollo等平台</p>
<p>gitlab : <a href="http://git.ops.test.com">http://git.ops.test.com</a><P>
<p>wiki : <a href="http://wiki.ops.test.com">http://wiki.ops.test.com</a><P>
<p>jira : <a href="http://jira.ops.test.com">http://jira.ops.test.com</a><P>
<p>jenkins : <a href="http://jenkins.ops.test.com">http://jenkins.ops.test.com</a><P>
<p>yearning : <a href="http://yearning.ops.test.com">http://yearning.ops.test.com</a><P>
<p>apollo : <a href="http://apollo.ops.test.com">http://apollo.ops.test.com</a><P>
<p>用户名：%s (用户名默认为员工企业邮箱的前缀)</p>
<p>密码：%s</p>
<p>请妥善保存您的账号密码，如有遗忘您可以访问后面的链接修改默认密码：<a href="http://password.ops.test.com">重置密码链接</a></p>
<p></p>
<p><b> 系统自动发送，勿回复！如有账号使用问题，请联系基础架构部协助处理。</b></p>
"""
