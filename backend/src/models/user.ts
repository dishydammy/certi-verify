import mongoose, { Document, Schema, Types } from 'mongoose';


export interface IUser extends Document {
  walletAddress: string;
  email?: string;
  name: string;
  role: 'student' | 'admin' | 'instructor';
  createdAt: Date;
}

const UserSchema = new Schema<IUser>({
  walletAddress: {
    type: String,
    required: true,
    unique: true,
    lowercase: true,
    trim: true,
  },
  email: {
    type: String,
    required: false,
    lowercase: true,
    trim: true,
  },
  name: {
    type: String,
    required: true,
    trim: true,
  },
  role: {
    type: String,
    enum: ['student', 'admin', 'instructor'],
    default: 'student',
  },
  createdAt: {
    type: Date,
    default: Date.now,
  },
});

export const UserModel = mongoose.model<IUser>('User', UserSchema);


