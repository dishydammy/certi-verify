import { z } from 'zod';
const loginSchema = z.object({
    email: z.string().email(),
    password: z.string().min(6),
});

const registerSchema = z.object({
    name: z.string().min(2).max(50),
    email: z.string().email(),
    password: z.string().min(6),
});

export type LoginUser = z.infer<typeof loginSchema>;
export type RegisterUser = z.infer<typeof registerSchema>;

export const validateUserLogin = (user: LoginUser) => {
    return loginSchema.safeParse(user);
};

export const validateUserUpdate = (user: Partial<LoginUser>) => {
    return loginSchema.partial().safeParse(user);
};

export const validateUserId = (id: string) => {
    return z.string().uuid().safeParse(id);
};

export const validateEmail = (email: string) => {
    return z.string().email().safeParse(email);
};

export const validateRegisterUser = (user: RegisterUser) => {
    return registerSchema.safeParse(user);
}
