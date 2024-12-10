DROP TABLE IF EXISTS Users;
CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,       -- Mã người dùng (khóa chính, tự động tăng)
    user_name TEXT NOT NULL,                         -- Tên người dùng (không được để trống)
    user_email TEXT NOT NULL UNIQUE,                 -- Email người dùng (phải là duy nhất)
    user_phone TEXT NOT NULL UNIQUE,                 -- Số điện thoại
    user_password TEXT NOT NULL,                     -- Mật khẩu
    user_date_of_birth DATE NOT NULL,                -- Ngày sinh
    user_gender TEXT NOT NULL,                       -- Giới tính
    user_address TEXT NOT NULL,                      -- Địa chỉ
    user_is_admin BOOLEAN NOT NULL DEFAULT 0         -- Quyền admin, mặc định là không phải admin
);

DROP TABLE IF EXISTS Books;
CREATE TABLE Books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,        -- Mã sách (khóa chính, tự động tăng)
    title TEXT NOT NULL,                              -- Tiêu đề sách
    author TEXT NOT NULL,                             -- Tác giả
    description TEXT,                                 -- Mô tả sách
    price DECIMAL(10, 3) NOT NULL,                    -- Giá sách
    image_url TEXT,                                   -- URL (hình ảnh hoặc sách điện tử)
    publication_date DATE,                            -- Ngày xuất bản
    category TEXT NOT NULL,                           -- Thể loại sách
    level_class INT NOT NULL,                         -- Lớp
    level_school TEXT NOT NULL,                       -- Cấp trường (Tiểu học, Trung học cs, Trung học pt)
    stock_quantity INTEGER NOT NULL DEFAULT 0,        -- Số lượng tồn kho
    publisher TEXT NOT NULL,                          -- Nhà xuất bản
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,   -- Ngày tạo bản ghi
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP    -- Ngày cập nhật bản ghi
);

DROP TABLE IF EXISTS Orders;
CREATE TABLE Orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,         -- Mã đơn hàng (khóa chính, tự động tăng)
    user_id INTEGER NOT NULL,                           -- Mã người dùng (khóa ngoại)
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,     -- Ngày đặt hàng
    status TEXT NOT NULL DEFAULT 'Chờ xác nhận',        -- Trạng thái đơn hàng
    total_price DECIMAL(10, 3) NOT NULL,                -- Tổng giá trị đơn hàng
    recipient_name TEXT NOT NULL,                       -- Tên người nhận
    recipient_phone TEXT NOT NULL,                      -- Số điện thoại người nhận 
    recipient_email TEXT NOT NULL,                      -- Email người nhận
    shipping_address TEXT NOT NULL,                     -- Địa chỉ giao hàng
    payment_method TEXT NOT NULL,                       -- Phương thức thanh toán
    payment_status TEXT NOT NULL DEFAULT 'Chưa thanh toán', -- Trạng thái thanh toán
    shipping_date DATE,                                 -- Ngày vận chuyển
    delivery_date DATE,                                 -- Ngày giao hàng thành công
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,     -- Ngày tạo bản ghi
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,     -- Ngày cập nhật bản ghi
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE  -- Ràng buộc khóa ngoại
);

DROP TABLE IF EXISTS Order_Items;
CREATE TABLE Order_Items (
    order_id INTEGER NOT NULL,                          -- Mã đơn hàng (khóa phụ)
    book_id INTEGER NOT NULL,                           -- Mã sản phẩm (khóa phụ)
    quantity INTEGER NOT NULL,                          -- Số lượng sản phẩm
    price_per_item DECIMAL(10, 3),                      -- Giá mỗi sản phẩm
    total_price DECIMAL(10, 3) NOT NULL,                -- Tổng giá trị của mục này (quantity * price_per_item)
    PRIMARY KEY (order_id, book_id),                    -- Đặt order_id và book_id làm khóa chính
    FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES Books(book_id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS Carts;
CREATE TABLE Carts (
    cart_id INTEGER PRIMARY KEY AUTOINCREMENT,          -- Mã giỏ hàng
    user_id INTEGER NOT NULL UNIQUE,                    -- Mã người dùng (khóa ngoại, đảm bảo mỗi user chỉ có một giỏ hàng)
    quantity INTEGER NOT NULL DEFAULT 0,                -- Số lượng sách trong giỏ
    total_amount DECIMAL(10, 3) NOT NULL DEFAULT 0,     -- Tổng tiền trong giỏ
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS Cart_Items;
CREATE TABLE Cart_Items (
    cart_id INTEGER NOT NULL,                           -- Mã giỏ hàng (khóa ngoại)
    book_id INTEGER NOT NULL,                           -- Mã sách (khóa ngoại)
    quantity INTEGER NOT NULL DEFAULT 1,                -- Số lượng sách trong giỏ
    price_at_purchase DECIMAL(10, 3) NOT NULL,          -- Giá tại thời điểm thêm
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,       -- Ngày giờ thêm sách vào giỏ
    PRIMARY KEY (cart_id, book_id),                     -- Khóa chính
    FOREIGN KEY (cart_id) REFERENCES Carts(cart_id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES Books(book_id) ON DELETE CASCADE
);
