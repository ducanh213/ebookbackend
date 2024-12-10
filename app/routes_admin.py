from flask import Blueprint, jsonify
from sqlalchemy import text
from app import db
from flask import request
from .models import Book, User, Order, Cart,CartItem,OrderItem

api_admin = Blueprint('apiAdmin', __name__)

def error_response(message, status_code):
    return jsonify({"error": message}), status_code

LIMIT_RECENT = 5
PASS_DEFAULT = "123456"

# ----------------------------------------------------------------------------------
# Route cho ADMIN
@api_admin.route('/admin', methods=['GET'])
def home():
    return "Welcome ADMIN!"
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# Route cho dashboard
@api_admin.route('/dashboard', methods=['GET'])
def dashboard():
    orders = Order.query.count()
    books  =  Book.query.all()
    users = User.query.count()
    item = 0
    for book in books:
        item += book.stock_quantity
    return jsonify(
        {
            "order": orders,
            "book" : len(books),
            "user" : users,
            "item": item
        }
    ), 201
# ----------------------------------------------------------------------------------

@api_admin.route('/order-recent', methods=['GET'])
def OrderRecent():
    entities = Order.query.order_by(Order.created_at.desc()).limit(LIMIT_RECENT).all()
    entities_list = [order.to_dict() for order in entities]  # Chuyển mỗi book thành dict
    return jsonify(entities_list), 200

@api_admin.route('/user-recent', methods=['GET'])
def UserRecent():
    entities = User.query.limit(LIMIT_RECENT).all()
    entities_list = [user.to_dict() for user in entities]  # Chuyển mỗi book thành dict
    return jsonify(entities_list), 200

@api_admin.route('/user-paging', methods=['POST'])
def UserPaging():
    data = request.get_json()
    search = '%' + data['search'] + '%'
    page_number = data['page_number']
    page_size = data['page_size']
    if page_size is None or page_size < 1:
        page_size = 1
    

    entities = User.query.filter(User.user_name.like(search)).offset((page_number - 1) * page_size).limit(page_size).all()

    entities_list = [entity.to_dict() for entity in entities]  # Chuyển mỗi book thành dict
    return entities_list

@api_admin.route('/orders',methods=['POST'])
def get_carts():
    data = request.get_json()
    search = '%' + data['search'] + '%'
    orders= Order.query.filter(Order.recipient_name.like(search)).all()
    orders_list = [cart.to_dict() for cart in orders]
    if not orders:
         return jsonify({"error": "Cart not found"}), 404

    for order in orders_list:
        user = User.query.filter_by(user_id=order['user_id']).first()
        if user is None:
            order['user_name'] = "Ẩn danh"
        else:
            order['user_name'] = user.user_name
    return jsonify(orders_list), 200


@api_admin.route('/orderitems/<int:order_id>', methods=['GET'])
def get_user_orders(order_id):
    orderEntity = Order.query.filter_by(order_id=order_id).first()
    if not orderEntity:
        return error_response("Cart not found for this user", 404)
    order_items = OrderItem.query.filter_by(order_id=orderEntity.order_id).all()
    if not order_items:
        return error_response("Cart not found for this user", 404)

    orderItems = [entity.to_dict() for entity in order_items]

    for item in orderItems:
        book = Book.query.filter_by(book_id = item['book_id']).first()
        if book is None:
            item['book_name'] = "Item đã bị xóa"
        else:
            item['book_name'] = book.title

    return jsonify(orderItems), 200


@api_admin.route('/orders', methods=['PUT'])
def update_order():
    data = request.get_json()
    if data is None or data['order_id'] is None:
        return jsonify({"error": "Cart not found"}), 404
    order = Order.query.get(data['order_id'])
    if not order:
        return jsonify({"error": "Cart not found"}), 404
    try:
        order.status = data.get('status', order.status)
        # add thêm logic trừ sách nếu cần.
        order_items = OrderItem.query.filter_by(order_id=order.order_id).all()
        if not order_items:
            return error_response("Cart not found for this user", 404)
        orderItems = [entity.to_dict() for entity in order_items]
        for item in orderItems:
            book = Book.query.filter_by(book_id = item['book_id']).first()
            if book is not None:
                stock = book.stock_quantity - item['quantity']
                if stock < 0:
                    return error_response("Quantity over", 404)
                book.stock_quantity = stock
                db.session.commit()
            else:
                item['book_name'] = book.title
        db.session.commit()
        return jsonify(order.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update cart: {str(e)}"}), 400

@api_admin.route('/products',methods=['POST'])
def get_products():
    data = request.get_json()
    search = '%' + data['search'] + '%'
    entities= Book.query.filter(Book.title.like(search)).all()
    entities_list = [cart.to_dict() for cart in entities]
    if not entities:
         return jsonify({"error": "Cart not found"}), 404
    return jsonify(entities_list), 200

@api_admin.route('/products/<int:id>', methods=['GET'])
def get_product_detail(id):
    orderEntity = Book.query.filter_by(id=id).first()
    if not orderEntity:
        return error_response("Cart not found for this user", 404)

    return jsonify(orderEntity.to_dict()), 200

# Route để cập nhật thông tin sách
@api_admin.route('/books', methods=['PUT'])
def update_book():
    data = request.get_json()  # Nhận dữ liệu JSON từ client
    book = Book.query.get(data['id'])  # Tìm sách theo ID
    if not book:
        return jsonify({"error": "Book not found"}), 404  # Nếu không tìm thấy sách

    try:
        # Cập nhật thông tin sách
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.description = data.get('description', book.description)
        book.price = data.get('price', book.price)
        book.category = data.get('category', book.category)
        book.level_class = data.get('level_class', book.level_class)
        book.level_school = data.get('level_school', book.level_school)
        book.stock_quantity = data.get('stock_quantity', book.stock_quantity)
        book.publisher = data.get('publisher', book.publisher)
        db.session.commit()  # Lưu thay đổi vào database
        return jsonify(book.to_dict()), 200  # Trả về thông tin sách vừa cập nhật
    except Exception as e:
        db.session.rollback()  # Hủy bỏ nếu có lỗi
        return jsonify({"error": f"Failed to update book: {str(e)}"}), 400

# ------------------------------------------------------------------------------------
# Router để Thêm sách mới
@api_admin.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()  # Nhận dữ liệu JSON từ client
    try:
        # Tạo đối tượng sách mới
        new_book = Book(
            title=data['title'],
            author=data['author'],
            description=data.get('description', ''),
            price=data['price'],
            category=data['category'],
            level_class=data['level_class'],
            level_school=data['level_school'],
            stock_quantity=data.get('stock_quantity', 0),
            publisher=data['publisher']
        )
        db.session.add(new_book)  # Thêm sách mới vào session
        db.session.commit()  # Lưu thay đổi vào database
        return jsonify(new_book.to_dict()), 201  # Trả về thông tin sách vừa thêm
    except Exception as e:
        db.session.rollback()  # Hủy bỏ nếu có lỗi
        return jsonify({"error": f"Failed to create book: {str(e)}"}), 400
# ----------------------------------------------------------------------------------
#Route để lấy danh sách người dùng
@api_admin.route('/users', methods=['POST'])
def get_users():
    data = request.get_json()
    search = '%' + data['search'] + '%'
    entities= User.query.filter(User.user_name.like(search)).all()
    entities_list = [user.to_dict() for user in entities]
    if not entities:
         return jsonify({"error": "user not found"}), 404
    return jsonify(entities_list), 200
# ----------------------------------------------------------------------------------
# Route tạo người dùng mới
@api_admin.route('/add-user', methods=['POST'])
def create_user():
    """
    Tạo người dùng mới từ dữ liệu JSON gửi lên.
    """
    data = request.get_json()  # Lấy dữ liệu JSON từ client
    try:
        # Tạo đối tượng User mới
        new_user = User(
            user_name=data['user_name'],
            user_email=data['user_email'],
            user_phone=data['user_phone'],
            user_password = PASS_DEFAULT,  # Mã hóa mật khẩu nếu cần
            user_date_of_birth=data['user_date_of_birth'],
            user_gender=data['user_gender'],
            user_address=data['user_address'],
            user_is_admin=data.get('user_is_admin', False)  # Mặc định là người dùng thường
        )
        db.session.add(new_user)  # Thêm vào session
        db.session.commit()  # Lưu vào database
        return jsonify(new_user.to_dict()), 201  # Trả về thông tin người dùng mới
    except Exception as e:
        db.session.rollback()  # Hủy bỏ nếu có lỗi
        return jsonify({"error": f"Failed to create user: {str(e)}"}), 400
# ----------------------------------------------------------------------------------
# Route cập nhật thông tin người dùng theo ID
@api_admin.route('/users', methods=['PUT'])
def update_user():
    """
    Cập nhật thông tin người dùng dựa vào ID.
    """
    data = request.get_json()  # Lấy dữ liệu JSON từ client
    user = User.query.get(data['user_id'])  # Tìm người dùng theo ID
    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        # Cập nhật thông tin người dùng
        user.user_name = data.get('user_name', user.user_name)
        user.user_email = data.get('user_email', user.user_email)
        user.user_phone = data.get('user_phone', user.user_phone)
        user.user_password = data.get('user_password', user.user_password)  # Cập nhật mật khẩu nếu cần
        user.user_date_of_birth = data.get('user_date_of_birth', user.user_date_of_birth)
        user.user_gender = data.get('user_gender', user.user_gender)
        user.user_address = data.get('user_address', user.user_address)
        user.user_is_admin = data.get('user_is_admin', user.user_is_admin)

        db.session.commit()  # Lưu thay đổi vào database
        return jsonify(user.to_dict()), 200  # Trả về thông tin người dùng sau khi cập nhật
    except Exception as e:
        db.session.rollback()  # Hủy bỏ nếu có lỗi
        return jsonify({"error": f"Failed to update user: {str(e)}"}), 400
# ----------------------------------------------------------------------------------
# Route xóa người dùng
@api_admin.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Xóa người dùng dựa vào ID.
    """
    user = User.query.get(user_id)  # Tìm người dùng theo ID
    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        db.session.delete(user)  # Xóa người dùng
        db.session.commit()  # Lưu thay đổi vào database
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()  # Hủy bỏ nếu có lỗi
        return jsonify({"error": f"Failed to delete user: {str(e)}"}), 400
# ----------------------------------------------------------------------------------