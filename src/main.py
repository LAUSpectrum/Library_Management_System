from colorama import init, Fore
from operations.admin import admin_page
from operations.member import member_page
init(autoreset=True)


def main():
	while 1:
		user_type = input(Fore.GREEN + '请输入您的身份. 管理员[A], 读者[M]:').lower()

		# do-while
		while user_type != 'm' and user_type != 'a':
			user_type = input(Fore.RED + '请输入字母[A]或[M]: ').lower()

		if user_type == "a":
			admin_page()
		elif user_type == "m":
			member_page()

		if input(Fore.GREEN + "是否关闭页面[Y/N]").lower() == "y": break


if __name__ == "__main__":
	main()
