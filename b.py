import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

smtpserver = 'smtp.sina.com'
username = 'hi_iamarobot@sina.com'
password = 'robot2018'
# username = 'kaiyuanjieliu2018@163.com'
# password = 'kaiyuanjieliu18'
#password = 'robot2018'
#password = 'hirobot'

sender = 'hi_iamarobot@sina.com'
receivers = 'hi_iamarobot@sina.com,wintersee@outlook.com' # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
subject = '大家好，我开始表演了'
content = '欢愉小胖注意听讲！'
attachment_path = 'C:\workspace\GitHub\data\WebCrawler\WallStreetCN\wall_street_calendar_20180113.txt'
attachment = 'all_street_calendar_20180113.txt'


def send_mail(sender,receivers,subject,content,attachment,attachment_path):
    #创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receivers
    message['Subject'] = Header(subject, 'utf-8')

    # 邮件正文内容
    message.attach(MIMEText(content, 'plain', 'utf-8'))

    # 构造附件1，传送当前目录下的 test.txt 文件
    att1 = MIMEText(open(attachment_path, 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    att1["Content-Disposition"] = 'attachment; filename="'+attachment+'"'
    message.attach(att1)

    try:
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)
        smtp.login(username, password)
        smtp.sendmail(sender, receivers.split(','), message.as_string())
        smtp.quit()
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(e)
        print("Error: 无法发送邮件")

send_mail(sender, receivers, subject, content, attachment, attachment_path)
#
#
# import smtplib
# from email.mime.text import MIMEText
# from email.header import Header
#
# sender = 'from@runoob.com'
# receivers = ['429240967@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
#
# # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
# message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
# message['From'] = Header("菜鸟教程", 'utf-8')
# message['To'] = Header("测试", 'utf-8')
#
# subject = 'Python SMTP 邮件测试'
# message['Subject'] = Header(subject, 'utf-8')
#
# try:
#     smtpObj = smtplib.SMTP('localhost')
#     smtpObj.sendmail(sender, receivers, message.as_string())
#     print
#     "邮件发送成功"
# except smtplib.SMTPException:
#     print
#     "Error: 无法发送邮件"
#
#
#
#
#
#
# import smtplib
# from email.mime.text import MIMEText
# from email.header import Header
#
# sender = '***'
# receiver = '***'
# subject = 'python email test'
# smtpserver = 'smtp.163.com'
# username = '***'
# password = '***'
#
# msg = MIMEText('你好', 'text', 'utf-8')  # 中文需参数‘utf-8’，单字节字符不需要
# msg['Subject'] = Header(subject, 'utf-8')
#
# smtp = smtplib.SMTP()
# smtp.connect('smtp.163.com')
# smtp.login(username, password)
# smtp.sendmail(sender, receiver, msg.as_string())
# smtp.quit()