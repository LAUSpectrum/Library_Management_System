from utils import *


def renew_book(session: Session, member_id, book_isbn):

	records = session.query(Borrow).filter(
		Borrow.member_id == member_id,
		Borrow.book_isbn == book_isbn,
		Borrow.is_active == True,
	).all()

	if records:
		BorrowRecord = records[0]

		if BorrowRecord.left_opportunity > 0:  # he's got opportunity renew this book

			borrow_date = datetime.datetime.now()
			due_date = datetime.datetime.now() + datetime.timedelta(days=30)

			BorrowRecord.borrow_date = borrow_date.strftime("%Y-%m-%d %H:%M:%S")
			BorrowRecord.due_date = due_date.strftime("%Y-%m-%d %H:%M:%S")
			BorrowRecord.left_opportunity -= 1

			print(Fore.GREEN + "请在 {} 之前归还此书, 您还能再续借 {} 次.".format(
				due_date.strftime("%Y-%m-%d %H:%M:%S"), BorrowRecord.left_opportunity))

			session.commit()

			time.sleep(1)
		else: print("you have to return this book on time!")
	else:
		print("no record has been found!")


def return_book(session: Session, member_id, book_isbn):
	records = session.query(Borrow).filter(Borrow.member_id == member_id, Borrow.book_isbn == book_isbn).all()

	if records:
		BorrowRecord = records[0]
		if BorrowRecord.is_active:
			return_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			BorrowRecord.is_active = False
			BorrowRecord.return_date = return_date

			print(Fore.GREEN + "您在 {} 归还了此书.".format(return_date))
			session.commit()
		else:
			print(Fore.RED + "您已经还过此书了!")
	else:
		print(Fore.RED + "没有查找到借阅记录!")


def do_borrow_book(session: Base, member_id):
	while 1:
		books = []
		while 1:
			book_isbn = input(Fore.GREEN + "请输入欲借图书的[ISBN]: ")
			if session.query(Book).filter(Book.isbn == book_isbn).all():
				books.append(book_isbn)
			else:
				print(Fore.RED + "库中暂无此书, 无法借阅")
			if input(Fore.GREEN + "是否输入完毕[Y/N]: ") == 'y':
				borrow_info = [get_borrow_info(member_id, book) for book in books]
				insert_db_data(session, borrow_info, mode="borrow")
				print(Fore.GREEN + "本次已借 {} 本书!".format(len(borrow_info)))
				break
		if input(Fore.GREEN + "是否继续借书[Y/N]: ") == 'n':
			break


def de_renew_book(session: Base, member_id):
	while 1:
		book_isbn = input(Fore.GREEN + "请输入续借图书的[ISBN]: ")
		renew_book(session, member_id, book_isbn)
		if input(Fore.GREEN + "是否继续续借[Y/N]: ") == 'n':
			break


def do_return_book(session: Base, member_id):
	while 1:
		book_isbn = input(Fore.GREEN + "请输入欲还图书的[ISBN]: ")
		return_book(session, member_id, book_isbn)
		if input(Fore.GREEN + "是否继续还书[Y/N]: ") == 'n':
			break


def member_operations(session: Base, member_id):
	print(Fore.GREEN + '您已经以读者身份成功登录!')

	while True:
		print(Fore.GREEN + '您可以借书[B], 还书[R], 或续借[E]')
		choice = input(Fore.GREEN + "请输入您需要的操作: ").lower()

		if choice == "b":
			do_borrow_book(session, member_id)
		elif choice == "r":
			do_return_book(session, member_id)
		elif choice == "e":
			de_renew_book(session, member_id)
		else:
			print(Fore.RED + "请输入目标操作所对应的正确字母!")

		if input(Fore.GREEN + "是否退出读者身份登录[Y/N]: ").lower() == "y": break


def member_page():

	# process the database
	Session = sessionmaker(bind=engine)
	session = Session()

	member_id = input(Fore.GREEN + '请输入您的[读者ID]: ')
	member_password = input(Fore.GREEN + '请输入您的[密码]: ')

	while not find_people(session, Member, member_id, member_password):
		choice = input(Fore.RED + '您的[管理员ID]与[密码]不匹配, 是否重新输入[Y/N]:').lower()

		if choice == "y":
			member_id = input(Fore.GREEN + '请输入您的[管理员ID]: ')
			member_password = input(Fore.GREEN + '请输入您的[密码]: ')

		else:
			session.close()
			return None

	member_operations(session, member_id)
	session.close()

