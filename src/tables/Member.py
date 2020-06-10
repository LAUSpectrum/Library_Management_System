from sqlalchemy import Column, Integer, String, DateTime
from DbConfig import Base


class Member(Base):
	__tablename__ = 'members'

	id = Column(String(32), unique=True, nullable=False, primary_key=True)
	name = Column(String(32))
	email = Column(String(32), nullable=True)
	password = Column(String(128), nullable=False)
	# create_time = Column(DateTime, comment="数据创建日期")
	# update_time = Column(DateTime, comment="数据更新日期")


	def set_name(self, name):
		self.name = name

	def set_email(self, email):
		self.email = email

	def set_password(self, password):
		self.password = password
