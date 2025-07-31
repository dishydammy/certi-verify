import mongoose, { Document, Schema, Types } from 'mongoose';

interface IAnswer {
  question: Types.ObjectId;
  response: any;
  isCorrect: boolean;
  marksAwarded: number;
}

export interface ISubmission extends Document {
  quiz: Types.ObjectId;
  student: Types.ObjectId;
  answers: IAnswer[];
  score: number;
  percentage: number;
  passed: boolean;
  certificate?: Types.ObjectId;
  submittedAt: Date;
}

const SubmissionSchema = new Schema<ISubmission>({
  quiz: { type: Schema.Types.ObjectId, ref: 'Quiz', required: true },
  student: { type: Schema.Types.ObjectId, ref: 'User', required: true },
  answers: [
    {
      question: { type: Schema.Types.ObjectId, ref: 'Question' },
      response: Schema.Types.Mixed,
      isCorrect: Boolean,
      marksAwarded: Number,
    },
  ],
  score: { type: Number, required: true },
  percentage: { type: Number, required: true },
  passed: { type: Boolean, required: true },
  certificate: { type: Schema.Types.ObjectId, ref: 'Certificate' },
  submittedAt: { type: Date, default: Date.now },
});

export const SubmissionModel = mongoose.model<ISubmission>('Submission', SubmissionSchema);
