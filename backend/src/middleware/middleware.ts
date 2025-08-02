import { Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import {Request} from '../types/index'

// // Extend Express Request interface to include 'user'
// declare global {
//   namespace Express {
//     interface Request {
//       user?: any;
//     }
//   }
// }

export const isAuthenticated = (req: Request, res: Response, next: NextFunction) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ message: 'Unauthorized' });

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET!);
    req.userId = decoded;
    next();
  } catch (err) {
    res.status(401).json({ message: 'Invalid token' });
  }
};
