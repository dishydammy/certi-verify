import express from 'express'
import { connectToDatabase } from './config/db-config';
import authRoutes from './routes/auth-routes'
import userRoutes from './routes/user-routes';

connectToDatabase()
const app = express();

app.use(express.json())
app.get('/', (req, res) => {
  res.send('Hello World!');
});
app.use('/api/auth', authRoutes)
app.use('/api/user', userRoutes);
app.listen(3000, () => {
  console.log('Server is running on http://localhost:3000');
});