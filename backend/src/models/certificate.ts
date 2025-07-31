import mongoose, { Document, Schema, Types } from 'mongoose';

export interface ICertificate extends Document {
  student: Types.ObjectId;
  submission: Types.ObjectId;
  metadataURI: string;
  tokenId: number;
  txHash: string;
  issuedAt: Date;
}

const CertificateSchema = new Schema<ICertificate>({
  student: { type: Schema.Types.ObjectId, ref: 'User', required: true },
  submission: { type: Schema.Types.ObjectId, ref: 'Submission', required: true },
  metadataURI: { type: String, required: true },
  tokenId: { type: Number, required: true },
  txHash: { type: String, required: true },
  issuedAt: { type: Date, default: Date.now },
});

export const CertificateModel = mongoose.model<ICertificate>('Certificate', CertificateSchema);
