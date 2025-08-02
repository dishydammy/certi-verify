import { UserModel } from "../models/user";
import { Request, Response } from "express";
import { hash, genSalt, compare } from "bcryptjs";
import { generateToken, verifyToken } from "../utils/token";


export const register = async (req: Request, res: Response) => {
    const { email, name, password } = req.body

    const userExist = await UserModel.findOne({ email })

    if (userExist) return res.status(400).json({ msg: "user already exist" })

    const salt = await genSalt(10)
    const hashedPassoword = await hash(password, salt)

    const newUser = await UserModel.create({ email, name, password: hashedPassoword })

    // const sendMail =  logic to send mail once user is created

    res.status(201).json({ msg: "user created succesfully, check your mail to verify your account" })

}

export const verifyUser = async (req: Request, res: Response) => {
    const token = req.query.token as string;

    if (!token) {
        return res.status(400).json({ message: 'Verification token missing' });
    }

    try {
        const decoded = verifyToken(token) as { userId: string };
        // Find user and update
        const user = await UserModel.findById(decoded.userId);
        if (!user) {
            return res.status(404).json({ message: 'User not found' });
        }

        if (user.isEmailVerified) {
            return res.status(400).json({ message: 'Email already verified' });
        }

        user.isEmailVerified = true;
        await user.save();

        return res.status(200).json({ message: 'Email verified successfully' });
    } catch (err) {
        return res.status(400).json({ message: 'Invalid or expired token' });
    }

}

export const login = async (req: Request, res: Response) => {
    const { email, password } = req.body
    const user = await UserModel.findOne({ email })
    if (!user)
        return res.status(400).json({ msg: "Invalid parameter" })
    // if (!user.isEmailVerified)
    //     return res.status(400).json({ msg: "Email not verified" })
    const passwordMatch = await compare(password, user.password);
    if (!passwordMatch)
        return res.status(400).json({ msg: "Invalid Parameters" })
    const token = generateToken(user._id as string)

    res.status(201).json({ token, user })
}

export const forgotPassword = async (req: Request, res: Response) => {
    const { email } = req.body
    const user = await UserModel.find({ email })
    if (!user)
        return res.status(400).json({ msg: "Invalid parameter" })
    // Logic to send reset password email
    res.status(200).json({ msg: "Reset password email sent" })
}

export const resetPassword = async (req: Request, res: Response) => {
    const { token, newPassword } = req.body
    if (!token || !newPassword) {
        return res.status(400).json({ msg: "Token and new password are required" });
    }

    try {
        const decoded = verifyToken(token) as { userId: string };
        const user = await UserModel.findById(decoded.userId);
        if (!user) {
            return res.status(404).json({ msg: "User not found" });
        }

        const salt = await genSalt(10);
        user.password = await hash(newPassword, salt);
        await user.save();

        return res.status(200).json({ msg: "Password reset successfully" });
    } catch (error) {
        return res.status(400).json({ msg: "Invalid or expired token" });
    }
}