import mongoose from "mongoose";
import dotenv from "dotenv";
dotenv.config();

export const connectToDatabase = () => {
    if (!process.env.MONGODB_URI) {
        throw new Error("MONGODB_URI is not defined in environment variables");
    }
mongoose.connect(process.env.MONGODB_URI).then(() => {
  console.log("Database connected successfully");
}).catch((error) => {
  console.error("Database connection error:", error);
}); }