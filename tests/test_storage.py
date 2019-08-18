from sg_utils import storeBase, db_connect, db_connection, get_cursor
import sg_utils
print("FILE", sg_utils.__file__)

class store(storeBase):
	def create(self):
		self.cursor.execute("CREATE TABLE IF NOT EXISTS storetest (name VARCHAR);")
		self.cursor.execute("insert into storetest values('shashank'),('pokemon')")

	@db_connection
	def select(self):
		cursor = get_cursor()
		cursor.execute("select * from storetest;")
		return cursor.fetchall()

db = None

def setup_module():
	global db
	db = store("test.db")

def teardown_module():
	db.destroy()


def test_connection():
	_,cursor = db.connection()
	cursor.execute("select * from storetest;")
	assert (cursor.fetchall()==[{'name': 'shashank'}, {'name': 'pokemon'}])

def test_execute():
	res = db.execute("select * from storetest where name=?;", ("shashank",))
	assert (res==[{'name': 'shashank'}])
	res = db.execute("select * from storetest where name=?;", ("hello",))
	assert (res==[])


def test_class_deco():
	assert (db.select()==[{'name': 'shashank'}, {'name': 'pokemon'}])

