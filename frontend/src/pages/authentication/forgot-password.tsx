import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Mail, ArrowRight, ArrowLeft, Shield, CheckCircle } from "lucide-react";
import { useState } from "react";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle password reset logic here
    console.log("Password reset request for:", email);
    setIsSubmitted(true);
  };

  if (isSubmitted) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex flex-col">
        {/* Header */}
        <header className="px-6 py-4">
          <div className="max-w-4xl mx-auto">
            <Badge variant="secondary" className="inline-flex items-center gap-2">
              🚀 AI Skills Verification Platform
            </Badge>
          </div>
        </header>

        {/* Success Message */}
        <main className="flex-1 flex items-center justify-center px-6 py-20">
          <div className="w-full max-w-md">
            <Card className="border-2 shadow-xl">
              <CardHeader className="text-center">
                <div className="mx-auto w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mb-4">
                  <CheckCircle className="h-8 w-8 text-green-600" />
                </div>
                <CardTitle className="text-2xl">Check Your Email</CardTitle>
                <CardDescription>
                  We've sent password reset instructions to {email}
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <Alert>
                  <Mail className="h-4 w-4" />
                  <AlertDescription>
                    If you don't see the email in a few minutes, check your spam folder or try again with a different email address.
                  </AlertDescription>
                </Alert>

                <div className="space-y-3">
                  <Button className="w-full" onClick={() => window.open('mailto:', '_blank')}>
                    <Mail className="mr-2 h-4 w-4" />
                    Open Email App
                  </Button>
                  
                  <Button variant="outline" className="w-full" onClick={() => setIsSubmitted(false)}>
                    Try Another Email
                  </Button>
                </div>

                <div className="text-center text-sm text-muted-foreground">
                  Remember your password?{" "}
                  <Button variant="link" className="p-0 h-auto text-blue-600 hover:text-blue-700">
                    Back to Sign In
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </main>

        {/* Footer */}
        <footer className="px-6 py-8 bg-white/30">
          <div className="max-w-4xl mx-auto text-center">
            <p className="text-sm text-muted-foreground">
              © 2025 AI Skills Verification Platform. Built with ❤️ for the future of education.
            </p>
          </div>
        </footer>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex flex-col">
      {/* Header */}
      <header className="px-6 py-4">
        <div className="max-w-4xl mx-auto">
          <Badge variant="secondary" className="inline-flex items-center gap-2">
            🚀 AI Skills Verification Platform
          </Badge>
        </div>
      </header>

      {/* Main Forgot Password Content */}
      <main className="flex-1 flex items-center justify-center px-6 py-20">
        <div className="w-full max-w-md">
          <Card className="border-2 shadow-xl">
            <CardHeader className="text-center">
              <div className="mx-auto w-16 h-16 bg-gradient-to-r from-blue-100 to-purple-100 rounded-full flex items-center justify-center mb-4">
                <Shield className="h-8 w-8 text-blue-600" />
              </div>
              <CardTitle className="text-2xl bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Reset Password
              </CardTitle>
              <CardDescription>
                Enter your email address and we'll send you instructions to reset your password
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="email" className="flex items-center gap-2">
                    <Mail className="h-4 w-4" />
                    Email Address
                  </Label>
                  <Input
                    id="email"
                    type="email"
                    placeholder="Enter your email address"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>

                <Button type="submit" className="w-full">
                  Send Reset Instructions
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </form>

              <div className="text-center">
                <Button variant="ghost" className="text-blue-600 hover:text-blue-700">
                  <ArrowLeft className="mr-2 h-4 w-4" />
                  Back to Sign In
                </Button>
              </div>

              <Alert>
                <Shield className="h-4 w-4" />
                <AlertDescription>
                  For security reasons, we'll only send reset instructions to registered email addresses.
                </AlertDescription>
              </Alert>

              <div className="text-center text-sm text-muted-foreground">
                Don't have an account?{" "}
                <Button variant="link" className="p-0 h-auto text-blue-600 hover:text-blue-700">
                  Sign up for free
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>

      {/* Footer */}
      <footer className="px-6 py-8 bg-white/30">
        <div className="max-w-4xl mx-auto text-center">
          <p className="text-sm text-muted-foreground">
            © 2025 AI Skills Verification Platform. Built with ❤️ for the future of education.
          </p>
        </div>
      </footer>
    </div>
  );
}