import unittest
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QDate
import MySQLdb as mdb

# Import các class cần kiểm thử
from main import Login_w, Dangky_w, Main_w, Chidoan_w, Doanvien_w, Ngdung_w, Taotk_w, widget

class TestQLDV(unittest.TestCase):

    def setUp(self):
        """Khởi tạo kết nối database và xóa dữ liệu thử nghiệm trước khi chạy test."""
        global db
        db = mdb.connect('localhost', 'root', 'Dat@123456', 'qldv')
        cursor = db.cursor()
        cursor.execute("DELETE FROM qldv.login WHERE user LIKE 'testuser%'")
        cursor.execute("DELETE FROM qldv.chidoan WHERE machidoan LIKE 'test%'")
        cursor.execute("DELETE FROM qldv.doanvien WHERE madv LIKE 'test%'")
        db.commit()

    def tearDown(self):
        """Đóng kết nối database sau khi chạy test."""
        global db
        db.close()

    # Kiểm tra chức năng đăng ký
    def test_dang_ky(self):
        # Mẫu dữ liệu đầu vào 1
        un1 = 'testuser1'
        psw1 = 'testpass1'
        Dangky_f.tk.setText(un1)
        Dangky_f.mk.setText(psw1)
        Dangky_f.dk()

        # Kiểm tra xem user đã được thêm vào database chưa
        cursor = db.cursor()
        cursor.execute("SELECT * FROM qldv.login WHERE user = %s AND pass = %s", (un1, psw1))
        kt = cursor.fetchone()
        self.assertIsNotNone(kt, "Tài khoản không được thêm vào database")

        # Mẫu dữ liệu đầu vào 2
        un2 = 'testuser1'
        psw2 = 'testpass2'
        Dangky_f.tk.setText(un2)
        Dangky_f.mk.setText(psw2)
        Dangky_f.dk()

        # Kiểm tra xem user đã được thêm vào database chưa
        cursor = db.cursor()
        cursor.execute("SELECT * FROM qldv.login WHERE user = %s AND pass = %s", (un2, psw2))
        kt = cursor.fetchone()
        self.assertIsNone(kt, "Tài khoản đã tồn tại nhưng vẫn được thêm vào database")

    # Kiểm tra chức năng đăng nhập
    def test_dang_nhap(self):
        # Thêm tài khoản thử nghiệm vào database
        cursor = db.cursor()
        cursor.execute("INSERT INTO qldv.login VALUES (%s, %s)", ('testuser1', 'testpass1'))
        db.commit()

        # Mẫu dữ liệu đầu vào 1
        Login_f.user.setText('testuser1')
        Login_f.pw.setText('testpass1')
        Login_f.login()

        # Kiểm tra xem đã chuyển đến trang chủ chưa
        self.assertEqual(widget.currentIndex(), 2, "Đăng nhập thất bại, không chuyển đến trang chủ")

        # Mẫu dữ liệu đầu vào 2
        Login_f.user.setText('testuser1')
        Login_f.pw.setText('testpass2')
        Login_f.login()

        # Kiểm tra xem đã chuyển đến trang chủ chưa
        self.assertNotEqual(widget.currentIndex(), 2, "Đăng nhập thành công mặc dù mật khẩu sai")

    # Kiểm tra chức năng thêm chi đoàn
    def test_them_chidoan(self):
        # Mẫu dữ liệu đầu vào 1
        Chidoan_f.machidoan.setText('test1')
        Chidoan_f.tenchidoan.setText('Chi đoàn thử nghiệm 1')
        Chidoan_f.ngaythanhlap.setDate(QDate(2023, 1, 1))
        Chidoan_f.tenbithu.setText('Bí thư thử nghiệm 1')
        Chidoan_f.them_chidoan()

        # Kiểm tra xem chi đoàn đã được thêm vào database chưa
        cursor = db.cursor()
        cursor.execute("SELECT * FROM qldv.chidoan WHERE machidoan = %s", ('test1',))
        kt = cursor.fetchone()
        self.assertIsNotNone(kt, "Chi đoàn không được thêm vào database")

        # Mẫu dữ liệu đầu vào 2 (thêm chi đoàn đã tồn tại)
        Chidoan_f.machidoan.setText('test1')
        Chidoan_f.tenchidoan.setText('Chi đoàn thử nghiệm 2')
        Chidoan_f.ngaythanhlap.setDate(QDate(2023, 2, 1))
        Chidoan_f.tenbithu.setText('Bí thư thử nghiệm 2')
        Chidoan_f.them_chidoan()

        # Kiểm tra xem chi đoàn đã được thêm vào database chưa
        cursor = db.cursor()
        cursor.execute("SELECT * FROM qldv.chidoan WHERE machidoan = %s", ('test1',))
        kt = cursor.fetchone()
        self.assertIsNotNone(kt, "Chi đoàn đã tồn tại nhưng vẫn được thêm vào database")

    # Kiểm tra chức năng thêm đoàn viên
    def test_them_doanvien(self):
        # Mẫu dữ liệu đầu vào 1
        Doanvien_f.madoanvien.setText('test1')
        Doanvien_f.tendoanvien.setText('Đoàn viên thử nghiệm 1')
        Doanvien_f.ngayvaodoan.setDate(QDate(2023, 1, 1))
        Doanvien_f.tenchidoan.setCurrentText('Chi đoàn thử nghiệm 1')
        Doanvien_f.chucvu.setCurrentText('Chức vụ 1')
        Doanvien_f.them_doanvien()

        # Kiểm tra xem đoàn viên đã được thêm vào database chưa
        cursor = db.cursor()
        cursor.execute("SELECT * FROM qldv.doanvien WHERE madv = %s", ('test1',))
        kt = cursor.fetchone()
        self.assertIsNotNone(kt, "Đoàn viên không được thêm vào database")

        # Mẫu dữ liệu đầu vào 2 (thêm đoàn viên đã tồn tại)
        Doanvien_f.madoanvien.setText('test1')
        Doanvien_f.tendoanvien.setText('Đoàn viên thử nghiệm 2')
        Doanvien_f.ngayvaodoan.setDate(QDate(2023, 2, 1))
        Doanvien_f.tenchidoan.setCurrentText('Chi đoàn thử nghiệm 2')
        Doanvien_f.chucvu.setCurrentText('Chức vụ 2')
        Doanvien_f.them_doanvien()

        # Kiểm tra xem đoàn viên đã được thêm vào database chưa
        cursor = db.cursor()
        cursor.execute("SELECT * FROM qldv.doanvien WHERE madv = %s", ('test1',))
        kt = cursor.fetchone()
        self.assertIsNotNone(kt, "Đoàn viên đã tồn tại nhưng vẫn được thêm vào database")

    # Kiểm tra chức năng thêm tài khoản người dùng
    def test_them_tk(self):
        # Mẫu dữ liệu đầu vào 1
        Taotk_f.taotk_2.setText('testuser2')
        Taotk_f.taomk.setText('testpass2')
        Taotk_f.tao_tk()

        # Kiểm tra xem tài khoản đã được thêm vào database chưa
        cursor = db.cursor()
        cursor.execute("SELECT * FROM qldv.login WHERE user = %s AND pass = %s", ('testuser2', 'testpass2'))
        kt = cursor.fetchone()
        self.assertIsNotNone(kt, "Tài khoản không được thêm vào database")

        # Mẫu dữ liệu đầu vào 2 (thêm tài khoản đã tồn tại)
        Taotk_f.taotk_2.setText('testuser2')
        Taotk_f.taomk.setText('testpass3')
        Taotk_f.tao_tk()

        # Kiểm tra xem tài khoản đã được thêm vào database chưa
        cursor = db.cursor()
        cursor.execute("SELECT * FROM qldv.login WHERE user = %s AND pass = %s", ('testuser2', 'testpass3'))
        kt = cursor.fetchone()
        self.assertIsNotNone(kt, "Tài khoản đã tồn tại nhưng vẫn được thêm vào database")

# Khởi tạo ứng dụng PyQt6 (không cần thiết cho việc chạy test)
# app = QApplication(sys.argv)
# ... (Khởi tạo các cửa sổ)
Login_f = Login_w()
Dangky_f = Dangky_w()
Main_f = Main_w()
Chidoan_f = Chidoan_w()
Doanvien_f = Doanvien_w()
Ngdung_f = Ngdung_w()
Taotk_f = Taotk_w()

# Chạy test
if __name__ == '__main__':
    unittest.main()