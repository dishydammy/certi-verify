import mongoose, { Document, Schema, Types } from 'mongoose';


export interface IUser extends Document {
  walletAddress: string;
  email?: string;
  name: string;
  password: string;
  role: 'student' | 'admin' | 'instructor';
  isEmailVerified: boolean;
  createdAt: Date;
}

const UserSchema = new Schema<IUser>({
  walletAddress: {
    type: String,
    // required: true,
    unique: true,
    lowercase: true,
    trim: true,
  },
  email: {
    type: String,
    required: true,
    lowercase: true,
    trim: true,
  },
  name: {
    type: String,
    required: true,
    trim: true,
  },
  password: { type: String },
  role: {
    type: String,
    enum: ['student', 'admin', 'instructor'],
    default: 'student',
  },
  isEmailVerified: { type: Boolean, default: false },
  createdAt: {
    type: Date,
    default: Date.now,
  },
});

export const UserModel = mongoose.model<IUser>('User', UserSchema);


