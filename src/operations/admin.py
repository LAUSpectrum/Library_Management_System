from utils import *


def do_admin(session: Base):
	while 1:
		print(Fore.GREEN + "您可以添加管理员[A], 删除管理员[R]")
		choice = input(Fore.GREEN + "请输入您需要的操作: ").lower()

		# 添加管理员
		if choice == "a":
			all_infos = []
			print(Fore.GREEN + "请输入您需要添加的管理员信息:")
			while 1:
				while 1:
					new_id = input(Fore.GREEN + "待添加新管理员[ID]: ")
					if session.query(Admin).filter(Admin.id == new_id).all():
						print(Fore.RED + "该[ID]已被占用, 请重新输入!")
					else:
						break
				new_name = input(Fore.GREEN + "待添加新管理员[姓名]: ")
				new_password = input(Fore.GREEN + "待添加新管理员[密码]: ")
				new_email = input(Fore.GREEN + "待添加新管理员[邮箱]: ")

				all_infos.append([new_id, new_name, new_email, new_password])

				if input(Fore.GREEN + "是否继续添加[Y/N]: ").lower() == "n":
					break

			insert_db_data(session, get_admin_info(all_infos), "admin")  # 判断是否重名
			print(Fore.GREEN + "已成功添加 {} 个新管理员!".format(len(all_infos)))

		# 删除现有的管理员
		if choice == "r":
			print(Fore.GREEN + "请输入您待删除的管理员信息:")
			count = 0
			while 1:
				rm_id = input(Fore.GREEN + "待删除管理员[ID]: ")

				if session.query(Admin).filter(Admin.id == rm_id).all():
					session.query(Admin).filter(Admin.id == rm_id).delete(synchronize_session=False)
					count += 1
					session.commit()
				else:
					print(Fore.RED + "查无此人!")

				if input(Fore.GREEN + "是否结束输入[Y/N]:").lower() == "y":
					print(Fore.GREEN + "已成功删除 {} 个新管理员!".format(count))
					break

		if input(Fore.GREEN + "是否继续增删管理员[Y/N]: ").lower() == "n": break


def do_books(session: Base):
	while 1:
		print(Fore.GREEN + "您可以添加图书[A], 删除图书[R]")
		choice = input(Fore.GREEN + "请输入您需要的操作: ").lower()

		# 添加图书
		if choice == "a":
			all_infos = []
			print(Fore.GREEN + "请输入您待添加的图书信息:")
			while 1:
				while 1:
					new_idsn = input(Fore.GREEN + "添加图书[ISBN]: ")
					if session.query(Book).filter(Book.isbn == new_idsn).all():
						print(Fore.RED + "图书已经在库, 请重新输入!")
					else:
						break
				new_name = input(Fore.GREEN + "待添加图书[书名]: ")
				new_author = input(Fore.GREEN + "待添加图书[作者]: ")
				new_publisher = input(Fore.GREEN + "待添加图书[出版社]: ")
				new_release_date = input(Fore.GREEN + "待添加图书[出版日期]: ")

				all_infos.append([new_idsn, new_name, new_author, new_publisher, new_release_date])

				if input(Fore.GREEN + "是否继续添加[Y/N]: ").lower() == "n":
					break

			insert_db_data(session, get_book_info(all_infos), "book")  # 判断是否重名
			print(Fore.GREEN + "已成功添加 {} 本新图书!".format(len(all_infos)))

		# 删除现有的图书
		if choice == "r":
			print(Fore.GREEN + "请输入您待删除的图书信息:")
			count = 0
			while 1:
				rm_isbn = input(Fore.GREEN + "待删除图书的[ISBN]: ")

				if session.query(Book).filter(Book.isbn == rm_isbn).all():
					session.query(Book).filter(Book.isbn == rm_isbn).delete(synchronize_session=False)
					count += 1
					session.commit()
				else:
					print(Fore.RED + "查无此书!")

				if input(Fore.GREEN + "是否结束输入[Y/N]:").lower() == "y":
					print(Fore.GREEN + "已成功删除 {} 本图书!".format(count))
					break

		if input(Fore.GREEN + "是否继续增删书籍[Y/N]: ").lower() == "n": break


def do_records(session: Base):
	while 1:
		choice = input(Fore.GREEN + "可根据读者ID查找借阅记录[M], 或根据图书ISBN查找[B]: ").lower()  # TODO: 根据时间查找

		if choice == "m":
			while 1:
				member_id = input(Fore.GREEN + "请输入读者的[ID]: ")
				query_results = session.query(Borrow).filter(Borrow.member_id == member_id).all()
				if query_results:
					show_borrow_record(session, query_results)
				else:
					print(Fore.RED + "没有此用户的借阅记录!")

				if input(Fore.GREEN + "是否继续按照读者ID查询[Y/N]: ").lower() == "n":
					break

		if choice == "b":
			while 1:
				book_isbn = input(Fore.GREEN + "请输入图书的[ISBN]: ")

				query_results = session.query(Borrow).filter(Borrow.book_isbn == book_isbn).all()
				if query_results:
					show_borrow_record(session, query_results)
				else:
					print(Fore.RED + "没有此书的借阅记录!")

				if input(Fore.GREEN + "是否继续按照图书ISBN查询[Y/N]: ").lower() == "n":
					break

		if input(Fore.GREEN + "是否继续查询[Y/N]: ").lower() == "n": break


def admin_operations(session: Base):

	print(Fore.GREEN + '您已经以管理员身份成功登录!')

	while True:
		print(Fore.GREEN + '您可以添加删除管理员[A], 增删查改书籍信息[B], 或者查看借阅记录[R]')
		choice = input(Fore.GREEN + "请输入您需要的操作: ").lower()

		if choice == "a":
			do_admin(session)
		elif choice == "b":
			do_books(session)
		elif choice == "r":
			do_records(session)
		else:
			print(Fore.RED + "请输入目标操作所对应的正确字母!")

		if input(Fore.GREEN + "是否退出管理员身份登录[Y/N]: ").lower() == "y": break


def admin_page():

	# process the database
	Session = sessionmaker(bind=engine)
	session = Session()

	admin_id = input(Fore.GREEN + '请输入您的[管理员ID]: ')
	admin_password = input(Fore.GREEN + '请输入您的[密码]: ')

	while not find_people(session, Admin, admin_id, admin_password):
		print(Fore.RED + '您的[管理员ID]与[密码]不匹配, 是否重新输入请输入[Y/N]:')
		choice = input().lower()

		if choice == "y":
			admin_id = input(Fore.GREEN + '请输入您的[管理员ID]: ')
			admin_password = input(Fore.GREEN + '请输入您的[密码]: ')

		else:
			session.close()
			return None

	admin_operations(session)
	session.close()
