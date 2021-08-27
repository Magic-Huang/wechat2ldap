# wechat2ldap

企业微信用户同步ldap，实现企业内部账号统一管理

项目来源为https://github.com/hryGithub/wechat2ldap.git
由于ou=group的 objectclass类不是groupOfUniqueNames 所以自己进行了修改
对user的属性也做了一些自己的调整

ou=group,ou=user 需要提前创建
配置文件settings.py
python main.py  （可放到计划任务中 每半小时执行）

功能： 
将企业微信公司下的部门同步到ou=group下
将企业微信下所有的员工同步到ou=user下
将员工和部门通过部门属性uniqueMember进行关联

如果企业微信增加、删除 同步脚本会从ldap中增加、删除用户  并更新部门属性uniqueMember
增加员工时 会从通过企业微信中的企业邮箱发送LDAP用户账号信息给新员工 

另外可以再部署一个自助密码服务 self-service-password https://ltb-project.org/documentation/self-service-password
部署后比如  password.test.com 员工可以自己通过web界面进行密码重置和密码修改  

邮件发送内容在settings.py中配置，如下  这些也是我在公司接入了的项目
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





