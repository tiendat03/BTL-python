import sys
from PyQt6 import QtCore, QtGui, QtWidgets,uic
from PyQt6.QtWidgets import *
from PyQt6.uic import *
import MySQLdb as mdb
db = mdb.connect('localhost', 'root', 'Dat@123456', 'qldv')

# cửa sổ login
class Login_w(QMainWindow):
    def __init__(self):
        super(Login_w,self).__init__()
        uic.loadUi('Login.ui',self)
        self.btnDangnhap.clicked.connect(self.login)
        self.tbnDangky.clicked.connect(self.dk_f)

    def dk_f(self):
        widget.setCurrentIndex(1)

    def login(self):
        un = self.user.text()
        psw = self.pw.text()
        query = db.cursor()
        query.execute("SELECT * FROM qldv.user where  user= '"+un+"' and pass= '"+psw+"'  ")
        kt = query.fetchone()
        if kt:
            QMessageBox.information(self,"Login output", "Đăng nhập thành công")
            widget.setCurrentIndex(2)
        else:
            QMessageBox.information(self,"Login output", "Đăng nhập thất bại")

# cửa sổ đăng ký
class Dangky_w(QMainWindow):
    def __init__(self):
        super(Dangky_w,self).__init__()
        uic.loadUi('Dangky.ui',self)
        self.tbnDK.clicked.connect(self.dk)


    def dk(self):
        un = self.tk.text()
        psw = self.mk.text()
        query = db.cursor()
        query.execute("SELECT * FROM qldv.user where  user= '"+un+"' and pass= '"+psw+"'  ")
        kt = query.fetchone()
        if kt:
            QMessageBox.information(self,"Reg output", "Tài khoản đã tồn tại")
        else:
            query.execute("insert into qldv.user values ('"+un+"', '"+psw+"')")
            db.commit()
            QMessageBox.information(self,"Reg output", "Đăng ký thành công")
            widget.setCurrentIndex(0)

# cửa sổ trang chủ
class Main_w(QMainWindow):
    def __init__(self):
        super(Main_w,self).__init__()
        uic.loadUi('trangchu.ui',self)
        self.tobchidoan.clicked.connect(self.chidoan_a)
        self.tobdoanvien.clicked.connect(self.doanvien_a)
        self.tobnguoidung.clicked.connect(self.ngdung_a)
        self.toboatdong.clicked.connect(self.hd_a)
        self.tobdangxuat.clicked.connect(self.dang_xuat)

    def dang_xuat(self):
        Login_f.user.setText('')
        Login_f.pw.setText('')
        widget.setCurrentIndex(0)
    def chidoan_a(self):
        widget.setCurrentIndex(3)

    def doanvien_a(self):
        widget.setCurrentIndex(4)

    def ngdung_a(self):
        widget.setCurrentIndex(5)

    def hd_a(self):
        widget.setCurrentIndex(6)


# Cửa sổ chi đoàn
class Chidoan_w(QMainWindow):
    def __init__(self):
        super(Chidoan_w,self).__init__()
        uic.loadUi('qlchidoan.ui',self)

        # Kết nối các tín hiệu với hàm xử lý
        self.tobdoanvien.clicked.connect(self.doanvien_a)
        self.tobnguoidung.clicked.connect(self.ngdung_a)
        self.toboatdong.clicked.connect(self.hd_a)
        self.btnThemchidoan.clicked.connect(self.them_chidoan)
        self.tbnTimchidoan.clicked.connect(self.tim_chidoan)
        self.btnSuachidoan.clicked.connect(self.sua_chidoan)  # Nút sửa chi đoàn
        self.btnXoachidoan.clicked.connect(self.xoa_chidoan)
        self.tobdangxuat.clicked.connect(self.dang_xuat)


        # Load dữ liệu chi đoàn ban đầu
        self.load_chidoan()

        # Thiết lập tín hiệu cho bảng chi đoàn
        self.tablechidoan.cellClicked.connect(self.hien_thi_chitiet)

    def dang_xuat(self):
        Login_f.user.setText('')
        Login_f.pw.setText('')
        widget.setCurrentIndex(0)
    def doanvien_a(self):
        widget.setCurrentIndex(4)

    def ngdung_a(self):
        widget.setCurrentIndex(5)

    def hd_a(self):
        widget.setCurrentIndex(6)

    def load_chidoan(self):
        """Load dữ liệu chi đoàn từ database vào bảng."""
        cursor = db.cursor()
        cursor.execute("SELECT * FROM qldv.chidoan")
        data = cursor.fetchall()
        self.tablechidoan.setRowCount(len(data))
        self.tablechidoan.setColumnCount(4)
        self.tablechidoan.setHorizontalHeaderLabels(["Mã Chi Đoàn", "Tên Chi Đoàn", "Ngày Thành Lập", "Tên Bí Thư"])

        # Thêm dữ liệu vào bảng
        for i, row in enumerate(data):
            for j, col in enumerate(row):
                item = QTableWidgetItem(str(col))
                self.tablechidoan.setItem(i, j, item)

    def them_chidoan(self):
        """Thêm mới một chi đoàn."""
        machidoan = self.machidoan.text()
        tenchidoan = self.tenchidoan.text()
        ngaythanhlap = self.ngaythanhlap.date().toString("yyyy-MM-dd")
        tenbithu = self.tenbithu.text()

        # Kiểm tra trường nhập liệu
        if not all(
                [machidoan, tenchidoan, ngaythanhlap, tenbithu]
        ):
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return

        # Thêm đoàn viên vào database
        cursor = db.cursor()
        query = """
        INSERT INTO qldv.chidoan (
            machidoan, tenchidoan, ngaythanhlap, tenbithu
        ) VALUES (%s, %s, %s, %s)
        """
        values = (
            machidoan,
            tenchidoan,
            ngaythanhlap,
            tenbithu,
        )
        try:
            cursor.execute(query, values)
            db.commit()
            QMessageBox.information(self, "Thông báo", "Thêm đoàn viên thành công!")
            self.load_chidoan()
        except mdb.Error as e:
            QMessageBox.information(self, "Thông báo", "Đoàn viên đã tồn tại!")

    def tim_chidoan(self):
        """Tìm kiếm chi đoàn."""
        tukhoa = self.Timchidoan.text()
        if not tukhoa:
            self.load_chidoan()
            return

        cursor = db.cursor()
        query = """
        SELECT * FROM qldv.chidoan
        WHERE machidoan LIKE %s OR tenchidoan LIKE %s OR tenbithu LIKE %s
        """
        values = (f"%{tukhoa}%", f"%{tukhoa}%", f"%{tukhoa}%")
        try:
            cursor.execute(query, values)
            data = cursor.fetchall()
            self.tablechidoan.setRowCount(len(data))
            self.tablechidoan.setColumnCount(4)
            self.tablechidoan.setHorizontalHeaderLabels(
                ["Mã Chi Đoàn", "Tên Chi Đoàn", "Ngày Thành Lập", "Tên Bí Thu"]
            )
            for i, row in enumerate(data):
                for j, col in enumerate(row):
                    item = QTableWidgetItem(str(col))
                    self.tablechidoan.setItem(i, j, item)
        except mdb.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi tìm kiếm chi đoàn: {e}")

    def hien_thi_chitiet(self, row, col):
        """Hiển thị chi tiết chi đoàn khi click vào hàng trong bảng."""
        machidoan = self.tablechidoan.item(row, 0).text()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM qldv.chidoan WHERE machidoan = %s", (machidoan,))
        data = cursor.fetchone()

        # Hiển thị thông tin chi tiết
        self.machidoan.setText(data[0])
        self.tenchidoan.setText(data[1])
        self.ngaythanhlap.setDate(QtCore.QDate.fromString(data[2], "yyyy-MM-dd"))
        self.tenbithu.setText(data[3])

    def sua_chidoan(self):
        """Sửa thông tin chi đoàn."""
        machidoan = self.machidoan.text()
        tenchidoan = self.tenchidoan.text()
        ngaythanhlap = self.ngaythanhlap.date().toString("yyyy-MM-dd")
        tenbithu = self.tenbithu.text()

        # Kiểm tra trường nhập liệu
        if not all(
                [machidoan, tenchidoan, ngaythanhlap, tenbithu]
        ):
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return

        # Cập nhật thông tin đoàn viên vào database
        cursor = db.cursor()
        query = """
        UPDATE qldv.chidoan SET
            tenchidoan = %s, ngaythanhlap = %s, tenbithu = %s
        WHERE machidoan = %s
        """
        values = (
            tenchidoan,
            ngaythanhlap,
            tenbithu,
            machidoan,
        )
        try:
            cursor.execute(query, values)
            db.commit()
            QMessageBox.information(self, "Thông báo", "Sửa đoàn viên thành công!")
            self.load_chidoan()
        except mdb.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi sửa đoàn viên: {e}")

    def xoa_chidoan(self):
        """Xóa chi đoàn."""
        # Lấy dòng được chọn
        selected_rows = self.tablechidoan.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một chi đoàn để xóa!")
            return

        # Lấy mã chi đoàn từ dòng được chọn
        row = selected_rows[0].row()
        machidoan = self.tablechidoan.item(row, 0).text()

        # Xác nhận xóa chi đoàn
        reply = QMessageBox.question(self, "Xóa chi đoàn", f"Bạn có chắc chắn muốn xóa chi đoàn có mã {machidoan}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Xóa chi đoàn khỏi database
            cursor = db.cursor()
            query = "DELETE FROM qldv.chidoan WHERE machidoan = %s"
            try:
                cursor.execute(query, (machidoan,))
                db.commit()
                QMessageBox.information(self, "Thông báo", "Xóa chi đoàn thành công!")
                self.load_chidoan()
            except mdb.Error as e:
                QMessageBox.critical(self, "Lỗi", f"Lỗi xóa chi đoàn: {e}")



# cửa sổ đoàn viên
class Doanvien_w(QMainWindow):
    def __init__(self):
        super(Doanvien_w,self).__init__()
        uic.loadUi('qldoanvien.ui',self)
        self.tobchidoan.clicked.connect(self.chidoan_a)
        self.tobnguoidung.clicked.connect(self.ngdung_a)
        self.toboatdong.clicked.connect(self.hd_a)
        self.tobdangxuat.clicked.connect(self.dang_xuat)
        self.btnThemdoanvien.clicked.connect(self.them_doanvien)
        self.tbnTimdoanvien.clicked.connect(self.tim_doanvien)
        self.btnSuadoanvien.clicked.connect(self.sua_doanvien)
        self.btnXoadoanvien.clicked.connect(self.xoa_doanvien)
        self.dsdoanvien.cellClicked.connect(self.hien_thi_chitiet)

        # Load danh sách đoàn viên ban đầu
        self.load_doanvien()
        self.load_chucvu_combobox()
        self.load_chidoan_combobox()

    def dang_xuat(self):
        Login_f.user.setText('')
        Login_f.pw.setText('')
        widget.setCurrentIndex(0)

    def chidoan_a(self):
        widget.setCurrentIndex(3)

    def ngdung_a(self):
        widget.setCurrentIndex(5)

    def hd_a(self):
        widget.setCurrentIndex(6)

    def load_doanvien(self):
        """Load dữ liệu đoàn viên từ database vào bảng."""
        cursor = db.cursor()
        cursor.execute("SELECT * FROM qldv.doanvien")
        data = cursor.fetchall()
        self.dsdoanvien.setRowCount(len(data))
        self.dsdoanvien.setColumnCount(5)
        self.dsdoanvien.setHorizontalHeaderLabels(
            ["Mã Đoàn Viên", "Tên Đoàn Viên", "Ngày Vào Đoàn", "Tên Chi Đoàn", "Chức Vụ"]
        )

        # Thêm dữ liệu vào bảng
        for i, row in enumerate(data):
            for j, col in enumerate(row):
                item = QTableWidgetItem(str(col))
                self.dsdoanvien.setItem(i, j, item)



    def them_doanvien(self):
        """Thêm mới một đoàn viên."""
        madoanvien = self.madoanvien.text()
        tendoanvien = self.tendoanvien.text()
        ngayvaodoan = self.ngayvaodoan.date().toString("yyyy-MM-dd")
        tenchidoan = self.tenchidoan.currentText()
        chucvu = self.chucvu.currentText()

        # Kiểm tra trường nhập liệu
        if not all(
                [madoanvien, tendoanvien, ngayvaodoan, tenchidoan, chucvu]
        ):
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return

        # Thêm đoàn viên vào database
        cursor = db.cursor()
        query = """
        INSERT INTO qldv.doanvien (
            madv, tendv, ngayvaodoan, tenchidoan, chucvu
        ) VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            madoanvien,
            tendoanvien,
            ngayvaodoan,
            tenchidoan,
            chucvu,
        )
        try:
            cursor.execute(query, values)
            db.commit()
            QMessageBox.information(self, "Thông báo", "Thêm đoàn viên thành công!")
            self.load_doanvien()
        except mdb.Error as e:
            QMessageBox.information(self, "Thông báo", "Đoàn viên đã tồn tại!")

    def tim_doanvien(self):
        """Tìm kiếm đoàn viên."""
        tukhoa = self.Timdoanvien.text()
        if not tukhoa:
            self.load_doanvien()
            return

        cursor = db.cursor()
        query = """
        SELECT * FROM qldv.doanvien
        WHERE madv LIKE %s OR tendv LIKE %s OR tenchidoan LIKE %s
        """
        values = (f"%{tukhoa}%", f"%{tukhoa}%", f"%{tukhoa}%")
        try:
            cursor.execute(query, values)
            data = cursor.fetchall()
            self.dsdoanvien.setRowCount(len(data))
            self.dsdoanvien.setColumnCount(5)
            self.dsdoanvien.setHorizontalHeaderLabels(
                ["Mã Đoàn Viên", "Tên Đoàn Viên", "Ngày Vào Đoàn", "Tên Chi Đoàn", "Chức Vụ"]
            )
            for i, row in enumerate(data):
                for j, col in enumerate(row):
                    item = QTableWidgetItem(str(col))
                    self.dsdoanvien.setItem(i, j, item)
        except mdb.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi tìm kiếm đoàn viên: {e}")

    def load_chidoan_combobox(self):
        """Load danh sách chi đoàn vào combobox."""
        cursor = db.cursor()
        cursor.execute("SELECT tenchidoan, machidoan FROM qldv.chidoan")
        data = cursor.fetchall()
        self.tenchidoan.clear()
        for ten, ma in data:
            self.tenchidoan.addItem(ten, ma)  # Thêm item với dữ liệu liên kết

    def load_chucvu_combobox(self):
        """Load danh sách chức vụ vào combobox."""
        cursor = db.cursor()
        cursor.execute("SELECT chucvu, machucvu FROM qldv.chucvu")
        data = cursor.fetchall()
        self.chucvu.clear()
        for ten, ma in data:
            self.chucvu.addItem(ten, ma)  # Thêm item với dữ liệu liên kết

    def hien_thi_chitiet(self, row, col):
        """Hiển thị chi tiết đoàn viên khi click vào hàng trong bảng."""
        madoanvien = self.dsdoanvien.item(row, 0).text()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM qldv.doanvien WHERE madv = %s", (madoanvien,))
        data = cursor.fetchone()

        # Hiển thị thông tin chi tiết
        self.madoanvien.setText(data[0])
        self.tendoanvien.setText(data[1])
        self.ngayvaodoan.setDate(QtCore.QDate.fromString(data[2], "yyyy-MM-dd"))
        self.tenchidoan.setCurrentText(data[3])
        self.chucvu.setCurrentText(data[4])


    def sua_doanvien(self):
        """Sửa thông tin đoàn viên."""
        madoanvien = self.madoanvien.text()
        tendoanvien = self.tendoanvien.text()
        ngayvaodoan = self.ngayvaodoan.date().toString("yyyy-MM-dd")
        tenchidoan = self.tenchidoan.currentText()
        chucvu = self.chucvu.currentText()


        # Kiểm tra trường nhập liệu
        if not all(
                [madoanvien, tendoanvien, ngayvaodoan, tenchidoan, chucvu]
        ):
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return

        # Cập nhật thông tin đoàn viên vào database
        cursor = db.cursor()
        query = """
        UPDATE qldv.doanvien SET
            tendv = %s, ngayvaodoan = %s, tenchidoan = %s, chucvu = %s
        WHERE madv = %s
        """
        values = (
            tendoanvien,
            ngayvaodoan,
            tenchidoan,
            chucvu,
            madoanvien,
        )
        try:
            cursor.execute(query, values)
            db.commit()
            QMessageBox.information(self, "Thông báo", "Sửa đoàn viên thành công!")
            self.load_doanvien()
        except mdb.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi sửa đoàn viên: {e}")

    def xoa_doanvien(self):
        """Xóa đoàn viên."""
        # Lấy dòng được chọn
        selected_rows = self.dsdoanvien.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một đoàn viên để xóa!")
            return

        # Lấy mã đoàn viên từ dòng được chọn
        row = selected_rows[0].row()
        madoanvien = self.dsdoanvien.item(row, 0).text()

        # Xác nhận xóa đoàn viên
        reply = QMessageBox.question(
            self,
            "Xóa đoàn viên",
            f"Bạn có chắc chắn muốn xóa đoàn viên có mã {madoanvien}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            # Xóa đoàn viên khỏi database
            cursor = db.cursor()
            query = "DELETE FROM qldv.doanvien WHERE madv = %s"
            try:
                cursor.execute(query, (madoanvien,))
                db.commit()
                QMessageBox.information(
                    self, "Thông báo", "Xóa đoàn viên thành công!"
                )
                self.load_doanvien()
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Lỗi xóa đoàn viên: {e}")

    def load_chidoan_combobox(self):
        """Load danh sách chi đoàn vào combobox."""
        cursor = db.cursor()
        cursor.execute("SELECT tenchidoan, machidoan FROM qldv.chidoan")
        data = cursor.fetchall()
        self.tenchidoan.clear()
        for ten, ma in data:
            self.tenchidoan.addItem(ten, ma)  # Thêm item với dữ liệu liên kết

        cursor = db.cursor()
        cursor.execute("SELECT machucvu, chucvu FROM qldv.chucvu")
        data = cursor.fetchall()
        self.chucvu.clear()
        for ma, ten in data:
            self.chucvu.addItem(ten, ma)

class Ngdung_w(QMainWindow):
    def __init__(self):
        super(Ngdung_w,self).__init__()
        uic.loadUi('qlngdung.ui',self)
        self.tobchidoan.clicked.connect(self.chidoan_a)
        self.tobdoanvien.clicked.connect(self.doanvien_a)
        self.tobdangxuat.clicked.connect(self.dang_xuat)
        self.toboatdong.clicked.connect(self.hd_a)
        self.btnThemtkngdung.clicked.connect(self.themtk)
        self.btnSuatkngdung.clicked.connect(self.sua_tk)
        self.btnXoatkngdung.clicked.connect(self.xoa_tk)
        self.tbnTimngdung.clicked.connect(self.tim_tk)
        self.dstk.cellClicked.connect(self.hien_thi_chitiet)

        self.load_tk()

    def themtk(self):
        widget.setCurrentIndex(6)
    def dang_xuat(self):
        Login_f.user.setText('')
        Login_f.pw.setText('')
        widget.setCurrentIndex(0)
    def chidoan_a(self):
        widget.setCurrentIndex(3)

    def doanvien_a(self):
        widget.setCurrentIndex(4)

    def hd_a(self):
        widget.setCurrentIndex(6)

    def load_tk(self):
        """Load user accounts from the database into the table."""
        cursor = db.cursor()
        cursor.execute("SELECT * FROM qldv.user")
        data = cursor.fetchall()
        self.dstk.setRowCount(len(data))
        self.dstk.setColumnCount(2)
        self.dstk.setHorizontalHeaderLabels(["Tài Khoản", "Mật Khẩu"])

        # Add data to the table
        for i, row in enumerate(data):
            for j, col in enumerate(row):
                item = QTableWidgetItem(str(col))
                self.dstk.setItem(i, j, item)

    def tim_tk(self):
        """Search for user accounts."""
        tukhoa = self.Timngdung.text()
        if not tukhoa:
            self.load_tk()
            return

        cursor = db.cursor()
        query = "SELECT * FROM qldv.user WHERE user LIKE %s"
        values = (f"%{tukhoa}%",)
        try:
            cursor.execute(query, values)
            data = cursor.fetchall()
            self.dstk.setRowCount(len(data))
            self.dstk.setColumnCount(2)
            self.dstk.setHorizontalHeaderLabels(["Tài Khoản", "Mật Khẩu"])
            for i, row in enumerate(data):
                for j, col in enumerate(row):
                    item = QTableWidgetItem(str(col))
                    self.dstk.setItem(i, j, item)
        except mdb.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi tìm kiếm: {e}")

    def hien_thi_chitiet(self, row, col):
        """Display account details when a row is clicked."""
        tk = self.dstk.item(row, 0).text()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM qldv.user WHERE user = %s", (tk,))
        data = cursor.fetchone()

        # Display details in lineEdits
        self.tkngdung.setText(data[0])
        self.mkngdung.setText(data[1])

    def sua_tk(self):
        """Update an existing user account."""
        tk = self.tkngdung.text()
        mk = self.mkngdung.text()

        # Check for empty fields
        if not tk or not mk:
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return

        cursor = db.cursor()
        query = "UPDATE qldv.user SET pass = %s WHERE user = %s"
        values = (mk, tk)
        try:
            cursor.execute(query, values)
            db.commit()
            QMessageBox.information(self, "Thông báo", "Sửa tài khoản thành công!")
            self.load_tk()  # Refresh the table
            widget.setCurrentIndex(5)
        except mdb.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi sửa tài khoản: {e}")

    def xoa_tk(self):
        """Xóa tài khoản."""
        # Lấy dòng được chọn
        selected_rows = self.dstk.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một tài khoản để xóa!")
            return

        # Lấy tài khoản từ dòng được chọn
        row = selected_rows[0].row()
        tk = self.dstk.item(row, 0).text()

        # Xác nhận xóa tài khoản
        reply = QMessageBox.question(self, "Xóa tài khoản", f"Bạn có chắc chắn muốn xóa tài khoản {tk}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            cursor = db.cursor()
            query = "DELETE FROM qldv.user WHERE user = %s"
            try:
                cursor.execute(query, (tk,))
                db.commit()
                QMessageBox.information(self, "Thông báo", "Xóa tài khoản thành công!")
                self.load_tk()
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Lỗi xóa tài khoản: {e}")

class Taotk_w(QMainWindow):
    def __init__(self):
        super(Taotk_w,self).__init__()
        uic.loadUi('taotk.ui',self)
        self.tbntao.clicked.connect(self.tao_tk)

    def tao_tk(self):
        un = self.taotk_2.text()
        psw = self.taomk.text()
        query = db.cursor()
        try:
            query.execute("SELECT * FROM qldv.user WHERE user = %s AND pass = %s", (un, psw))
            kt = query.fetchone()
            if kt:
                QMessageBox.information(self, "Reg output", "Tài khoản đã tồn tại")
                widget.setCurrentIndex(5)
            else:
                query.execute("INSERT INTO qldv.user VALUES (%s, %s)", (un, psw))
                db.commit()
                QMessageBox.information(self, "Reg output", "Tạo thành công")
                widget.setCurrentIndex(5)
        except mdb.Error as e:
            QMessageBox.information(self, "Thông báo", "Tài khoản đã tồn tại!")

class hd_w(QMainWindow):
    def __init__(self):
        super(hd_w, self).__init__()
        uic.loadUi('hd.ui', self)  # Load the UI from 'hd.ui'
        self.tobchidoan.clicked.connect(self.chidoan_a)
        self.tobdoanvien.clicked.connect(self.doanvien_a)
        self.tobnguoidung.clicked.connect(self.ngdung_a)
        self.tobdangxuat.clicked.connect(self.dang_xuat)
        self.btnThemhd.clicked.connect(self.them_hd)
        self.tbnTimhd.clicked.connect(self.tim_hd)
        self.btnSuahd.clicked.connect(self.sua_hd)
        self.btnXoahd.clicked.connect(self.xoa_hd)
        self.dshd.cellClicked.connect(self.hien_thi_chitiet)

        # Load hoạt động ban đầu
        self.load_hd()

    def dang_xuat(self):
        Login_f.user.setText('')
        Login_f.pw.setText('')
        widget.setCurrentIndex(0)

    def chidoan_a(self):
        widget.setCurrentIndex(3)

    def doanvien_a(self):
        widget.setCurrentIndex(4)

    def ngdung_a(self):
        widget.setCurrentIndex(5)

    def load_hd(self):
        """Load hoạt động từ database vào bảng."""
        cursor = db.cursor()
        cursor.execute("SELECT * FROM qldv.hoatdong")
        data = cursor.fetchall()
        self.dshd.setRowCount(len(data))
        self.dshd.setColumnCount(5)
        self.dshd.setHorizontalHeaderLabels(["Mã Hoạt Động", "Tên Hoạt Động", "Ngày Diễn Ra", "Ngày kêt thúc", "Mô Tả"])

        for i, row in enumerate(data):
            for j, col in enumerate(row):
                item = QTableWidgetItem(str(col))
                self.dshd.setItem(i, j, item)

    def them_hd(self):
        """Thêm mới hoạt động."""
        mahd = self.mahd.text()
        tenhd = self.tenhd.text()
        ngaydienrahd = self.ngaydienrahd.date().toString("yyyy-MM-dd")
        ngayketthuchd = self.ngayketthuchd.date().toString("yyyy-MM-dd")
        motahd = self.motahd.toPlainText()

        # Kiểm tra trường nhập liệu
        if not all([mahd, tenhd, ngaydienrahd, ngayketthuchd, motahd]):
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return

        # Thêm hoạt động vào database
        cursor = db.cursor()
        query = "INSERT INTO qldv.hoatdong (mahd, tenhd, ngaydienrahd, ngayketthuchd, motahd) VALUES (%s, %s, %s, %s, %s)"
        values = (mahd, tenhd, ngaydienrahd, ngayketthuchd, motahd)
        try:
            cursor.execute(query, values)
            db.commit()
            QMessageBox.information(self, "Thông báo", "Thêm hoạt động thành công!")
            self.load_hd()
        except mdb.Error as e:
            QMessageBox.information(self, "Thông báo", "Hoạt động đã tồn tại!")

    def tim_hd(self):
        """Tìm kiếm hoạt động."""
        tukhoa = self.Timhd.text()
        if not tukhoa:
            self.load_hd()  # Hiển thị tất cả hoạt động nếu không có từ khóa
            return

        cursor = db.cursor()
        query = """
        SELECT * FROM qldv.hoatdong
        WHERE mahd LIKE %s OR tenhd LIKE %s
        """
        values = (f"%{tukhoa}%", f"%{tukhoa}%")
        try:
            cursor.execute(query, values)
            data = cursor.fetchall()
            self.dshd.setRowCount(len(data))
            self.dshd.setColumnCount(5)
            self.dshd.setHorizontalHeaderLabels(["Mã Hoạt Động", "Tên Hoạt Động", "Ngày Diễn Ra", "Ngày kết thúc", "Mô Tả"])
            for i, row in enumerate(data):
                for j, col in enumerate(row):
                    item = QTableWidgetItem(str(col))
                    self.dshd.setItem(i, j, item)
        except mdb.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi tìm kiếm hoạt động: {e}")

    def hien_thi_chitiet(self, row, col):
        """Hiển thị chi tiết hoạt động khi click vào hàng trong bảng."""
        mahd = self.dshd.item(row, 0).text()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM qldv.hoatdong WHERE mahd = %s", (mahd,))
        data = cursor.fetchone()

        # Hiển thị thông tin chi tiết
        self.mahd.setText(data[0])
        self.tenhd.setText(data[1])
        self.ngaydienrahd.setDate(QtCore.QDate.fromString(data[2], "yyyy-MM-dd"))
        self.ngayketthuchd.setDate(QtCore.QDate.fromString(data[3], "yyyy-MM-dd"))
        self.motahd.setText(data[4])

    def sua_hd(self):
        """Sửa thông tin hoạt động."""
        mahd = self.mahd.text()
        tenhd = self.tenhd.text()
        ngaydienrahd = self.ngaydienrahd.date().toString("yyyy-MM-dd")
        ngayketthuchd = self.ngayketthuchd.date().toString("yyyy-MM-dd")
        motahd = self.motahd.toPlainText()

        # Kiểm tra trường nhập liệu
        if not all([mahd, tenhd, ngaydienrahd, ngayketthuchd, motahd]):
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return

        # Cập nhật thông tin hoạt động vào database
        cursor = db.cursor()
        query = "UPDATE qldv.hoatdong SET tenhd = %s, ngaydienrahd = %s, ngayketthuchd = %s, motahd = %s WHERE mahd = %s"
        values = (tenhd, ngaydienrahd, ngayketthuchd, motahd, mahd)
        try:
            cursor.execute(query, values)
            db.commit()
            QMessageBox.information(self, "Thông báo", "Sửa hoạt động thành công!")
            self.load_hd()
        except mdb.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi sửa hoạt động: {e}")

    def xoa_hd(self):
        """Xóa hoạt động."""
        # Lấy dòng được chọn
        selected_rows = self.dshd.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một hoạt động để xóa!")
            return

        # Lấy mã hoạt động từ dòng được chọn
        row = selected_rows[0].row()
        mahd = self.dshd.item(row, 0).text()

        # Xác nhận xóa hoạt động
        reply = QMessageBox.question(self, "Xóa hoạt động", f"Bạn có chắc chắn muốn xóa hoạt động có mã {mahd}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Xóa hoạt động khỏi database
            cursor = db.cursor()
            query = "DELETE FROM qldv.hoatdong WHERE mahd = %s"
            try:
                cursor.execute(query, (mahd,))
                db.commit()
                QMessageBox.information(self, "Thông báo", "Xóa hoạt động thành công!")
                self.load_hd()
            except mdb.Error as e:
                QMessageBox.critical(self, "Lỗi", f"Lỗi xóa hoạt động: {e}")

    

app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
Login_f = Login_w()
Dangky_f = Dangky_w()
Main_f = Main_w()
Chidoan_f = Chidoan_w()
Doanvien_f = Doanvien_w()
Ngdung_f = Ngdung_w()
hd_f = hd_w()
Taotk_f = Taotk_w()
widget.addWidget(Login_f)
widget.addWidget(Dangky_f)
widget.addWidget(Main_f)
widget.addWidget(Chidoan_f)
widget.addWidget(Doanvien_f)
widget.addWidget(Ngdung_f)
widget.addWidget(hd_f)
widget.addWidget(Taotk_f)
# Thiết lập tín hiệu selectionChanged cho bảng chi đoàn
Chidoan_f.tablechidoan.cellClicked.connect(Chidoan_f.xoa_chidoan)
# Thiết lập tín hiệu selectionChanged cho bảng đoàn viên
Doanvien_f.dsdoanvien.cellClicked.connect(Doanvien_f.xoa_doanvien)
# Thiết lập tín hiệu selectionChanged cho bảng tài khoản
Ngdung_f.dstk.cellClicked.connect(Ngdung_f.xoa_tk)
# Thiết lập tín hiệu selectionChanged cho bảng hoạt động
hd_f.dshd.cellClicked.connect(hd_f.xoa_hd)
widget.setCurrentIndex(0)
widget.setFixedHeight(600)
widget.setFixedWidth(630)
widget.show()
app.exec()
