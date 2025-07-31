import mongoose, { Document, Schema, Types } from 'mongoose';
export interface IQuiz extends Document {
  title: string;
  description?: string;
  questions: Types.ObjectId[];
  createdBy: Types.ObjectId;
  duration: number;
  passingScore: number;
  isPublished: boolean;
  createdAt: Date;
}

const QuizSchema = new Schema<IQuiz>({
  title: { type: String, required: true },
  description: { type: String },
  questions: [{ type: Schema.Types.ObjectId, ref: 'Question' }],
  createdBy: { type: Schema.Types.ObjectId, ref: 'User', required: true },
  duration: { type: Number, default: 0 },
  passingScore: { type: Number, default: 0 },
  isPublished: { type: Boolean, default: false },
  createdAt: { type: Date, default: Date.now },
});

export const QuizModel = mongoose.model<IQuiz>('Quiz', QuizSchema);
