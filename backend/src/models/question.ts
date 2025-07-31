import mongoose, { Document, Schema, Types } from 'mongoose';

interface IOption {
  text: string;
  isCorrect: boolean;
}

export interface IQuestion extends Document {
  quiz: Types.ObjectId;
  text: string;
  type: 'multiple-choice' | 'true-false' | 'short-answer';
  options: IOption[];
  marks: number;
}

const QuestionSchema = new Schema<IQuestion>({
  quiz: { type: Schema.Types.ObjectId, ref: 'Quiz', required: true },
  text: { type: String, required: true },
  type: {
    type: String,
    enum: ['multiple-choice', 'true-false', 'short-answer'],
    default: 'multiple-choice',
  },
  options: [
    {
      text: String,
      isCorrect: Boolean,
    },
  ],
  marks: { type: Number, default: 1 },
});

export const QuestionModel = mongoose.model<IQuestion>('Question', QuestionSchema);
