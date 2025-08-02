import { Response } from 'express';
import { Request } from '../types';
import { UserModel } from '../models/user';

export const getAllUsers = async (req: Request, res: Response) => {
    try {
        const users = await UserModel.find({}, '-password'); // Exclude password field
        res.status(200).json(users);
    } catch (error) {
        res.status(500).json({ message: 'Error fetching users', error });
    }
}