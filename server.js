const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

// routes
const orderRoutes = require('./routes/order.routes');
app.use('/api/orders', orderRoutes);

// health
app.get('/', (req, res) => res.send({ status: 'ok' }));

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
