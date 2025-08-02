// import axios from "axios";
// import dotenv from "dotenv";

// dotenv.config();

// const SENDER_API_URL = "https://api.sender.net/v2/subscribers";
// const SENDER_TOKEN = process.env.SENDER_TOKEN;

// if (!SENDER_TOKEN) {
//   throw new Error("SENDER_TOKEN is not defined");
// }

// export const sendMail = async (
//   email: string,
//   firstname: string,
//   otp: string
// ): Promise<boolean> => {
//   const data = {
//     email,
//     firstname,
//     groups: [process.env.SENDER_OTP_GROUP],
//     fields: { "{$otp}": otp.toString() },
//   };

//   try {
//     const response = await axios.post(SENDER_API_URL, data, {
//       headers: {
//         Authorization: `Bearer ${SENDER_TOKEN}`,
//         "Content-Type": "application/json",
//       },
//     });

//     const responseData = response.data as {
//       success: boolean;
//       message?: string;
//     };
//     if (!responseData.success) {
//       const errorMessage =
//         (response.data as { message?: string }).message || "Unknown error";
//       throw new Error(`Error sending mail: ${errorMessage}`);
//     }

//     return true;
//   } catch (error) {
//     const errorMessage =
//       (error as any).response?.data?.message ||
//       (error as any).message ||
//       "Unknown error";
//     throw new Error(`Error sending mail: ${errorMessage}`);
//   }
// };
