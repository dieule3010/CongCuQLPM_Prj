const fs = require("fs");
const path = require("path");

// đường dẫn đến file JSON
const file = path.join(__dirname, "../../data/orders.json");

// đọc file JSON
function readOrders() {
  if (!fs.existsSync(file)) return [];
  const data = fs.readFileSync(file);
  return JSON.parse(data);
}

// ghi file JSON
function writeOrders(data) {
  fs.writeFileSync(file, JSON.stringify(data, null, 2));
}

/*
|--------------------------------------------------------------------------
| 1. TẠO ĐƠN HÀNG
|--------------------------------------------------------------------------
*/
exports.createOrder = (req, res) => {
  const orders = readOrders();

  const newOrder = {
    id: Date.now(),
    items: req.body.items || [],
    status: "pending",
    rating: null,
    payment: "unpaid",
    created_at: new Date()
  };

  orders.push(newOrder);
  writeOrders(orders);

  res.json({
    message: "Đơn hàng đã được tạo",
    data: newOrder
  });
};

/*
|--------------------------------------------------------------------------
| 2. LẤY DANH SÁCH ĐƠN HÀNG
|--------------------------------------------------------------------------
*/
exports.getMyOrders = (req, res) => {
  const orders = readOrders();
  res.json(orders);
};

/*
|--------------------------------------------------------------------------
| 3. LẤY 1 ĐƠN THEO ID
|--------------------------------------------------------------------------
*/
exports.getOrderById = (req, res) => {
  const orders = readOrders();
  const id = parseInt(req.params.id);

  const order = orders.find(o => o.id === id);
  if (!order)
    return res.status(404).json({ message: "Không tìm thấy đơn hàng" });

  res.json(order);
};

/*
|--------------------------------------------------------------------------
| 4. CẬP NHẬT TRẠNG THÁI
|--------------------------------------------------------------------------
*/
exports.updateStatus = (req, res) => {
  const orders = readOrders();
  const id = parseInt(req.params.id);

  const order = orders.find(o => o.id === id);
  if (!order)
    return res.status(404).json({ message: "Không tìm thấy đơn hàng" });

  order.status = req.body.status;

  writeOrders(orders);

  res.json({
    message: "Cập nhật trạng thái thành công",
    data: order
  });
};

/*
|--------------------------------------------------------------------------
| 5. GỬI ĐÁNH GIÁ
|--------------------------------------------------------------------------
*/
exports.sendRating = (req, res) => {
  const orders = readOrders();
  const id = parseInt(req.params.id);

  const order = orders.find(o => o.id === id);
  if (!order)
    return res.status(404).json({ message: "Không tìm thấy đơn hàng" });

  order.rating = req.body.rating;

  writeOrders(orders);

  res.json({
    message: "Đánh giá thành công",
    data: order
  });
};

/*
|--------------------------------------------------------------------------
| 6. THANH TOÁN
|--------------------------------------------------------------------------
*/
exports.payOrder = (req, res) => {
  const orders = readOrders();
  const id = parseInt(req.params.id);

  const order = orders.find(o => o.id === id);
  if (!order)
    return res.status(404).json({ message: "Không tìm thấy đơn hàng" });

  order.payment = "paid";
  order.status = "completed";

  writeOrders(orders);

  res.json({
    message: "Thanh toán thành công",
    data: order
  });
};
