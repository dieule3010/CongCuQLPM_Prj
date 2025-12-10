const express = require('express');
const router = express.Router();
const orderCtrl = require('../controllers/order.controller');

// tạo đơn
router.post('/', orderCtrl.createOrder);

// lấy danh sách
router.get('/', orderCtrl.getMyOrders);

// lấy 1 đơn
router.get('/:id', orderCtrl.getOrderById);

// cập nhật trạng thái
router.patch('/:id/status', orderCtrl.updateStatus);

// gửi rating
router.post('/:id/rating', orderCtrl.sendRating);

// thanh toán
router.post('/:id/pay', orderCtrl.payOrder);

module.exports = router;
