# Library_Management_System
## 1. 需求手册

1.  两种用户权限, 读者和管理员
2.  管理员权限中的方法: 
    1.  增删管理员
    2.  录入删除书籍
    3.  查询借阅记录: 按照图书信息, 或读者信息来查询
3.  读者权限中的方法:
    1.  借阅图书
    2.  归还图书
    3.  续借图书

## 2. 具体实现

### 2.1 数据库部分

1.  Table 1: Member
    1.  ID (登录, 查询借阅记录用)
    2.  Name (登录, 查询借阅记录用)
    3.  Password (登录用)
    4.  Email (可选, 发邮件提示还书用)
2.  Table 2: Admin
    1.  ID (登录用)
    2.  Name (登录用)
    3.  Password (登录用)
    4.  Email (无用)
3.  Table 3: Book
    1.  ISBN (查询借阅记录用)
    2.  Name (查询借阅记录用)
    3.  Author (查询借阅记录用)
    4.  Publisher (查询借阅记录用)
    5.  Release Date (查询借阅记录用)
4.  Table 4: Borrow
    1.  Book_ISBN (查询借阅记录用)
    2.  Member_ID (查询借阅记录用)
    3.  Borrow_Date (借出日期)
    4.  Due_Date (应还日期)
    5.  Return_Date (归还日期, 默认为Null)
    6.  Left_Opportunities (该借书人对此书的剩余续借次数)
    7.  Is_Active (判断该记录中的书在借还是已归还)

TODO: 

1.  实现每天扫描借阅记录的应还日期, 对于应还书的用户发送邮件提醒
2.  用户或管理员登录的时候, 可以通过邮箱, 用户名, 用户ID多种方式登录
3.  登录验证码

### 2.2 GUI部分

TODO: 用wxPython实现GUI

### 2.3 推荐系统部分

TODO: 用机器学习方法实现图书推荐系统

1.  借阅成功之后, 基于读者的借阅记录推荐3本他可能感兴趣的书籍
2.  借阅失败之后, 基于读者的查询内容和兴趣偏好推荐他可能需要的书籍

