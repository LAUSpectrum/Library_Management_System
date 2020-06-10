from sqlalchemy import Column, Integer, String, ForeignKey
from DbConfig import Base

class Admin(Base):
	__tablename__ = 'admins'

	id = Column(String(32), unique=True, nullable=False, primary_key=True)
	name = Column(String(32))
	email = Column(String(32), nullable=True)
	password = Column(String(128), nullable=False)
	# book_isbn = Column(String(32), ForeignKey("books.isbn"))
	# member_id = Column(String(32), ForeignKey("members.id"))

	def set_name(self, name):
		self.name = name

	def set_email(self, email):
		self.email = email

	def set_password(self, password):
		self.password = password

